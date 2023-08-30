from flask import Flask, render_template
from flask_frozen import Freezer
import json
from gitlab_scrapper import find_user_with_most_reviews_from_env_args

app = Flask(__name__)
freezer = Freezer(app)

# Sample data
sole_review_count = {
    'jvalverde': {'Wireshark': 1, 'all': 1},
    'Lekensteyn': {'Wireshark': 1, 'all': 3},
    'JaapKeuter': {'Wireshark': 1, 'all': 1},
    'AndersBroman': {'Wireshark': 1, 'all': 1}
}

multiple_review_count = {
    'jvalverde': {'Wireshark': 0, 'all': 0},
    'Lekensteyn': {'Wireshark': 1, 'all': 3},
    'JaapKeuter': {'Wireshark': 0, 'all': 0},
    'AndersBroman': {'Wireshark': 0, 'all': 0}
}


def project_names_crawler():
    project_names = []
    for project in sole_review_count.values():
        for project_name in project.keys():
            if project_name not in ['all']:
                project_names.append(project_name)

    for project in multiple_review_count.values():
        for project_name in project.keys():
            if project_name not in ['all']:
                project_names.append(project_name)

    return list(set(project_names))


@app.route('/')
def index():
    # Print to dom loading screen
    print("Loading data from Gitlab...")

    sole_review_count, multiple_review_count = find_user_with_most_reviews_from_env_args()

    sole_review_data = json.dumps([
        {"username": username, **projects} for username, projects in sole_review_count.items()
    ])

    print(sole_review_data)

    multiple_review_data = json.dumps([
        {"username": username, **projects} for username, projects in multiple_review_count.items()
    ])

    project_names = project_names_crawler()

    return render_template('index.html', sole_review_data=sole_review_data,
                           multiple_review_data=multiple_review_data, project_names=project_names)


if __name__ == '__main__':
    app.run(debug=True)
