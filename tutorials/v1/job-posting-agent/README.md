# AI Job Posting Generator

This project uses aiXplain’s Agentic Framework to generate structured job postings based on a given job title or description.

## Features

- Multi-agent setup using `TeamAgentFactory`
- Agents specialized in:
  - Company culture analysis
  - Role requirements extraction
  - Job post creation
  - Industry trend analysis
- Uses Google Search Tool for real-time context
- Outputs job descriptions in Markdown format

## Requirements

- Python 3.8+
- aiXplain SDK
- aiXplain access key (set as `TEAM_API_KEY` environment variable)

## Usage

1. Install dependencies:
   ```bash
   pip install aixplain
   ```

2. Set your API key:
   ```bash
   export TEAM_API_KEY="your_key_here"
   ```

3. Run the script:
   ```bash
   python job_posting.py
   ```

## Output

Generates a fully formatted job post in Markdown based on the provided query.

## License

MIT License
