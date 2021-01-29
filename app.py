from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdjkfnsdjkfnsdfjsdkfnjdfsdnfj' # исправить потом!!!!
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass@localhost/quote_page_db'

db = SQLAlchemy(app)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    im_link = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template('adminpage.html')


if __name__ == '__main__':
    app.run()
