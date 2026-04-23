from github import Github
import os
import time

def create_pr(file_content: str):
    g = Github(os.getenv("GITHUB_TOKEN"))
    repo = g.get_repo(os.getenv("GITHUB_REPO"))

    timestamp = int(time.time())
    branch_name = f"ai-pipeline-{timestamp}"

    source = repo.get_branch("main")

    repo.create_git_ref(
        ref=f"refs/heads/{branch_name}",
        sha=source.commit.sha
    )

    file_path = f"pipelines/pipeline_{timestamp}.py"

    repo.create_file(
        path=file_path,
        message="🚀 AI generated pipeline",
        content=file_content,
        branch=branch_name
    )

    pr = repo.create_pull(
        title="🚀 AI Generated Pipeline",
        body=f"Generated automatically.\n\nFile: {file_path}",
        head=branch_name,
        base="main"
    )

    return pr.html_url