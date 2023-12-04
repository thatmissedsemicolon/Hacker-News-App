"""
Routes module to handle routing logic for the application.
"""

from flask import Blueprint, render_template, request
from middleware.middleware import token_required, token_not_required, verfiy_is_admin
from auth.auth import Auth
from user.user import Users

bp = Blueprint('routes', __name__)

auth = Auth()
user = Users()

@bp.route("/", methods=["GET"])
def home():
    """Render the homepage."""
    response = user.get_news()
    if response:
        return response
    return "Authorization failed", 400


@bp.route("/signin", methods=["GET"])
@token_not_required   # This decorator checks the user does not need to be authenticated.
def signin():
    """Handle the sign-in process."""
    return render_template('signin.html')


@bp.route("/signup", methods=["GET"])
@token_not_required
def signup():
    """Handle the sign-in process."""
    return render_template('signup.html')


@bp.route("/callback", methods=["GET", "POST"])
@token_not_required
def callback():
    """Handle the callback after third-party authentication."""
    response = auth.callback()
    if response:
        return response
    return "Authorization failed", 400


@bp.route("/authorize", methods=["GET", "POST"])
@token_not_required
def authorize_user():
    """Authorize the user."""
    response = auth.authorize_user()
    if response:
        return response
    return "Authorization failed", 400


@bp.route("/logout", methods=["GET", "POST"])
@token_required    # This decorator checks the user needs to be authenticated.
def logout():
    """Handle the logout process."""
    response = auth.logout()
    if response:
        return response
    return "Authorization failed", 400


@bp.route("/profile", methods=["GET"])
@token_required
def get_profile():
    """Retrieve the user profile."""
    response = user.get_profile()
    if response:
        return response
    return "Authorization failed", 400


@bp.route("/updateUser", methods=["POST"])
@token_required
def update_user_role():
    """Update the role of the user."""
    response = user.update_user_role()
    if response:
        return response
    return "Authorization failed", 400


@bp.route("/newsfeed", methods=["GET"])
def get_news_json():
    """Retrieve news in JSON format."""
    response = user.get_news_json()
    if response:
        return response
    return "Authorization failed", 400


@bp.route('/like/<int:post_id>', methods=['POST'])
@token_required
def like_post(post_id):
    """Likes the post"""
    response = user.like_post(post_id)
    if response:
        return response
    return "Authorization failed", 400


@bp.route('/dislike/<int:post_id>', methods=['POST'])
@token_required
def dislike_post(post_id):
    """Dislikes the post"""
    response = user.dislike_post(post_id)
    if response:
        return response
    return "Authorization failed", 400


@bp.route('/admin/newsitems', methods=['GET', 'POST'])
@verfiy_is_admin  # This decorator checks the user is an admin.
def admin_news_items(role):
    """Get all news item for admin and can sort by all, liked, disliked, and unreacted"""
    sort_order = request.form.get('sort_order', 'all')
    response = user.get_news_items(role, sort_order)
    if response:
        return response
    return "Authorization failed", 400


@bp.route('/admin/delete-post/<int:post_id>', methods=['POST'])
@verfiy_is_admin
def admin_delete_post(role, post_id):
    """Delete the post"""
    response = user.delete_post(post_id)
    if response:
        return response
    return "Authorization failed", 400


@bp.route('/admin/edit-post/<int:post_id>', methods=['GET', 'POST'])
@verfiy_is_admin
def admin_edit_post(role, post_id):
    """Edit the post"""
    response = user.edit_post(role, post_id)
    if response:
        return response
    return "Authorization failed", 400


@bp.route('/admin/view-reactions-users/<int:post_id>', methods=['POST'])
@verfiy_is_admin
def admin_view_reactions_users(role, post_id):
    """View reactions and users for a post"""
    response = user.view_reactions_users(role, post_id)
    if response:
        return response
    return "Authorization failed", 400


@bp.route('/admin/remove-user-reaction/<int:post_id>', methods=['POST'])
@verfiy_is_admin
def admin_remove_user_reaction(role, post_id):
    """View reactions and users for a post"""
    email = request.form['email']
    reaction_type = request.form['reaction']
    response = user.remove_user_reaction(email, post_id, reaction_type)
    if response:
        return response
    return "Authorization failed", 400


@bp.route('/admin/view-all-users', methods=['GET'])
@verfiy_is_admin
def admin_view_all_users(role):
    """View all users"""
    response = user.get_all_users(role)
    if response:
        return response
    return "Authorization failed", 400


@bp.route('/admin/delete-user', methods=['POST'])
@verfiy_is_admin
def admin_delete_user(role):
    """View all users"""
    response = user.delete_user(role)
    if response:
        return response
    return "Authorization failed", 400


@bp.route('/admin/backups')
@verfiy_is_admin
def list_backups(role):
    """List all backups"""
    response = user.list_backups(role)
    if response:
        return response
    return "Authorization failed", 400


@bp.route('/admin/create_backup', methods=['POST'])
@verfiy_is_admin
def initiate_backup(role):
    """Initiate backup"""
    response = user.create_backup()
    if response:
        return response
    return "Authorization failed", 400
