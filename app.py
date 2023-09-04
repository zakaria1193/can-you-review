from flask import Flask, render_template, jsonify, request
from flask_frozen import Freezer
from gitlab_scrapper import find_user_with_most_reviews_from_env_args, get_reviews_url_for_user_name_and_env_args

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


@app.route('/get_data')
def get_data():
    sole_review_count, multiple_review_count = find_user_with_most_reviews_from_env_args()
    sole_review_data = [
        {"username": username, **projects} for username, projects in sole_review_count.items()
    ]
    multiple_review_data = [
        {"username": username, **projects} for username, projects in multiple_review_count.items()
    ]

    print(sole_review_data)
    print(multiple_review_data)

    project_names = project_names_crawler()

    data = {
        'sole_review_data': sole_review_data,
        'multiple_review_data': multiple_review_data,
        'project_names': project_names
    }

    return jsonify(data)


# /get_user_reviews_url?username=
@app.route('/get_user_reviews_url')
def get_user_reviews_url():
    username = request.args.get('username')
    # return gitlab url for the user's reviews
    url = get_reviews_url_for_user_name_and_env_args(username)
    return jsonify({'url': url})


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
