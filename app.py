from flask import Flask, render_template, request, redirect, url_for, session
import json
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session management

# Load diary entries
if os.path.exists('diary_entries.json'):
    with open('diary_entries.json', 'r') as f:
        diary_entries = json.load(f)
        # To ensure that every entry has a date
        for entry in diary_entries:
            entry.setdefault('date', '1970-01-01 00:00:00') # Assign a default date if not provided
else:
    diary_entries = []

# Save entries back to file
def save_entries():
    with open('diary_entries.json', 'w') as f:
        json.dump(diary_entries, f, indent=4)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/project')
def project():
    return render_template('project.html')

# Public Diary Page
@app.route('/diary')
def diary():
    return render_template('diary.html', entries=diary_entries)

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == "maria":  # Replace with a strong password
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error="Invalid password. Please try again.")
    return render_template('login.html')

# Admin Page
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))

    global diary_entries

    if request.method == 'POST':
        # Handle adding, editing, or deleting entries
        if 'add' in request.form:
            title = request.form['title']
            content = request.form['content']
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry = {
                "id": len(diary_entries) + 1,
                "title": title,
                "content": content,
                "date": date
            }
            diary_entries.append(entry)
            diary_entries.sort(key=lambda x: x.get('date', '1970-01-01 00:00:00'), reverse=True)
            save_entries()

        elif 'edit_id' in request.form:
            entry_id = int(request.form['edit_id'])
            entry = next((e for e in diary_entries if e['id'] == entry_id), None)
            if entry:
                entry['title'] = request.form['title']
                entry['content'] = request.form['content']
                save_entries()

        elif 'delete_id' in request.form:
            entry_id = int(request.form['delete_id'])
            diary_entries = [e for e in diary_entries if e['id'] != entry_id]
            save_entries()

        return redirect(url_for('admin'))

    return render_template('admin.html', entries=diary_entries)

# Logout Route
@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
