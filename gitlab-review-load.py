#!/usr/bin/env python3

import os
import csv
import gitlab
import datetime
import argparse
from collections import defaultdict

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Find the user with the most reviews in all GitLab projects.')
    parser.add_argument('--url', default=os.environ.get('GITLAB_URL'), help='GitLab URL')
    parser.add_argument('--token', default=os.environ.get('GITLAB_PRIVATE_TOKEN'), help='Private token')
    parser.add_argument('--weeks', default=2, type=int, help='Number of weeks to consider for MR activity')
    parser.add_argument('--output_dir', help='Directory to save csv to', default='public/output')

    args = parser.parse_args()

    if not args.url:
        parser.error("GitLab URL is required")

    if not args.token:
        parser.error("GitLab private token is required")

    # Set your GitLab URL and private token
    gitlab_url = args.url
    private_token = args.token

    # Calculate the date n weeks ago
    weeks_ago = datetime.datetime.now() - datetime.timedelta(weeks=args.weeks)

    # Initialize GitLab API client
    print("Initializing GitLab API client")
    gl = gitlab.Gitlab(gitlab_url, private_token=private_token)
    
    # Get all projects
    print("Getting all projects...")
    projects = gl.projects.list(all=True)
    print("Found {} projects".format(len(projects)))

    # Initialize dictionaries for total review counts
    total_single_review_count = defaultdict(int)
    total_multiple_review_count = defaultdict(int)

    # Create CSV file
    csv_filename = os.path.join(args.output_dir, 'review_counts.csv')
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['project_id', 'project_name', 'username', 'single_review_count', 'multiple_review_count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Iterate through all projects
        for project in projects:
            # Get merge requests
            print("Getting merge requests for project {}".format(project.name))
            try:
                merge_requests = project.mergerequests.list(state="opened", updated_after=weeks_ago)
            except gitlab.exceptions.GitlabError:
                print("Error: Could not get merge requests for project {}".format(project.name))
                continue

            print("Found {} merge requests".format(len(merge_requests)))

            # Count reviews for each user
            single_review_count = defaultdict(int)
            multiple_review_count = defaultdict(int)

            for mr in merge_requests:
                reviewers = mr.reviewers
                if len(reviewers) == 1:
                    single_review_count[reviewers[0]["username"]] += 1
                elif len(reviewers) >= 2:
                    for reviewer in reviewers:
                        multiple_review_count[reviewer["username"]] += 1

            # Write review counts to CSV
            all_reviewers = set(single_review_count.keys()) | set(multiple_review_count.keys())
            for reviewer in all_reviewers:
                writer.writerow({
                    'project_id': project.id,
                    'project_name': project.name,
                    'username': reviewer,
                    'single_review_count': single_review_count[reviewer],
                    'multiple_review_count': multiple_review_count[reviewer]
                })
                total_single_review_count[reviewer] += single_review_count[reviewer]
                total_multiple_review_count[reviewer] += multiple_review_count[reviewer]

        # Write total review counts to CSV
        all_reviewers = set(total_single_review_count.keys()) | set(total_multiple_review_count.keys())
        for reviewer in all_reviewers:
            writer.writerow({
                'project_id': '',
                'project_name': 'all',
                "username": reviewer,
                "single_review_count": total_single_review_count[reviewer],
                "multiple_review_count": total_multiple_review_count[reviewer]
            })

    print("Review counts have been written to review_counts.csv")

if __name__ == "__main__":
    main()
