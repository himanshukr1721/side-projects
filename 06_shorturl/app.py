from flask import Flask, request, redirect, render_template, flash
import random
import string
import re

from models import (
    init_db, 
    insert_url, 
    get_url, 
    get_all_url, 
    increment_count, 
    delete_url_by_code
    )

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

init_db()

def generate_short_code(length=6):
    while True:
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        # Check if code already exists
        if not get_url(code):
            return code



@app.route("/", methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        original_url = request.form['urls']
        short_code = generate_short_code()
        insert_url(original_url, short_code)
        return redirect("/")
    
    all_urls = get_all_url()
    return render_template('index.html', all_urls=all_urls)



@app.route('/<short_code>')
def redirect_url(short_code):
    url_data = get_url(short_code)
    if url_data:
        increment_count(short_code)
        return redirect(url_data[1])
    return render_template('404.html'), 404

@app.route('/delete/<short_code>', methods=['POST'])
def delete_url(short_code):
    delete_url_by_code(short_code)
    return redirect("/")

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # default to 5000 for local testing
    app.run(host="0.0.0.0", port=port, debug=True)
