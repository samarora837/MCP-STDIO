import sys
import os
import traceback
from typing import Any, Dict
from mcp.server.fastmcp import FastMCP
from github_integration import fetch_pr_changes
from notion_client import Client
from dotenv import load_dotenv

print(f"[MCP LOG] Current cwd: {os.getcwd()}", file=sys.stderr)
print(f"[MCP LOG] File exists: {os.path.exists('pr_analyzer.py')}", file=sys.stderr)

class PRAnalyzer:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        self.notion_api_key = os.getenv("NOTION_API_KEY")
        self.notion_page_id = os.getenv("NOTION_PAGE_ID")

        # Initialize MCP Server
        self.mcp = FastMCP("github_pr_analysis")
        print("MCP Server initialized...", file=sys.stderr)


        # Initialize Notion client
        self._init_notion()

        # Register MCP tools
        self._register_tools()

    def split_text(self, text: str, max_length: int = 2000):
        return [text[i:i + max_length] for i in range(0, len(text), max_length)]

    def _init_notion(self):
        """Initialize the Notion client with API key and page ID."""
        try:
            if not self.notion_api_key or not self.notion_page_id:
                raise ValueError("Missing Notion API key or page ID in environment variables")

            self.notion = Client(auth=self.notion_api_key)
            print(f"Notion client initialized successfully", file=sys.stderr)
            print(f"Using Notion page ID: {self.notion_page_id}", file=sys.stderr)
        except Exception as e:
            print(f"Error initializing Notion client: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            sys.exit(1)

    def _register_tools(self):
        """Register MCP tools for PR analysis."""

        @self.mcp.tool()
        async def fetch_pr(repo_owner: str, repo_name: str, pr_number: int) -> Dict[str, Any]:
            """Fetch changes from a GitHub pull request."""
            print(f"Fetching PR #{pr_number} from {repo_owner}/{repo_name}", file=sys.stderr)
            try:
                pr_info = fetch_pr_changes(repo_owner, repo_name, pr_number)
                if pr_info is None:
                    print("No changes returned from fetch_pr_changes", file=sys.stderr)
                    return {}
                print(f"Successfully fetched PR information", file=sys.stderr)
                return {
                    "content": (
                        f"{pr_info}\n\n"
                        "📄 **Would you like me to create a Notion page for this analysis?**\n"
                        "Reply with **yes** or **no**."
                    )
                }
                #return pr_info
            except Exception as e:
                print(f"Error fetching PR: {str(e)}", file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
                return {}

        @self.mcp.tool()
        async def create_notion_page(title: str, content: str) -> str:
            """Create a Notion page with PR analysis."""
            print(f"Creating Notion page: {title}", file=sys.stderr)
            print("content:", type(content))

            try:
                analysis_chunks = self.split_text(content)
                children = []
                for chunk in analysis_chunks:
                    children.append({
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": chunk}
                            }]
                        }
                    })
                print(f"Creating {len(children)} blocks")
                print("children type:", type(children))
                print("children length:", len(children))
                self.notion.pages.create(
                    parent={"type": "page_id", "page_id": self.notion_page_id},
                    properties={"title": {"title": [{"text": {"content": title}}]}},
                    children=children
                )
                print(f"Notion page '{title}' created successfully!", file=sys.stderr)
                return f"Notion page '{title}' created successfully!"
            except Exception as e:
                error_msg = f"Error creating Notion page: {str(e)}"
                print(error_msg, file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
                return error_msg

    def run(self):
        """Start the MCP server."""
        try:
            print("Running MCP Server for GitHub PR Analysis...", file=sys.stderr)
            self.mcp.run(transport="stdio")
        except Exception as e:
            print(f"Fatal Error in MCP Server: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    analyzer = PRAnalyzer()
    analyzer.run()