from pydriller import Repository
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import traceback

# Get user inputs for branch names and paths
branch_names_str = input("Enter desired branch names (separated by space): ")
branch_names = branch_names_str.split()

paths_str = input("Enter repository URLs (separated by space): ")
paths = paths_str.split()

# Get user input for end_date
end_date_str = input("Enter the end date in YYYY-MM-DD format: ")
end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

# Get user input for days and years
days_str = input("Enter the number of days for the start date: ")
years_str = input("Enter the number of years for the start date: ")

days = int(days_str)
years = int(years_str)

# Calculate start_date using timedelta and relativedelta
start_date = end_date - timedelta(days=days) - relativedelta(years=years)

commits = []

for path in paths:
    try:
        # Clone the repository to a temporary directory
        repo = Repository(path, since=start_date, to=end_date)

        for commit in repo.traverse_commits():
            # Check if the commit is in any of the desired branches
            if any(branch_name in commit.branches for branch_name in branch_names):
                hash = commit.hash
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
        print('Problem reading repository at ' + path)
        traceback.print_exc()
        continue

# Save it to FileCommits.csv
df_file_commits = pd.DataFrame(commits)
df_file_commits.to_csv('FileCommits.csv')
