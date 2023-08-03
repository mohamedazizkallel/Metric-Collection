from pydriller import Repository
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import traceback
import schedule
import time

def extract_commits(branch_names, paths, start_date, end_date):
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

def run_script(branch_names, paths, start_date, end_date):
    print("Running data extraction for branches:", branch_names, "and paths:", paths)
    extract_commits(branch_names, paths, start_date, end_date)
    print("Data extraction completed!")

def get_user_input():
    branch_names_str = input("Enter desired branch names (separated by space): ")
    branch_names = branch_names_str.split()

    paths_str = input("Enter repository URLs (separated by space): ")
    paths = paths_str.split()

    end_date_str = input("Enter the end date in YYYY-MM-DD format: ")
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    days_str = input("Enter the number of days for the start date: ")
    years_str = input("Enter the number of years for the start date: ")

    days = int(days_str)
    years = int(years_str)

    start_date = end_date - timedelta(days=days) - relativedelta(years=years)

    return branch_names, paths, start_date, end_date

def main():
    # Get user inputs
    branch_names, paths, start_date, end_date = get_user_input()

    # Run the script immediately
    run_script(branch_names, paths, start_date, end_date)

    # Schedule the script to run every Monday at 3:00 AM
    schedule.every().monday.at("03:00").do(run_script, branch_names, paths, start_date, end_date)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
