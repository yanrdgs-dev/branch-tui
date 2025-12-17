# Branch TUI

A lightweight Terminal User Interface (TUI) for managing GitHub issues and automating semantic branch creation.

## Features

- **Live Issue Browsing:** List open issues from your current repository directly in the terminal.
- **Semantic Branching:** Automatically generates branch names based on issue labels and titles (e.g., `feat/42-new-login-system`).
- **Secure Persistence:** Guided setup for GitHub Personal Access Tokens (PAT) with secure local storage.
- **Async Performance:** Built with modern Python using `httpx` for API calls and `Textual` for a fluid UI.

## Installation

This project is optimized for [uv](https://github.com/astral-sh/uv), the fastest Python package manager.

### 1. Global Installation

To use the `branch-tui` command anywhere on your system:

```bash
# Clone the repository
git clone https://github.com/yanrdgs-dev/branch-tui.git
cd branch-tui

# Install the tool globally via uv
uv tool install .
```

### 2. Initial Setup

When starting the TUI for the first time, the app will ask for a **GitHub Personal Access Token (PAT)**.

1. Go to [GitHub Settings > Tokens](http://github.com/settings/tokens/).
2. Create a **Classic Token** with `repo` scope.
3. Paste it into the TUI. Your token is saved securely at `~/.branch-tui-config/

## Usage

Navigate to any local Git repository in your terminal and run:

```bash
branch_tui
```

## Keybinds

|  Key   |                Action                 |
| :----: | :-----------------------------------: |
| Arrows |    Navigate through the issue list    |
| Enter  | Create a semantic branch and checkout |
|   R    |        Refresh the issues list        |
|   Q    |         Quit the application          |
