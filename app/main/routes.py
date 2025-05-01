from flask import render_template, redirect, url_for,request
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.main.forms import PostForm, EmptyForm, EditUsernameForm, EditAboutMeForm, EditProfilePictureForm
from app.models import User, Post
from app.utils import get_page,generate_filename,delete_file
from werkzeug.utils import secure_filename
from datetime import datetime, timezone
from app.errors.handlers import not_found
import os
from config import IMAGES_PATH
from PIL import Image

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.cur.execute("UPDATE users SET last_seen = %s WHERE id = %s;",(current_user.last_seen,current_user.id))
        db.conn.commit()

@bp.route("/", methods=["GET","POST"])
@bp.route("/index", methods=["GET","POST"])
@login_required
def index(): # Página inicial, posts dos usuarios seguidos pelo usuario e input de post 
    form=PostForm()
    if form.validate_on_submit():
        db.cur.execute("INSERT INTO posts(body,user_id) VALUES (%s,%s)",(form.post.data,current_user.id))
        db.conn.commit()
        return redirect(url_for('main.index'))
    offset,page = get_page()
    posts, count = current_user.following_posts(offset)
    if not posts and page != 1:
        return redirect(url_for('main.index',page=1))

    return render_template("index.jinja",title="Home",posts=posts, form=form,page=page,count=count) 

@bp.route("/user/<username>")
@login_required
def user(username):
    result = db.select_user("username",username)
    if result is None:
        return not_found(404)
    user = User(id=result["id"],username=result["username"],email=result["email"],password_hash=result["password"],
                profile_picture=result["profile_picture"],last_seen=result["last_seen"],about_me=result.get("about_me")) if result else None
    if user is None:
        return not_found(404)
    
    offset,page = get_page()
    
    posts = db.cur.execute(f"""SELECT p.id, p.body, p.created_at, p.user_id, 
                            u.username, u.email, u.about_me, u.profile_picture, u.last_seen 
                            FROM posts p INNER JOIN users u ON u.id = p.user_id
                            WHERE u.id = %s ORDER BY p.created_at DESC
                            LIMIT 30 OFFSET {offset};""",(user.id,)).fetchall()
    if not posts and page != 1:
        return redirect(url_for('main.user',page=1,username=username))

    count = db.cur.execute(f"""SELECT 1 FROM posts p INNER JOIN users u ON u.id = p.user_id
                            WHERE u.id = %s LIMIT 30 OFFSET {offset + 30};""",(user.id,)).fetchone()
    if count is not None: #TODO ver esses if-else counts
        count = 1
    else:
        count = 0

    form = EmptyForm()
    return render_template("user.jinja",title=username, user=user,form=form, 
                           posts=posts,page=page,count=count)

@bp.route("/edit_profile", methods=["GET","POST"])
@login_required
def edit_profile():
    form = EmptyForm()
    return render_template("edit_profile.jinja",title="Edit Profile",form=form)

@bp.route("/edit_profile/edit_username", methods=["GET","POST"])
@login_required
def edit_username():
    form = EditUsernameForm(current_user.username)
    if form.validate_on_submit():
        db.cur.execute("""UPDATE users SET username = %s WHERE id = %s;""",(form.username.data,current_user.id))
        return redirect(url_for("main.edit_profile"))
    return render_template("edit_username.jinja",title="Edit username",form=form)

@bp.route("/edit_profile/edit_about_me", methods=["GET","POST"])
@login_required
def edit_about_me():
    form = EditAboutMeForm(current_user.about_me)
    if form.validate_on_submit():
        db.cur.execute("""UPDATE users SET about_me = %s WHERE id = %s;""",(form.about_me.data,current_user.id))
    elif request.method == "GET":
        return render_template("edit_about_me.jinja",title="Edit about me",form=form)
    return redirect(url_for("main.edit_profile"))

@bp.route("/edit_profile/edit_profile_picture", methods=["GET","POST"])
@login_required
def edit_profile_picture():
    form = EditProfilePictureForm()
    if form.validate_on_submit():
        profile_picture = form.profile_picture.data
        img = Image.open(profile_picture)
        img = img.resize((400,400),Image.Resampling.LANCZOS)
        filename = secure_filename(profile_picture.filename)
        filename = generate_filename(filename)
        img.save(os.path.join(IMAGES_PATH,filename))
        old_filename = db.cur.execute("""SELECT profile_picture 
                                      FROM users WHERE id = %s;""",(current_user.id,)).fetchone()
        db.cur.execute("""UPDATE users 
                       SET profile_picture = %s WHERE id = %s;""",(filename,current_user.id))
        if old_filename["profile_picture"] != '7b2666b68102643c39a0c4c2d095515e.png' and \
        old_filename["profile_picture"] != 'd3badb0b2c80449763ef7610bd10915c.jpeg':
            delete_file(old_filename["profile_picture"]) # TODO arthur gere uma imagem padrão e faça uma variavel
    if request.method == "GET":
        return render_template("edit_profile_picture.jinja",title="Edit profile picture",form=form)
    return redirect(url_for("main.edit_profile"))

@bp.route("/follow/<username>", methods=["POST"])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.cur.execute("""SELECT id,username,email,
                              about_me,profile_picture,last_seen 
                              FROM users WHERE username = %s;""",(username,)).fetchone()
        user = User(id=user["id"],username=user["username"],email=["email"],
                    about_me=user["about_me"],profile_picture=user["profile_picture"],last_seen=user["last_seen"],password_hash=None)
        
        if user is None:
            return redirect(url_for("main.index"))

        if user == current_user:
            return redirect(url_for("main.user", username=username))
        
        current_user.follow(user)
        db.conn.commit()
        return redirect(url_for("main.user", username=username))
    else:
        return redirect(url_for("main.index"))
    
@bp.route("/unfollow/<username>", methods=["POST"])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.cur.execute("""SELECT id,username,email,
                              about_me,profile_picture,last_seen 
                              FROM users WHERE username = %s;""",(username,)).fetchone()
        user = User(id=user["id"],username=user["username"],email=["email"],
                    about_me=user["about_me"],profile_picture=user["profile_picture"],last_seen=user["last_seen"],password_hash=None)
        
        if user is None:
            return redirect(url_for("main.index"))
        if user == current_user:
            return redirect(url_for("main.user", username=username))
        
        current_user.unfollow(user)
        db.conn.commit()
        return redirect(url_for("main.user", username=username))
    else:
        return redirect(url_for("main.index"))

@bp.route("/discover")
@login_required
def discover():
    offset, page = get_page()
    posts = db.cur.execute(f"""SELECT p.id, p.body, p.created_at, p.user_id, 
                            u.username, u.email, u.about_me, u.profile_picture, u.last_seen 
                            FROM posts p INNER JOIN users u ON u.id = p.user_id
                            ORDER BY p.created_at DESC
                            LIMIT 30 OFFSET {offset};""").fetchall()
    if not posts:
        return redirect(url_for('main.discover',page=1))
    count = db.cur.execute(f"""SELECT 1 AS "exists" 
                            FROM posts p INNER JOIN users u ON u.id = p.user_id
                            LIMIT 30 OFFSET {offset + 30};""").fetchone()
    if count is not None:
        count = 1
    else:
        count = 0


    return render_template("discover.jinja", title="Discover",page=page,posts=posts,count=count)

@bp.route("/<username>/followers")
@login_required
def followers(username):
    offset, page = get_page()
    user = db.cur.execute("""SELECT id,username,email,
                              about_me,profile_picture,last_seen 
                              FROM users WHERE username = %s;""",(username,)).fetchone()
    user = User(id=user["id"],username=user["username"],email=["email"],
                    about_me=user["about_me"],profile_picture=user["profile_picture"],last_seen=user["last_seen"],password_hash=None)

    followers, count = user.get_followers(offset)
    
    return render_template("followers.jinja",title="Followers",count=count,followers=followers,page=page,username=username)

@bp.route("/<username>/followeds")
@login_required
def followeds(username):
    offset, page = get_page()
    user = db.cur.execute("""SELECT id,username,email,
                              about_me,profile_picture,last_seen 
                              FROM users WHERE username = %s;""",(username,)).fetchone()
    user = User(id=user["id"],username=user["username"],email=["email"],
                    about_me=user["about_me"],profile_picture=user["profile_picture"],last_seen=user["last_seen"],password_hash=None)
    
    followeds, count = user.get_followeds(offset)

    return render_template("followeds.jinja",title="Followeds",page=page,count=count,followeds=followeds,username=username)
