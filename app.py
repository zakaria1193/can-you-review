from flask import Flask, render_template
from flask_frozen import Freezer
import json

app = Flask(__name__)
freezer = Freezer(app)

# Sample data
sole_review_count = {
    'jvalverde': {'Wireshark': 1, 'all': 1},
    'Lekensteyn': {'Wireshark': 1, 'all': 1},
    'JaapKeuter': {'Wireshark': 1, 'all': 1},
    'AndersBroman': {'Wireshark': 1, 'all': 1}
}

multiple_review_count = {
    'jvalverde': {'Wireshark': 0, 'all': 0},
    'Lekensteyn': {'Wireshark': 0, 'all': 0},
    'JaapKeuter': {'Wireshark': 0, 'all': 0},
    'AndersBroman': {'Wireshark': 0, 'all': 0}
}

@app.route('/')
def index():
    sole_review_data = json.dumps([
        {"username": username, **projects} for username, projects in sole_review_count.items()
    ])
    
    multiple_review_data = json.dumps([
        {"username": username, **projects} for username, projects in multiple_review_count.items()
    ])
    
    return render_template('index.html', sole_review_data=sole_review_data, multiple_review_data=multiple_review_data)

if __name__ == '__main__':
    app.run(debug=True)
