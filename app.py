from flask import Flask, render_template, request, redirect, url_for, flash
from data_manager import DataManager
from models import db, User, Movie
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)

# Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "temporary-secret-key-12345")

db.init_app(app)
data_manager = DataManager()


@app.route('/')
def index():
    """Home page showing all users and add user form"""
    users = data_manager.get_all_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def add_user():
    """Add a new user to the database"""
    name = request.form.get('name')

    if name:
        data_manager.create_user(name)

    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def user_movies(user_id):
    """Display all movies for a specific user"""
    user = User.query.get_or_404(user_id)
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """Add a new movie to user's favorite list"""
    user = User.query.get_or_404(user_id)

    name = request.form.get('name')

    if name and name.strip():
        try:
            api_key = os.getenv("OMDB_API_KEY")
            response = requests.get("http://www.omdbapi.com/", params={
                "t": name.strip(),
                "apikey": api_key
            })
            data = response.json()

            if data.get("Response") == "True":
                director = data.get("Director", "")
                year = int(data.get("Year", "0")) if data.get("Year", "").isdigit() else None
                poster_url = data.get("Poster", "")

                data_manager.add_movie(
                    user_id,
                    data.get("Title", name.strip()),
                    director,
                    year,
                    poster_url
                )
                flash(f'Movie "{data.get("Title")}" added successfully!', 'success')
            else:
                flash(f'Could not find movie "{name}" in OMDb.', 'error')

        except Exception as e:
            flash(f'Error adding movie: {str(e)}', 'error')
    else:
        flash('Please provide a movie name', 'error')

    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """Update the title of a specific movie"""
    user = User.query.get_or_404(user_id)
    movie = Movie.query.get_or_404(movie_id)

    # Verify movie belongs to the user
    if movie.user_id != user_id:
        flash('Movie not found for this user', 'error')
        return redirect(url_for('user_movies', user_id=user_id))

    new_title = request.form.get('title')

    if new_title and new_title.strip():
        try:
            data_manager.update_movie(movie_id, new_title.strip())
            flash(f'Movie title updated successfully!', 'success')
        except Exception as e:
            flash(f'Error updating movie: {str(e)}', 'error')
    else:
        flash('Please provide a valid movie title', 'error')

    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Remove a specific movie from user's favorite list"""
    movie = Movie.query.get_or_404(movie_id)

    # Verify movie belongs to the user
    if movie.user_id != user_id:
        flash('Movie not found for this user', 'error')
        return redirect(url_for('user_movies', user_id=user_id))

    try:
        movie_name = movie.name
        data_manager.delete_movie(movie_id)
        flash(f'Movie "{movie_name}" deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting movie: {str(e)}', 'error')

    return redirect(url_for('user_movies', user_id=user_id))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    with app.app_context():
        os.makedirs("data", exist_ok=True)
        db.create_all()

    app.run(debug=True)
