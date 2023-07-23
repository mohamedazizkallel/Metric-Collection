from pydriller import Repository
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import traceback
import schedule
import time


def process_repositories():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=10) - relativedelta(years=0)

    # Replace this path with your own repository of interest
    paths = ['https://github.com/mohamedazizkallel/Metric-Collection.git',
             'https://github.com/mohamedazizkallel/ArtGallery.git',
             'https://github.com/KrSkander/Pixxeling-Mobile.git']

    branch_name = "main"  # Replace with the desired branch name

    commits = []

    for path in paths:
        try:
            # Clone the repository to a temporary directory
            repo = Repository(path)

            for commit in repo.traverse_commits():
                # Check if the commit is in the desired branch
                if branch_name in commit.branches:
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


# Schedule the script to run every Monday at a specific time (e.g., 3:00 AM)
schedule.every().monday.at("03:00").do(process_repositories)

while True:
    schedule.run_pending()
    time.sleep(1)
