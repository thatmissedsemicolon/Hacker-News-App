"""
Module to define the database models for the application.
"""

from datetime import datetime
from . import db, app

class Post(db.Model):
    """
    Represents a post in the application.
    """

    __tablename__ = 'posts' # table name
    id = db.Column(db.Integer, primary_key=True)
    by = db.Column(db.String, nullable=True, default='N/A')
    descendants = db.Column(db.Integer, default=0)
    kids = db.Column(db.String, nullable=True)  # Storing as a comma-separated string
    score = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime)
    title = db.Column(db.String, nullable=True)
    type = db.Column(db.String, nullable=True)
    url = db.Column(db.String, nullable=True)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    reactions = db.relationship('UserPostReaction', backref='post', lazy=True)

    @property
    def serialize(self):
        """
        Return object data in easily serializable format.
        """

        return {
            'by': self.by,
            'descendants': self.descendants,
            'id': self.id,
            'kids': self.kids.split(','), 
            'score': self.score,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'title': self.title,
            'type': self.type,
            'url': self.url,  
            'likes': self.likes,
            'dislikes': self.dislikes,
        }

class User(db.Model):
    """
    Represents a user in the application.
    """

    __tablename__ = 'users'  # table name
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False, unique=True)  # set unique=True
    email = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False)

class UserPostReaction(db.Model):
    """
    Represents a user's reaction to a post in the application.
    """

    __tablename__ = 'user_post_reactions'  # table name
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Corrected here
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)  # Corrected here
    reaction = db.Column(db.String(10), nullable=False)

class Backup(db.Model):
    """
    Represents a backup entry in the application.
    """
    __tablename__ = 'backups'  # table name
    id = db.Column(db.Integer, primary_key=True)
    backup_file_path = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables
with app.app_context():
    db.create_all()
