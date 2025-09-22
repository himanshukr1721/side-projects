from flask import Flask

from models import (
    init_db, 
    insert_url, 
    get_url, 
    get_all_url, 
    increment_count, 
    delete_url_by_code
    )

app = Flask(__name__)

@app.route("/")

def hello_world():
    return 'hello to python'


@app.route("/about")

def about():
    return 'amazing course on pytohon'


if __name__ == '__main__':
    app.run(debug=True)