from flask import Flask, request, redirect, url_for, send_from_directory
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///best.db'
app.config['UPLOAD_FOLDER'] = 'static/food'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=False)
    password = db.Column(db.String(30), nullable=False, unique=False)
    first_name = db.Column(db.String(30), nullable=True, unique=False)
    last_name = db.Column(db.String(30), nullable=True, unique=False)


class Restaurants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=False)
    poster = db.Column(db.String(300), nullable=True, unique=False)
    info = db.Column(db.String(300), nullable=False, unique=False)
    address = db.Column(db.String(99), nullable=False, unique=False)
    price_level = db.Column(db.String(30), nullable=False, unique=False)
    kitchen_type = db.Column(db.String(99), nullable=False, unique=False)
    happy_hour = db.Column(db.String(99), nullable=False, unique=False)
    style = db.Column(db.String(99), nullable=False, unique=False)
    opening_hours = db.Column(db.String(300), nullable=False, unique=False)
    site = db.Column(db.String(300), nullable=False, unique=False)
    wolt_review = db.Column(db.String(30), nullable=False, unique=False)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def index():
    restaurants = Restaurants.query.all()
    for restaurant in restaurants:
        print(restaurant.poster)
    return render_template('index.html', restaurants=restaurants)


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        u = Users(username=username, password=password)
        db.session.add(u)
        db.session.commit()
        print(username, password)

        return redirect('/')
    else:
        return render_template('login.html')


@app.route('/rest_page/<rest_id>')
def rest(rest_id):
    restaurant = Restaurants.query.get(rest_id)
    return render_template('rest_page.html', restaurant=restaurant)


@app.route('/add_restaurant', methods=["POST", "GET"])
def add_rest():
    if request.method == "POST":
        name = request.form.get('name')
        info = request.form.get('info')
        address = request.form.get('address')
        price_level = request.form.get('price_level')
        kitchen_type = request.form.get('kitchen_type')
        happy_hour = request.form.get('happy_hour')
        style = request.form.get('style')
        opening_hours = request.form.get('opening_hours')
        site = request.form.get('site')
        wolt_review = request.form.get('wolt_review')
        poster = request.files.get('poster')
        if poster:
            filename = secure_filename(poster.filename)
            poster_path = os.path.join('food', filename)
            poster.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            r = Restaurants(name=name, poster=os.path.join(app.config['UPLOAD_FOLDER'], filename), info=info,
                            address=address,
                            price_level=price_level, kitchen_type=kitchen_type, happy_hour=happy_hour,
                            style=style, opening_hours=opening_hours, site=site, wolt_review=wolt_review)
        else:
            r = Restaurants(name=name, info=info, address=address,
                            price_level=price_level, kitchen_type=kitchen_type, happy_hour=happy_hour,
                            style=style, opening_hours=opening_hours, site=site, wolt_review=wolt_review)


        db.session.add(r)
        db.session.commit()

        return redirect('/')
    else:
        return render_template('add_restaurant.html')


if __name__ == '__main__':
    app.run(debug=True)