"""
Module to handle user-related operations.
"""

from datetime import datetime
import os
import json
import shutil
import requests

from flask import jsonify, redirect, url_for, request, session, render_template, Response
from sqlalchemy import desc, case
from database.models import Post, UserPostReaction, User, Backup
from . import app, db

class Users:
    """
    Class to handle operations related to users.
    """

    def __init__(self):
        pass

    def fetch_news(self):
        """
        Fetch news items.
        """
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            post_ids = response.json()

            for post_id in post_ids[:10]:
                # Check if post already exists in the database
                existing_post = Post.query.get(post_id)
                if existing_post:
                    continue  # Skip to the next iteration if post already exists

                post_url = f"https://hacker-news.firebaseio.com/v0/item/{post_id}.json"
                post_response = requests.get(post_url, timeout=10)

                if post_response.status_code == 200:
                    post_data = post_response.json()
                    post = Post(
                        id=post_data['id'],
                        by=post_data.get('by', 'N/A'),
                        descendants=post_data.get('descendants', 0),
                        kids=','.join(map(str, post_data.get('kids', []))),
                        score=post_data.get('score', 0),
                        timestamp=datetime.fromtimestamp(post_data['time']),
                        title=post_data.get('title', ''),
                        type=post_data.get('type', 'N/A'),
                        url=post_data.get('url')
                    )
                    db.session.add(post)
            db.session.commit()

    def extract_keywords(self, title):
        """Extract keywords from a title by removing common stop words."""
        # List of common stop words, expand as needed
        stop_words = ["the", "of", "and", "in", "a", "to", "is", "with", "as", "for", "on", "by"]
        # Splitting the title by spaces and filtering out stop words
        keywords = [word for word in title.split() if word.lower() not in stop_words]

        return ", ".join(keywords)

    def add_user_if_not_exists(self, user_info):
        """
        Add a user if they don't exist in the database.
        """
        user_id = user_info.get('sub')
        email = user_info.get('email')
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            user = User(user_id=user_id, email=email, role='user')
            db.session.add(user)
            db.session.commit()

    def get_profile(self):
        """
        Fetch the profile of the user.
        """
        user_info = session["user"].get("userinfo")
        user_id = user_info.get('sub')
        user = User.query.filter_by(user_id=user_id).first()
        return render_template('profile.html', user_role=user.role, session=session.get("user"))

    def update_user_role(self):
        """
        Update the role of the user.
        """
        user_info = session["user"].get("userinfo")
        user_id = user_info.get('sub')
        user = User.query.filter_by(user_id=user_id).first()
        user.role = request.form.get('role')
        db.session.commit()
        return redirect(url_for('routes.get_profile'))

    def get_news_json(self):
        """
        Fetch the news in JSON format.
        """
        posts = Post.query.order_by(
            desc(
                case((Post.likes is None, 0), else_=Post.likes) +
                case((Post.dislikes is None, 0), else_=Post.dislikes)
            ),
            desc(Post.timestamp),
        ).limit(30).all()

        post_dicts = [post.serialize for post in posts]

        response = Response(
            response=json.dumps({"news_items": post_dicts}, indent=2),
            content_type='application/json',
            status=200
        )
        return response

    def get_news(self):
        """
        Fetch the news for the user.
        """
        page = request.args.get('page', 1, type=int)
        posts = Post.query.order_by(
            desc(
                case((Post.likes is None, 0), else_=Post.likes) +
                case((Post.dislikes is None, 0), else_=Post.dislikes)
            ),
            desc(Post.timestamp),
        ).paginate(page=page, per_page=5)

        user_info, user_role = None, "guest"
        if "user" in session:
            user_info = session["user"].get("userinfo")
            if user_info:
                user_id = user_info.get('sub')
                user = User.query.filter_by(user_id=user_id).first()
                if user:
                    user_role = user.role

        return render_template('newsfeed.html', user_role=user_role, posts=posts, session=user_info)

    def like_post(self, post_id):
        """
        Allow the user to like a post.
        """
        email = session["user"].get("userinfo").get("email")
        user = User.query.filter_by(email=email).first()

        if not user:
            return redirect(url_for('routes.home'))

        existing_reaction = (UserPostReaction.query
                            .filter_by(user_id=user.id, post_id=post_id)
                            .first())
        post = Post.query.get_or_404(post_id)
        if existing_reaction:
            if existing_reaction.reaction != 'like':
                existing_reaction.reaction = 'like'
                post.likes += 1
                post.dislikes -= 1
                db.session.commit()
        else:
            post.likes += 1
            new_reaction = UserPostReaction(user_id=user.id, post_id=post_id, reaction='like')
            db.session.add(new_reaction)
            db.session.commit()

        return redirect(request.referrer or url_for('routes.home'))

    def dislike_post(self, post_id):
        """
        Allow the user to dislike a post.
        """
        email = session["user"].get("userinfo").get("email")
        user = User.query.filter_by(email=email).first()

        if not user:
            return redirect(url_for('routes.home'))

        existing_reaction = (UserPostReaction.query
                            .filter_by(user_id=user.id, post_id=post_id)
                            .first())

        post = Post.query.get_or_404(post_id)
        if existing_reaction:
            if existing_reaction.reaction != 'dislike':
                existing_reaction.reaction = 'dislike'
                post.dislikes += 1
                post.likes -= 1
                db.session.commit()
        else:
            post.dislikes += 1
            new_reaction = UserPostReaction(user_id=user.id, post_id=post_id, reaction='dislike')
            db.session.add(new_reaction)
            db.session.commit()

        return redirect(request.referrer or url_for('routes.home'))

    def verfiy_is_admin(self, role):
        """
        Verify if a user is an admin.
        """
        return render_template('admin.html', user_role=role, session=session.get("user"))

    def get_news_items(self, role, sort_order='all'):
        """
        Get news items for the admin.
        """
        page = request.args.get('page', 1, type=int)
        query = Post.query
        if sort_order == "liked":
            query = query.filter(Post.likes != 0)
        elif sort_order == "disliked":
            query = query.filter(Post.dislikes != 0)
        posts = query.order_by(
            desc(
                case((Post.likes is None, 0), else_=Post.likes) +
                case((Post.dislikes is None, 0), else_=Post.dislikes)
            ),
            desc(Post.timestamp),
        ).paginate(page=page, per_page=5)

        for post in posts.items:
            post.keywords = self.extract_keywords(post.title)

        return render_template(
            'admin.html', user_role=role, 
            posts=posts, session=session.get("user")
        )

    def delete_post(self, post_id):
        """
        Allow the admin to delete a post.
        """
        post = Post.query.get_or_404(post_id)
        UserPostReaction.query.filter_by(post_id=post_id).delete()
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('routes.admin_news_items'))

    def edit_post(self, role, post_id):
        """
        Allow the admin to edit a post.
        """
        post = Post.query.get_or_404(post_id)
        if request.method == 'POST':
            post.title = request.form['title']
            post.type = request.form['type']
            post.by = request.form['by']
            post.score = request.form['score']
            post.url = request.form['url']
            db.session.commit()
            return redirect(url_for('routes.admin_news_items'))
        return render_template('admin.html', post=post, user_role=role, session=session.get("user"))

    def view_reactions_users(self, role, post_id):
        """
        View users who reacted to a post.
        """
        reactions = UserPostReaction.query.filter_by(post_id=post_id).all()
        user_ids = [reaction.user_id for reaction in reactions]
        reaction_types = {reaction.user_id: reaction.reaction for reaction in reactions}
        liked_users = User.query.filter(User.id.in_(user_ids)).all()
        user_reactions = [(user.email, reaction_types[user.id]) for user in liked_users]
        return render_template(
            'admin.html', users=user_reactions, post_id=post_id,
            user_role=role, session=session.get("user")
        )

    def remove_user_reaction(self, email, post_id, reaction_type):
        """
        Remove a user's reaction (like or dislike) from a post.
        """

        user = User.query.filter_by(email=email).first()

        post = Post.query.filter_by(id=post_id).first()

        reaction = UserPostReaction.query.filter_by(
            user_id=user.id, post_id=post.id, reaction=reaction_type
        ).first()

        if reaction_type == 'like':
            post.likes = post.likes - 1 if post.likes > 0 else 0
        elif reaction_type == 'dislike':
            post.dislikes = post.dislikes - 1 if post.dislikes > 0 else 0

        db.session.delete(reaction)
        db.session.commit()

        return redirect(url_for('routes.admin_news_items'))

    def create_backup(self):
        """
        Create a backup of the database.
        """
        backup_filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        backup_path = os.path.join(os.environ.get("SQL_BACKUP_DIR"), backup_filename)
        shutil.copyfile(f'{os.environ.get("SQL_DIR")}/test.db', backup_path)
        backup_record = Backup(backup_file_path=backup_path)
        db.session.add(backup_record)
        db.session.commit()
        return redirect(url_for('routes.list_backups'))

    def list_backups(self, role):
        """
        List all backups for the admin.
        """
        page = request.args.get('page', 1, type=int)

        backups = Backup.query.order_by(
            Backup.id
        ).paginate(page=page, per_page=5)

        return render_template(
            'admin.html', backups=backups, 
            user_role=role, session=session.get("user")
        )

    def has_user_liked_post(self, email, post_id):
        """
        Checks if user has like the post.
        """

        user = User.query.filter_by(email=email).first()

        post = Post.query.filter_by(id=post_id).first()

        reaction = UserPostReaction.query.filter_by(
            user_id=user.id, post_id=post.id, reaction='like'
        ).first()

        return reaction is not None

    def has_user_disliked_post(self, email, post_id):
        """
        Checks if user has dislike the post.
        """

        user = User.query.filter_by(email=email).first()

        post = Post.query.filter_by(id=post_id).first()

        reaction = UserPostReaction.query.filter_by(
            user_id=user.id, post_id=post.id, reaction='dislike'
        ).first()

        return reaction is not None

    def get_all_users(self, role):
        """
        View all users.
        """
        page = request.args.get('page', 1, type=int)
        users = User.query.paginate(page=page, per_page=5)
        return render_template(
            'admin.html', users=users, 
            user_role=role, session=session.get("user")
        )

    def delete_user(self, role):
        """
        Delete a user.
        """
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        user_reactions = UserPostReaction.query.filter_by(user_id=user.id).all()

        for reaction in user_reactions:
            post = Post.query.get(reaction.post_id)
            if post:
                if reaction.reaction == 'like' and post.likes > 0:
                    post.likes -= 1
                elif reaction.reaction == 'dislike' and post.dislikes > 0:
                    post.dislikes -= 1
                db.session.add(post)

        UserPostReaction.query.filter_by(user_id=user.id).delete()
        db.session.delete(user)
        db.session.commit()

        if session["user"].get("userinfo").get("email") == email:
            return redirect(url_for('routes.logout'))
        return redirect(url_for('routes.admin_view_all_users'))

    def backup_database(self):
        """
        Create a backup of the database.
        """
        backup_filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        backup_path = os.path.join(os.environ.get("SQL_BACKUP_DIR"), backup_filename)
        shutil.copyfile(f'{os.environ.get("SQL_DIR")}/test.db', backup_path)
        backup_record = Backup(backup_file_path=backup_path)
        db.session.add(backup_record)
        db.session.commit()
