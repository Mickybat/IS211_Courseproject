from flask import Flask
from flask import render_template
from flask import redirect, url_for
from flask import request
from flask import flash
import sqlite3
from werkzeug.exceptions import abort


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Fa3*)NhM^g)M"nK'


def get_db_connection():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE post_id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts ORDER BY created DESC').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin':
            error = 'Invalid username or password'
        elif request.form['password'] != 'password':
            error = 'Invalid username or password'
        else:
            return redirect('/dashboard')

    return render_template("login.html", error=error)


@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    posts = conn.execute('SELECT post_id, title FROM posts')
    return render_template('dashboard.html', posts=posts)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        if not author:
            flash('Author is required!')
        if not content:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, author, content) VALUES (?, ?, ?)',
                         (title, author, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']

        conn = get_db_connection()
        conn.execute('UPDATE posts SET title = ?, content = ?, author = ?'
                     ' WHERE post_id = ?', (title, content, author, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE post_id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run()