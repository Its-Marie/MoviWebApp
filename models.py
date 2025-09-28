from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ← WICHTIG: Primary Key!
    name = db.Column(db.String(100), nullable=False)

    # Relationship to movies
    movies = db.relationship(
        "Movie", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.name}>"


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ← WICHTIG: Primary Key!
    name = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(100))
    year = db.Column(db.Integer)
    poster_url = db.Column(db.String(500))

    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<Movie {self.name}>"
