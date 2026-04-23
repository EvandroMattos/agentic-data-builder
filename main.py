from agent.generator import generate_pipeline
from github.pr_creator import create_pr

prompt = input("Describe your pipeline: ")

code = generate_pipeline(prompt)

with open("pipeline.py", "w") as f:
    f.write(code)

# criar PR
create_pr(
    token="YOUR_GITHUB_TOKEN",
    repo_name="your-user/your-repo",
    content=code
)

print("Pipeline created and PR opened 🚀")