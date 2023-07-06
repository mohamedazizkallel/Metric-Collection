from pydriller import Repository
import pandas as pd

# Replace this path with your own repository of interest
path = 'https://github.com/mohamedazizkallel/Metric-Collection.git'
repo = Repository(path)
commits = []

for commit in repo.traverse_commits():
    hash = commit.hash
    try:
        for f in commit.modified_files:
            record = {
                'hash': hash,
                'message': commit.msg,
                'author_name': commit.author.name,
                'author_email': commit.author.email,
                'author_date': commit.author_date,
                'author_tz': commit.author_timezone,
                'committer_name': commit.committer.name,
                'committer_email': commit.committer.email,
                'committer_date': commit.committer_date,
                'committer_tz': commit.committer_timezone,
                'in_main': commit.in_main_branch,
                'is_merge': commit.merge,
                'num_deletes': commit.deletions,
                'num_inserts': commit.insertions,
                'net_lines': commit.insertions - commit.deletions,
                'num_files': commit.files,
                'branches': ', '.join(commit.branches),
                'filename': f.filename,
                'old_path': f.old_path,
                'new_path': f.new_path,
                'project_name': commit.project_name,
                'project_path': commit.project_path,
                'parents': ', '.join(commit.parents),
            }
            # Omitted: modified_files (list), project_path, project_name
            commits.append(record)
    except Exception:
        print('Problem reading commit ' + hash)
        continue

# Save it to FileCommits.csv
df_file_commits = pd.DataFrame(commits)
df_file_commits.to_csv('FileCommits.csv')