GitHub PR Analysis MCP Server

This project implements a Model Context Protocol (MCP) server that analyzes GitHub Pull Requests and optionally creates a structured Notion page with the analysis results.
It is designed to be used locally with Claude CLI using the stdio MCP transport.

🚀 Features:
Analyze GitHub Pull Requests using GitHub API
Extract PR metadata, commits, files, and code changes
Generate structured AI-based PR analysis
Optionally create a Notion page with the analysis
Runs locally via MCP stdio
Integrates seamlessly with Claude CLI

🧠 Architecture Overview:
Claude CLI
   │
   │ (MCP stdio)
   ▼
MCP Server (Python)
   ├── GitHub API (PR data)
   ├── AI Analysis Logic
   └── Notion API (Page creation)

📁 Project Structure:
MCP-STDIO/
├── pr_analyzer.py        # MCP server entry point
├── github_integration.py # GitHub PR fetching logic
├── requirements.txt      # Python dependencies
└── .venv/                # Virtual environment

🔑 Required Environment Variables:

The application relies on the following environment variables:

Variable	Description
GITHUB_TOKEN	GitHub Personal Access Token
NOTION_API_KEY	Notion integration secret
NOTION_PAGE_ID	Parent Notion page ID

🔐 How to Create GITHUB_TOKEN:
Go to 👉 https://github.com/settings/tokens

Click Generate new token (classic)
Select scopes:
✅ repo
✅ read:user
Generate token and copy it


🧾 How to Create NOTION_API_KEY:
Go to 👉 https://www.notion.so/my-integrations

Click New integration
Name it (e.g. PR Analyzer)
Select your workspace
Copy the Internal Integration Secret


📄 How to Create NOTION_PAGE_ID:
Create a page in Notion (this will be the parent page)
Share the page with your integration:
Click Share
Invite your integration
Copy the page URL:

https://www.notion.so/AI-PR_ANALYSIS-2*************************


Extract the page ID (last 32 characters):
2***********************

📦 Dependencies (requirements.txt):
Package	           Purpose
requests	    Communicates with GitHub & Notion REST APIs
python-dotenv	Loads environment variables from .env
fastmcp	        MCP server framework

🛠 Setup Instructions:
1️⃣ Create Virtual Environment
cd MCP-STDIO
python -m venv .venv
source .venv/bin/activate

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Verify Server Runs Manually
.venv/bin/python pr_analyzer.py


✅ This should start the MCP server without errors.

🤖 Using the MCP Server with Claude CLI
1️⃣ Ensure Claude CLI is Installed
claude --version


Expected output:

2.x.x (Claude Code)

2️⃣ Configure MCP Server (~/.claude.json)
{
  "mcpServers": {
    "github_pr_analysis": {
      "type": "stdio",
      "command": "full path of your .venv/bin/python ",
      "args": ["pr_analyzer.py"],
      "cwd": "full path of your pr_analyzer.py"
    }
  }
}

⚠️ Make sure:
command points to the virtualenv python
cwd is the folder containing pr_analyzer.py

3️⃣ Restart Claude CLI
claude
4️⃣ Verify MCP Server is Connected
Inside Claude CLI:
/mcp
You should see:
github_pr_analysis · ✔ connected
🧪 Example Usage in Claude
Analyze this PR:
https://github.com/org/repo/pull/123


Claude will:
Fetch PR details
Perform analysis

Ask:
“Would you like me to create a Notion page for this analysis?”

Reply with:
yes → creates Notion page
no → skips creation

🐞 Debugging Tips
Add logs in MCP server:
print("Debug message", file=sys.stderr)

Check Claude MCP logs:
claude --debug

Verify paths:
pwd
ls pr_analyzer.py

✅ Summary
MCP server runs locally via stdio
Claude CLI acts as the client
GitHub PRs are analyzed automatically
Notion pages are created on user confirmation
Secure via environment variables


 children=[{
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": content}
                            }]
                        }
                    }]