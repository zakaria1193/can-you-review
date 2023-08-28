#!/usr/bin/env python3

import os
import gitlab
import datetime
import argparse
from collections import defaultdict


def find_user_with_most_reviews(url, token, weeks, group_id):
    # Set your GitLab URL and private token
    gitlab_url = url
    private_token = token

    # Calculate the date n weeks ago
    weeks_ago = datetime.datetime.now() - datetime.timedelta(weeks=weeks)

    # Initialize GitLab API client
    print("Initializing GitLab API client")
    gl = gitlab.Gitlab(gitlab_url, private_token=private_token)

    # Get all projects
    print("Getting all mrs...")
    group = gl.groups.get(group_id)
    merge_requests = group.mergerequests.list(all=True, state="opened", updated_after=weeks_ago)
    print("Found {} merge requests".format(len(merge_requests)))

    # Count reviews for each user
    sole_review_count = {}
    multiple_review_count = {}

    def init_dict_if_not_exists(dict, key, value):
        if key not in dict:
            dict[key] = value
        else:
            print("Warning: key {} already exists in dict".format(key))

    print("Going through merge requests:")

    # Count reviews for each user by project
    for mr in merge_requests:
        project_name = gl.projects.get(mr.project_id).name

        # Add subdicts for each user for each project
        reviewers = mr.reviewers

        # Log for debugging
        reviewer_names = [reviewer["username"] for reviewer in reviewers]
        print("Project: {}, MR: {}, Reviewers: {}".format(project_name, mr.title, reviewer_names))

        for reviewer in reviewers:
            username = reviewer["username"]
            init_dict_if_not_exists(sole_review_count, username, {})
            init_dict_if_not_exists(sole_review_count[username], project_name, 0)

            init_dict_if_not_exists(multiple_review_count, username, {})
            init_dict_if_not_exists(multiple_review_count[username], project_name, 0)

        if len(reviewers) == 1:
            sole_review_count[reviewers[0]["username"]][project_name] += 1
        elif len(reviewers) >= 2:
            for reviewer in reviewers:
                multiple_review_count[reviewer["username"]][project_name] += 1

    print("-> Finished going through merge requests")

    # Count reviews for each user across all projects
    all_reviewers = set(sole_review_count.keys()) | set(multiple_review_count.keys())

    for reviewer in all_reviewers:
        # Create a fake project ID for the "all" project
        all_project_name = "all"

        # Initialize dicts if they don't exist
        init_dict_if_not_exists(sole_review_count[reviewer], all_project_name, 0)
        init_dict_if_not_exists(multiple_review_count[reviewer], all_project_name, 0)

        # Sum up the reviews across all projects
        for project_name in sole_review_count[reviewer]:
            if project_name == all_project_name:
                continue
            sole_review_count[reviewer][all_project_name] += \
                sole_review_count[reviewer][project_name]

        for project_name in multiple_review_count[reviewer]:
            if project_name == all_project_name:
                continue
            multiple_review_count[reviewer][all_project_name] += \
                multiple_review_count[reviewer][project_name]


    print(sole_review_count, multiple_review_count)
    return sole_review_count, multiple_review_count


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Find the user with the most reviews in all GitLab projects.')
    parser.add_argument('--url', default=os.environ.get('GITLAB_URL'), help='GitLab URL', required=True)
    parser.add_argument('--token', default=os.environ.get('GITLAB_PRIVATE_TOKEN'), help='Private token', required=True)
    parser.add_argument('--weeks', default=2, type=int, help='Number of weeks to consider for MR activity')
    parser.add_argument('group_id', help='Group ID to consider for MR activity')
    args = parser.parse_args()

    # Call the function with provided arguments
    find_user_with_most_reviews(args.url, args.token, args.weeks, args.group_id)


if __name__ == "__main__":
    main()
