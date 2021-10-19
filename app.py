
from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)

class Books(db.Model):
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    authors = db.Column(db.String(255), nullable=False)
    stockQty = db.Column(db.Integer, nullable=False, default=0)
    timesIssued = db.Column(db.Integer, nullable=False, default=0)
    
    

    def __repr__(self):
        return 'Book'+str(self.book_id)

        
class Customer(db.Model):
    __tablename__ = 'customer'
    cust_id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(255), nullable=False)
    debt = db.Column(db.Integer, nullable=False, default=0)
    total_trans = db.Column(db.Integer, nullable=False, default=0)
   
   

    def __repr__(self):
        return 'Customer '+str(self.cust_id)


transactions = db.Table('transactions',
    db.Column('trans_id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('book_id', db.Integer, db.ForeignKey('customer.cust_id')),
    db.Column('cust_id', db.Integer, db.ForeignKey('books.book_id')),
    db.Column('cost', db.Integer)
)


# class Transaction(db.Model):
#     __tablename__ = 'transaction'
#     trans_id = db.Column(db.Integer, primary_key=True,autoincrement = True)
#     cust_id = db.Column(db.Integer, db.ForeignKey('customer.cust_id'))
#     book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
#     cost = db.Column(db.Integer, nullable=False, default=0)
   

#     def __repr__(self):
#         return 'Trans '+str(self.trans_id)

@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def index():
    print(Customer.query.get(1),Books.query.get(1))
    t = transactions.insert().values(cust_id=1,book_id=1,cost=10)
    db.engine.execute(t)
    
    db.session.commit()
    print(db.session.query(transactions).all())
    most_popular=Books.query.order_by(Books.timesIssued).limit(5).all()
    return render_template('index.html',most_popular=most_popular)

@app.route('/books')
def books():
    all_books=Books.query.all()
    return render_template('books.html', all_books=all_books)

@app.route('/add_books', methods=['GET', 'POST'])
def add_books():
    if request.method=='POST':
        book_id=int(request.form['book_id'])
        book_title=request.form['title']
        book_author=request.form['author']
        book_stockQty=request.form['stockQty']
        new_book =Books(book_id=book_id,title=book_title,authors=book_author,stockQty=book_stockQty,timesIssued=0)
        db.session.add(new_book)
        db.session.commit()
        return redirect('/books')

    else:
        return render_template('add_books.html')
    
@app.route('/books/delete/<int:id>')
def delete_book(id):
    book=Books.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect('/books')

@app.route('/issue_book', methods=['GET', 'POST'])
def issue_book():
    if request.method=='POST':
        book_id=int(request.form['book_id'])
        book_title=request.form['title']
        book_author=request.form['author']
        book_stockQty=request.form['stockQty']
        new_book =Books(book_id=book_id,title=book_title,authors=book_author,stockQty=book_stockQty,timesIssued=0)
        db.session.add(new_book)
        db.session.commit()
        return redirect('/issue_book')

    else:
        return render_template('issue_book.html')

@app.route('/return_issue', methods=['GET', 'POST'])
def return_issue():
    if request.method=='POST':
        book_id=int(request.form['book_id'])
        book_title=request.form['title']
        book_author=request.form['author']
        book_stockQty=request.form['stockQty']
        new_book =Books(book_id=book_id,title=book_title,authors=book_author,stockQty=book_stockQty,timesIssued=0)
        db.session.add(new_book)
        db.session.commit()
        return redirect('/return_issue')

    else:
        return render_template('return_issue.html')

@app.route('/customers')
def customers():
    all_customers=Customer.query.all()
    return render_template('customers.html', all_customers=all_customers)

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method=='POST':
        cust_id=int(request.form['cust_id'])
        name=request.form['name']
        new_customer =Customer(cust_id=cust_id,name=name)
        db.session.add(new_customer)
        db.session.commit()
        return redirect('/customers')

    else:
        return render_template('add_customer.html')
    
@app.route('/customers/delete/<int:id>')
def delete_customers(id):
    customer=Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return redirect('/customers')

if __name__ == '__main__':
    try:
        new_book =Books(book_id=1,title="book_title",authors="book_author",stockQty=0,timesIssued=0)
        db.session.add(new_book)
        db.session.commit()
        new_customer =Customer(cust_id=1,name="name")
        db.session.add(new_customer)
        db.session.commit()
    except:
        pass
    app.run(debug=True)