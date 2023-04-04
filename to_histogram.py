#!/usr/bin/env python3

import csv
import json
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import defaultdict
import argparse
import os

def read_csv_data(csv_file):
    data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if row['project_name'] != 'all':
                project_name = row['project_name']
                username = row['username']
                single_review_count = int(row['single_review_count'])
                multiple_review_count = int(row['multiple_review_count'])
                data[project_name][username]['single'] += single_review_count
                data[project_name][username]['multiple'] += multiple_review_count

    return data


def create_review_plot(project_name, project_data, review_type, output_dir):
    sorted_users = sorted(project_data.keys(), key=lambda user: project_data[user]['single'] + project_data[user]['multiple'], reverse=True)

    fig, ax = plt.subplots()
    categories = [username for username in sorted_users]
    counts = [project_data[user][review_type] for user in sorted_users]
    ax.bar(categories, counts)
    ax.set_ylabel(f'Number of {review_type.capitalize()} Reviews')
    ax.set_title(f'{review_type.capitalize()} Review Counts for Project: {project_name}')
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))  # set y-axis to display only integers
    plt.xticks(rotation='vertical')
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, f'{project_name}_{review_type}_review_histogram.png'))
    plt.close(fig)

def create_index_json(output_dir):
    files = [f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]
    histogram_files = [file for file in files if file.endswith('_single_review_histogram.png') or file.endswith('_multiple_review_histogram.png')]

    with open(os.path.join(output_dir, 'index.json'), 'w') as json_file:
        json.dump(histogram_files, json_file)

def create_histogram(csv_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    data = read_csv_data(csv_file)

    for project_name, project_data in data.items():
        create_review_plot(project_name, project_data, 'single', output_dir)
        create_review_plot(project_name, project_data, 'multiple', output_dir)

    create_index_json(output_dir)

def main():
    parser = argparse.ArgumentParser(description='Create histograms from review counts CSV.')

    parser.add_argument('csv_file', help='CSV file to create histogram from')
    parser.add_argument('--output_dir', help='Directory to save histogram to', default='output')
    args = parser.parse_args()

    create_histogram(args.csv_file, args.output_dir)

if __name__ == "__main__":
    main()
