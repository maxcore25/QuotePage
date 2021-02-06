from flask import Flask, session, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
import os
import random

# Loading of configurations file
dotenv_path = os.path.join(os.path.dirname(__file__), 'app_config.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


app = Flask(__name__)
# app.debug = True
app.config['CSRF_ENABLED'] = os.getenv('CSRF_ENABLED')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/Projects/QuotePage/QuotePage/memes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')

db = SQLAlchemy(app)

# Models of database


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    im_link = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

# Forms


class PostForm(FlaskForm):
    picture = StringField('Picture url', validators=[DataRequired(message='This input required')])
    description = StringField('Description', validators=[DataRequired(message='This input required')])
    submit = SubmitField('Post')


class MoreButton(FlaskForm):
    submit = SubmitField('More memes')


db.create_all()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    print(session)
    if 'pic_counter' not in session:
        return redirect('/set_s')
    form = MoreButton()
    raw_posts = db.session.query(Post).all()
    posts = [(el.im_link, el.description, el.id) for el in raw_posts]
    res_posts = list(reversed(posts[:session['pic_counter']]))
    if form.validate_on_submit():
        raw_posts = db.session.query(Post).all()
        posts = [(el.im_link, el.description, el.id) for el in raw_posts]
        if session['pic_counter'] <= len(posts):
            session['pic_counter'] += 1
        res_posts = list(reversed(posts[:session['pic_counter']]))
    return render_template('index.html', title='Главная', posts=res_posts, form=form)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = PostForm()
    if form.validate_on_submit():
        picture, description = form.picture.data, form.description.data
        post = Post(im_link=picture, description=description)
        db.session.add(post)
        db.session.commit()
        return redirect('/admin')
    return render_template('adminpage.html', title='Добавление поста', form=form)


@app.route('/set_s', methods=['GET'])
def set_s():
    session['pic_counter'] = 2
    return redirect("/")


if __name__ == '__main__':
    app.run()
