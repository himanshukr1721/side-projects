from flask import Flask, request, redirect, render_template, flash, session, url_for
from functools import wraps
import random
import string
import re

from models import (
    init_db, 
    insert_url, 
    get_url, 
    get_all_url, 
    increment_count, 
    delete_url_by_code,
    create_user,
    verify_user
    )

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

init_db()

def is_valid_url(url):
    """Check if the URL is valid"""
    pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return pattern.match(url) is not None

def generate_short_code(length=6):
    while True:
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        # Check if code already exists
        if not get_url(code):
            return code

def login_required(f):
    """Decorator to require login for certain routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function



@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if user is logged in
        if 'user_id' not in session:
            flash('Please login to create short URLs', 'error')
            return redirect(url_for('login'))
        
        original_url = request.form['urls'].strip()
        
        # Validate URL
        if not original_url:
            flash('Please enter a URL', 'error')
            return redirect("/")
        
        # Add https:// if no protocol specified
        if not original_url.startswith(('http://', 'https://')):
            original_url = 'https://' + original_url
        
        if not is_valid_url(original_url):
            flash('Please enter a valid URL', 'error')
            return redirect("/")
        
        try:
            short_code = generate_short_code()
            insert_url(original_url, short_code)
            flash(f'URL shortened successfully! Short code: {short_code}', 'success')
        except Exception as e:
            flash('Error creating short URL. Please try again.', 'error')
        
        return redirect("/")
    
    all_urls = get_all_url()
    is_logged_in = 'user_id' in session
    username = session.get('username', None)
    return render_template('index.html', all_urls=all_urls, is_logged_in=is_logged_in, username=username)



@app.route('/<short_code>')
def redirect_url(short_code):
    url_data = get_url(short_code)
    if url_data:
        increment_count(short_code)
        return redirect(url_data[1])
    return render_template('404.html'), 404

@app.route('/delete/<short_code>', methods=['POST'])
@login_required
def delete_url(short_code):
    delete_url_by_code(short_code)
    flash('URL deleted successfully', 'success')
    return redirect("/")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        if not username or not password:
            flash('Please enter both username and password', 'error')
            return render_template('login.html')
        
        user = verify_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f'Welcome back, {user["username"]}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    # If already logged in, redirect to home
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation
        if not username or not password or not confirm_password:
            flash('All fields are required', 'error')
            return render_template('register.html')
        
        if len(username) < 3:
            flash('Username must be at least 3 characters long', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        # Create user
        if create_user(username, password):
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose another.', 'error')
    
    # If already logged in, redirect to home
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    username = session.get('username', 'User')
    session.clear()
    flash(f'Goodbye, {username}! You have been logged out.', 'success')
    return redirect(url_for('index'))

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # default to 5000 for local testing
    app.run(host="0.0.0.0", port=port, debug=True)
