import os
import io
import hashlib
from typing import Dict, Any, List, Generator, Optional
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from ..config.settings import SUPPORTED_EXTENSIONS

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

class DriveConnector:
    def __init__(self):
        """Initialize the Google Drive connector."""
        self.credentials = None
        self.service = None
        
    def authenticate(self, credentials_path: str = None):
        """Authenticate with Google Drive."""
        if credentials_path and os.path.exists(credentials_path):
            self.credentials = Credentials.from_authorized_user_file(credentials_path, SCOPES)
            
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secrets.json', SCOPES)
                self.credentials = flow.run_local_server(port=0)
                
            # Save credentials
            if credentials_path:
                with open(credentials_path, 'w') as token:
                    token.write(self.credentials.to_json())
                    
        self.service = build('drive', 'v3', credentials=self.credentials)
        
    def scan_folder(self, folder_id: str, recursive: bool = True) -> Generator[Dict[str, Any], None, None]:
        """Scan a Google Drive folder for supported files."""
        if not self.service:
            raise ValueError("Not authenticated. Call authenticate() first.")
            
        try:
            query = f"'{folder_id}' in parents and trashed = false"
            page_token = None
            
            while True:
                response = self.service.files().list(
                    q=query,
                    spaces='drive',
                    fields='nextPageToken, files(id, name, mimeType, modifiedTime, size)',
                    pageToken=page_token
                ).execute()
                
                for file in response.get('files', []):
                    if file['mimeType'] == 'application/vnd.google-apps.folder' and recursive:
                        # Recursively scan subfolders
                        yield from self.scan_folder(file['id'], recursive)
                    else:
                        extension = os.path.splitext(file['name'])[1].lower()
                        if any(extension in exts for exts in SUPPORTED_EXTENSIONS.values()):
                            yield {
                                'id': file['id'],
                                'name': file['name'],
                                'modified_time': file['modifiedTime'],
                                'size': file.get('size', 0)
                            }
                            
                page_token = response.get('nextPageToken')
                if not page_token:
                    break
                    
        except Exception as e:
            print(f"Error scanning Drive folder {folder_id}: {str(e)}")
            
    def download_file(self, file_id: str) -> io.BytesIO:
        """Download a file from Google Drive."""
        if not self.service:
            raise ValueError("Not authenticated. Call authenticate() first.")
            
        try:
            request = self.service.files().get_media(fileId=file_id)
            file_content = io.BytesIO()
            downloader = MediaIoBaseDownload(file_content, request)
            
            done = False
            while not done:
                _, done = downloader.next_chunk()
                
            file_content.seek(0)
            return file_content
            
        except Exception as e:
            print(f"Error downloading file {file_id}: {str(e)}")
            return None
            
    def _calculate_file_checksum(self, file_id: str) -> str:
        """Calculate checksum from the first part of a Drive file for fast comparison."""
        try:
            file_content = self.download_partial_file(file_id, bytes_limit=8192)
            if file_content:
                hasher = hashlib.md5()
                hasher.update(file_content.getvalue())
                return hasher.hexdigest()
            return ""
        except Exception as e:
            print(f"Error calculating checksum for file {file_id}: {str(e)}")
            return ""
            
    def download_partial_file(self, file_id: str, bytes_limit: int = 8192) -> Optional[io.BytesIO]:
        """Download just the first part of a file from Google Drive for checksum calculation."""
        if not self.service:
            raise ValueError("Not authenticated. Call authenticate() first.")
            
        try:
            request = self.service.files().get_media(fileId=file_id)
            file_content = io.BytesIO()
            downloader = MediaIoBaseDownload(file_content, request)
            
            # Download only first chunk
            _, done = downloader.next_chunk()
            file_content.seek(0)
            
            # If the file is larger than bytes_limit, truncate it
            if file_content.getbuffer().nbytes > bytes_limit:
                truncated = io.BytesIO(file_content.read(bytes_limit))
                return truncated
            
            return file_content
            
        except Exception as e:
            print(f"Error downloading partial file {file_id}: {str(e)}")
            return None
            
    def get_file_metadata(self, file_id: str) -> Dict[str, Any]:
        """Get metadata for a Google Drive file."""
        if not self.service:
            raise ValueError("Not authenticated. Call authenticate() first.")
            
        try:
            file = self.service.files().get(
                fileId=file_id,
                fields='id, name, mimeType, modifiedTime, size, createdTime'
            ).execute()
            
            # Calculate checksum for files that aren't too large
            size = int(file.get('size', 0))
            checksum = ""
            if size > 0 and size < 10485760:  # Skip files larger than 10MB
                checksum = self._calculate_file_checksum(file_id)
            
            return {
                'file_id': file['id'],
                'file_name': file['name'],
                'file_type': os.path.splitext(file['name'])[1].lower(),
                'mime_type': file['mimeType'],
                'size': size,
                'last_modified': file['modifiedTime'],
                'created': file['createdTime'],
                'checksum': checksum  # Add checksum to metadata
            }
            
        except Exception as e:
            print(f"Error getting metadata for file {file_id}: {str(e)}")
            return {} 