import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
import requests

load_dotenv()

MOVIE_DB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
MOVIE_DB_INFO_URL = "https://api.themoviedb.org/3/movie"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"
MOVIE_DB_API_KEY = os.environ["MOVIE_DB_API_KEY"]

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
Bootstrap(app)

# create db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movie-ranking.db"
app.config['FLASH_MESSAGES'] = True
db = SQLAlchemy(app)


# create table
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)


# create form to edit the rating and review of a movie
class RateMovieForm(FlaskForm):
    rating = StringField(label="Your Rating Out of 10 e.g. 7.5", validators=[DataRequired()])
    review = StringField(label="Your Review", validators=[DataRequired()])
    submit = SubmitField(label="Done")


class AddMovieForm(FlaskForm):
    title = StringField(label="Movie Title", validators=[DataRequired()])
    add_movie_btn = SubmitField(label="Add Movie")


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    # create a list of movies sorted by rating
    all_movies = Movie.query.order_by(Movie.rating).all()
    for i in range(len(all_movies)):
        # Following line gives each movie a new ranking reversed from their order in all_movies
        all_movies[i].ranking = len(all_movies) - i
        db.session.commit()
    return render_template("index.html", movies=all_movies)


# Add movie route
@app.route("/add", methods=["GET", "POST"])
def add_movie():
    add_form = AddMovieForm()
    if add_form.validate_on_submit():
        movie_title = add_form.title.data
        # Search for the movie using the title in the MovieDB API
        response = requests.get(url=MOVIE_DB_SEARCH_URL, params={"api_key": MOVIE_DB_API_KEY, "query": movie_title})
        data = response.json()["results"]
        if not data:
            flash(f"Movie with title {movie_title} not found!", category="error")
            return redirect(url_for("add_movie"))
        return render_template("select.html", options=data)
    return render_template("add.html", form=add_form)


@app.route("/find")
def find_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        movie_api_url = f"{MOVIE_DB_INFO_URL}/{movie_api_id}"
        response = requests.get(movie_api_url, params={"api_key": MOVIE_DB_API_KEY, "language": "en-US"})
        data = response.json()
        existing_movie = Movie.query.filter_by(title=data["title"]).first()
        if existing_movie:
            flash("Movie already exists!", category="danger")
            return redirect(url_for("edit_movie", id=existing_movie.id))
        new_movie = Movie(
            title=data["title"],
            year=data["release_date"].split("-")[0],
            img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
            description=data["overview"]
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for("edit_movie", id=new_movie.id))
    return redirect(url_for("home"))


# Edit movie route
@app.route("/edit", methods=["GET", "POST"])
def edit_movie():
    form = RateMovieForm()
    movie_id = request.args.get("id")
    movie = Movie.query.get(movie_id)  # get the movie that is being edited, by id
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)   # update the rating and the review in the database
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", movie=movie, form=form)


# Delete movie route
@app.route("/delete")
def delete_movie():
    movie_id = request.args.get("id")
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))


@app.errorhandler(404)
def handle_not_found_error(error):
    return render_template("error.html", error="404 - Page Not Found"), 404


@app.errorhandler(500)
def handle_internal_error(error):
    return render_template("error.html", error="500 - Internal Server Error"), 500


if __name__ == '__main__':
    app.run(debug=True)
