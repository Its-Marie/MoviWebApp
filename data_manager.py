from models import db, User, Movie
import requests
import os

class DataManager():
    """
    Data Manager class to handle CRUD operations for Users and Movies
    """

    # CRUD Operations
    def create_user(self, name):
        """Create a new user"""
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_all_users(self):
        return User.query.all()

    def get_user_movies(self, user_id):
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, user_id, name, director, year, poster_url):
        new_movie = Movie(
            name=name,
            director=director,
            year=year,
            poster_url=poster_url,
            user_id=user_id
        )
        db.session.add(new_movie)
        db.session.commit()
        return new_movie

    def update_movie(self, movie_id, new_title):
        """Update the details of a specific movie in the database"""
        movie = Movie.query.get(movie_id)
        if movie:
            movie.name = new_title
            db.session.commit()
            return movie
        return None

    def delete_movie(self, movie_id):
        """Delete a movie from the database"""
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return True
        return False

