import os
from pathlib import Path

from textual import work
from textual.app import App, ComposeResult
from textual.containers import Center, Vertical
from textual.screen import Screen
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Label,
    ListItem,
    ListView,
    Static,
)

from .api import fetch_issues
from .config import load_token, save_token
from .git_utils import create_branch, get_repo_context
from .models import format_branch_name


class TokenSetupScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Center(
            Vertical(
                Static(" [b]GitHub Token não encontrado[/b]", id="setup-title"),
                Static(
                    "To use this app, you need to set up a [b]Personal Access Token (classic)[/b].\n"
                    "Get one at: [u]github.com/settings/tokens[/u] with the [b]repo[/b] scope.",
                    id="setup-help",
                ),
                Input(
                    placeholder="Paste your token here...",
                    password=True,
                    id="token-input",
                ),
                Button("Save and continue", variant="success", id="save-btn"),
                id="setup-dialog",
            )
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        token_value = self.query_one("#token-input").value
        if token_value:
            save_token(token_value)
            os.environ["GITHUB_TOKEN"] = token_value

            self.app.pop_screen()
            self.app.push_screen(MainScreen())


class IssueItem(ListItem):
    def __init__(self, issue: dict):
        super().__init__()
        self.issue = issue

    def compose(self) -> ComposeResult:
        number = self.issue["number"]
        title = self.issue["title"]
        label = self.issue["labels"][0]["name"] if self.issue["labels"] else "task"
        yield Label(f"[b green]#{number:4}[/b green] | [white]{title[:50]}[/white] ")
        yield Label(
            f"   [dim]tag:[/dim] [magenta]{label}[/magenta]", classes="label-line"
        )


class MainScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Vertical(
            Static(" Open GitHub Issues ", id="title"),
            ListView(id="issue-list"),
            Static("Awaiting command...", id="status-bar"),
            id="main-container",
        )
        yield Footer()

    async def on_mount(self) -> None:
        self.load_issues()

    @work(exclusive=True)
    async def load_issues(self) -> None:
        status = self.query_one("#status-bar")
        list_view = self.query_one("#issue-list")

        owner, repo = get_repo_context()
        if not owner or not repo:
            status.update("Not a git repository or no remote found.")
            return

        status.update(f"Loading issues from {owner}/{repo}...")

        try:
            issues = await fetch_issues(owner, repo)
            if not issues:
                status.update("No open issues found.")
                return

            for issue in issues:
                await list_view.append(IssueItem(issue))

            status.update(
                f"Loaded {len(issues)} issues. Use the arrows to navigate and ENTER to create a branch."
            )
            list_view.focus()

        except Exception as e:
            status.update(f"Error loading issues: {str(e)}")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        issue = event.item.issue

        label = issue["labels"][0]["name"] if issue["labels"] else "task"
        branch_name = format_branch_name(label, issue["number"], issue["title"])

        try:
            create_branch(branch_name)
            self.app.exit(
                message=f"Created and switched to branch [b cyan]{branch_name}[/b cyan] successfully."
            )
        except Exception as e:
            self.query_one("#status-bar").update(
                f"[red]Error creating branch: {str(e)}"
            )


class BranchTUI(App):
    TITLE = "Branch TUI"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh Issues"),
    ]

    CSS_PATH = Path(__file__).parent / "styles.tcss"

    def on_mount(self) -> None:
        token = load_token()
        if not token:
            self.push_screen(TokenSetupScreen())
        else:
            os.environ["GITHUB_TOKEN"] = token
            self.push_screen(MainScreen())

    def action_refresh(self) -> None:
        self.query_one("#issue-list").clear()
        self.query_one(MainScreen).load_issues()


def run():
    app = BranchTUI()
    app.run()
