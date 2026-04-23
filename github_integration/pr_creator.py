from github import Github

def create_pr(token, repo_name, content):
    g = Github(token)
    repo = g.get_repo(repo_name)

    branch_name = "ai-generated-pipeline"

    source = repo.get_branch("main")
    repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source.commit.sha)

    repo.create_file(
        "pipeline.py",
        "AI generated pipeline",
        content,
        branch=branch_name
    )

    repo.create_pull(
        title="AI Generated Pipeline",
        body="This PR was created by an AI agent",
        head=branch_name,
        base="main"
    )