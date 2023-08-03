
from github import Github

# Replace 'token' with your actual personal access token
g = Github('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')

# Now try accessing the repository
# Replace 'username/repository' with the desired repository information
repo = g.get_repo('mohamedazizkallel/Metric-Collection')


# List repository contents - Replace 'path/to/directory' with the directory you want to explore
contents = repo.get_contents('')

for content in contents:
    if content.type == 'file':
        print(f"File: {content.path}")
    elif content.type == 'dir':
        print(f"Directory: {content.path}")

