import re
import subprocess


def get_repo_context():
    try:
        url = (
            subprocess.check_output(["git", "remote", "get-url", "origin"])
            .decode()
            .strip()
        )
        match = re.search(r"github\.com[:/](.+?)/(.+?)(\.git)?$", url)
        return match.groups()[:2] if match else (None, None)
    except subprocess.CalledProcessError:
        return (None, None)


def create_branch(name: str):
    subprocess.run(["git", "checkout", "-b", name], check=True)
