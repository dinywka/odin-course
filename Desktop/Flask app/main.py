import contextlib
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

@app.route("/", methods=['GET'])
def home():
    search_query = request.args.get('search', '')

    with contextlib.closing(sqlite3.connect("database.db")) as connection:
        connection.execute("""
        CREATE TABLE IF NOT EXISTS store_db
        (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            description TEXT DEFAULT '',
            price INTEGER NOT NULL DEFAULT '',
            count INTEGER NOT NULL DEFAULT ''
        );
        """)

        if search_query:
            rows = connection.execute(
                "SELECT id, title, description, price, count FROM store_db WHERE title LIKE ? ORDER BY id ASC;",
                ('%' + search_query + '%',)
            )
        else:
            rows = connection.execute(
                "SELECT id, title, description, price, count FROM store_db ORDER BY id ASC;"
            )

        products = []
        for record in rows:
            product = {
                "id": record[0],
                "title": record[1],
                "description": record[2][:15:1] + "..." if len(record[2]) > 15 else record[2],
                "price": record[3],
                "count": record[4]
            }
            products.append(product)

        return render_template('pages/home.html', products=products, search_query=search_query)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "GET":
        return render_template('pages/book_create.html')
    elif request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        count = request.form['count']

        with sqlite3.connect('database.db') as connection:
            connection.execute(
                "INSERT INTO store_db (title, description, price, count) VALUES (?, ?, ?, ?);",
                (title, description, price, count)
            )

        return redirect(url_for('home'))

if __name__ == "__main__":
    app.run()
