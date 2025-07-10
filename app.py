from flask import Flask, render_template, request, redirect, url_for, session, flash
from cloudant.client import Cloudant
from config import cloudant_config

app = Flask(__name__)
app.secret_key = 'your-secret-key'

client = Cloudant.iam(
    cloudant_config["username"],
    cloudant_config["apikey"],
    url=cloudant_config["url"],
    connect=True
)

db = client.create_database(cloudant_config["dbname"], throw_on_exists=False)

@app.route('/')
def home():
    return redirect(url_for('landing'))

@app.route('/landing')
def landing():
    tasks = [doc for doc in db]
    return render_template('landing.html', tasks=tasks)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    tasks = [doc for doc in db]
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        if not title:
            return "Title is required!", 400
        db.create_document({"title": title, "done": False})
        return redirect(url_for('dashboard'))
    return render_template('add.html')

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_task(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if id not in db:
        return "Task not found!", 404
    doc = db[id]
    if request.method == 'POST':
        doc['title'] = request.form['title']
        doc.save()
        return redirect(url_for('dashboard'))
    return render_template('edit.html', task=doc)

@app.route('/delete/<id>')
def delete_task(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if id in db:
        db[id].delete()
    return redirect(url_for('dashboard'))

@app.route('/done/<id>')
def mark_done(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if id in db:
        doc = db[id]
        doc['done'] = True
        doc.save()
    return redirect(url_for('dashboard'))

@app.route('/pending/<id>')
def mark_pending(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if id in db:
        doc = db[id]
        doc['done'] = False
        doc.save()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)