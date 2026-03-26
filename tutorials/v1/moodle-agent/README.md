# 🎓 Moodle Academic Agent

The **Moodle Academic Agent** is your personal AI assistant for staying on top of your academic life. It connects to your university’s Moodle system and helps you:

- 📝 Track upcoming assignments
- ❓ Stay informed about quizzes and tests
- 📚 View enrolled courses
- 📊 Monitor grades and academic progress
- 🗓️ Stay aware of calendar events and deadlines

The agent uses Moodle’s official web service API to fetch live data.

---

## 🚀 What the Agent Can Do

Depending on your query, the agent dynamically performs one of the following tasks:

| Task Type   | Use Case                            | Required Information             |
|-------------|-------------------------------------|----------------------------------|
| `assignments` | View upcoming homework and deadlines | Moodle token, course ID         |
| `quizzes`     | View quizzes/tests listed on Moodle | Moodle token, course ID         |
| `courses`     | Show the courses you're enrolled in | Moodle token, user ID           |
| `grades`      | Check your grades or progress       | Moodle token, course ID         |
| `calendar`    | View upcoming events and deadlines  | Moodle token                    |
| `site_info`   | Fetch user ID and account info      | Moodle token                    |

---

## 🛠️ What You Need to Use the Agent

Before using the Moodle Academic Agent, you'll need to gather the following information from your Moodle account:

### 1. 🔐 Your Moodle Token

This token gives the agent permission to access your Moodle data via API.

- Visit this page (or ask your admin where to find it):  
  **`https://<your-university-domain>/login/token.php?username=YOUR_USERNAME&password=YOUR_PASSWORD&service=moodle_mobile_app`**
- Copy and save the token value securely.

> Example:  
> `https://hadi.hacettepe.edu.tr/login/token.php?username=myusername&password=MyPassword22&service=moodle_mobile_app`

---

### 2. 👤 Your Moodle User ID

This is the numeric ID linked to your account. After getting your token, visit this page:
> `https://<your-university-domain>/webservice/rest/server.php?wstoken=YOUR_TOKEN&moodlewsrestformat=json&wsfunction=core_webservice_get_site_info`

- You’ll see your User ID in the second line, under "userid".
- Copy and save the value securely.
---

### 3. 🌐 Your Moodle Base URL

This is the root address of your university’s Moodle platform.

> Example:  
> `https://moodle.youruniversity.edu`

You'll need to enter this so the agent knows where to send requests.

---

## 💬 Example Prompts

Once set up, you can chat with your agent like this:

- “What assignments are due next week?”
- “Do I have any quizzes this month?”
- “What courses am I enrolled in?”
- “Can you show my grades in Data Structures?”
- “Any important events this week?”

The agent will fetch real data and help you plan your academic tasks effectively.

---

## 🔐 Security Tips

- **Do not share** your Moodle token with anyone.
- Use secure storage (like environment variables) in production environments.
- Never publish your token in public notebooks or repositories.

---

## ✅ Ready to Go

Once you have your Moodle token, user ID, and base URL, you’re all set!  
Get the agent, connect it to your info, and let it help you stay focused, organized, and academically successful.
