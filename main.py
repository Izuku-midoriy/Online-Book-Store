import os
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Dummy book data
demo_books = [
    {
        'id': 1,
        'title': 'The Great Gatsby',
        'author': 'F. Scott Fitzgerald',
        'price': 10.99,
        'description': 'A story of wealth and love in the Jazz Age',
        'image_url': 'https://m.media-amazon.com/images/I/71FTb9X6wsL._AC_UF1000,1000_QL80_.jpg'
    },
    {
        'id': 2,
        'title': 'To Kill a Mockingbird',
        'author': 'Harper Lee',
        'price': 12.50,
        'description': 'A powerful story of racial injustice',
        'image_url': 'https://m.media-amazon.com/images/I/71FxgtFKcQL._AC_UF1000,1000_QL80_.jpg'
    },
    {
        'id': 3,
        'title': '1984',
        'author': 'George Orwell',
        'price': 9.99,
        'description': 'Dystopian novel about totalitarianism',
        'image_url': 'https://m.media-amazon.com/images/I/71kxa1-0mfL._AC_UF1000,1000_QL80_.jpg'
    }
]

@app.route('/')
def home():
    return render_template('home.html', books=demo_books)

@app.route('/books')
def books():
    return render_template('books.html', books=demo_books)

@app.route('/book/<int:id>')
def book_detail(id):
    book = next((b for b in demo_books if b['id'] == id), None)
    if not book:
        flash('Book not found', 'danger')
        return redirect(url_for('books'))
    return render_template('book_detail.html', book=book)

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        flash('Please login to view your cart', 'warning')
        return redirect(url_for('login'))
    return render_template('cart.html', cart_items=[], total=0)

@app.route('/checkout')
def checkout():
    if 'user_id' not in session:
        flash('Please login to checkout', 'warning')
        return redirect(url_for('login'))
    flash('Order placed successfully!', 'success')
    return redirect(url_for('orders'))

@app.route('/orders')
def orders():
    if 'user_id' not in session:
        flash('Please login to view orders', 'warning')
        return redirect(url_for('login'))
    return render_template('orders.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        flash('Registration is disabled in demo mode.', 'info')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['user_id'] = 1
        session['username'] = username
        flash('Login successful!', 'success')
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
