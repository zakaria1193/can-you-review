#!/usr/bin/env python3

import csv
import matplotlib.pyplot as plt
from collections import defaultdict
import argparse
import os

def create_histogram(csv_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

        for row in reader:
            if row['project_name'] != 'all':
                project_name = row['project_name']
                username = row['username']
                single_review_count = int(row['single_review_count'])
                multiple_review_count = int(row['multiple_review_count'])
                data[project_name][username]['single'] += single_review_count
                data[project_name][username]['multiple'] += multiple_review_count

    for project_name, project_data in data.items():
        # Sort users by total number of MRs in descending order
        sorted_users = sorted(project_data.keys(), key=lambda user: project_data[user]['single'] + project_data[user]['multiple'], reverse=True)

        # Single review plot
        fig_single, ax_single = plt.subplots()
        categories_single = [username for username in sorted_users]
        counts_single = [project_data[user]['single'] for user in sorted_users]
        ax_single.bar(categories_single, counts_single)
        ax_single.set_ylabel('Number of Single Reviews')
        ax_single.set_title(f'Single Review Counts for Project: {project_name}')
        plt.xticks(rotation='vertical')  # Rotate x-axis labels (usernames) vertically
        fig_single.tight_layout()  # Adjust layout to prevent label overlap
        fig_single.savefig(os.path.join(output_dir, f'{project_name}_single_review_histogram.png'))
        plt.close(fig_single)  # Close the single review figure after saving it

        # Multiple review plot
        fig_multiple, ax_multiple = plt.subplots()
        categories_multiple = [username for username in sorted_users]
        counts_multiple = [project_data[user]['multiple'] for user in sorted_users]
        ax_multiple.bar(categories_multiple, counts_multiple)
        ax_multiple.set_ylabel('Number of Multiple Reviews')
        ax_multiple.set_title(f'Multiple Review Counts for Project: {project_name}')
        plt.xticks(rotation='vertical')  # Rotate x-axis labels (usernames) vertically
        fig_multiple.tight_layout()  # Adjust layout to prevent label overlap
        fig_multiple.savefig(os.path.join(output_dir, f'{project_name}_multiple_review_histogram.png'))
        plt.close(fig_multiple)  # Close the multiple review figure after saving it


def main():
    parser = argparse.ArgumentParser(description='Create histograms from review counts CSV.')

    parser.add_argument('csv_file', help='CSV file to create histogram from')
    parser.add_argument('--output_dir', help='Directory to save histogram to', default='output_histograms')
    args = parser.parse_args()

    create_histogram(args.csv_file, args.output_dir)

if __name__ == "__main__":
    main()
