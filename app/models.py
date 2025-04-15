from app import login,db
from flask_login import UserMixin
from werkzeug.security import check_password_hash,generate_password_hash

class User(UserMixin):
    id:int
    username:str
    email:str
    password_hash:str
    about_me:str | None
    profile_picture:str
    last_seen:str

    def __init__(self,id,username: str, email: str,password_hash: str | None,about_me: str, profile_picture: str,last_seen):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.about_me = about_me
        self.profile_picture = profile_picture
        self.last_seen = last_seen

    def set_password(self,password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password: str):
        return check_password_hash(self.password_hash, password)
    
    def get_followers(self, offset):
        result = db.cur.execute(f"""SELECT u.id,u.username,u.profile_picture FROM followers f 
                                INNER JOIN users u ON f.follower_id = u.id 
                                WHERE followed_id = %s LIMIT 30
                                OFFSET {offset};""",(self.id,)).fetchall()
        
        count = db.cur.execute(f"""SELECT 1 as "exists" FROM followers f 
                                INNER JOIN users u ON f.follower_id = u.id 
                                WHERE followed_id = %s LIMIT 30
                                OFFSET {offset + 30};""",(self.id,)).fetchone()
        if count is not None:
            count = count["exists"]
        else:
            count = 0
        
        return result, count
    
    def get_followeds(self, offset):
        result = db.cur.execute(f"""SELECT u.id,u.username,u.profile_picture FROM followers f 
                                INNER JOIN users u ON f.followed_id = u.id 
                                WHERE follower_id = %s LIMIT 30
                                OFFSET {offset} ;""",(self.id,)).fetchall()

        count = db.cur.execute(f"""SELECT 1 AS "exists" FROM followers f 
                                INNER JOIN users u ON f.followed_id = u.id 
                                WHERE follower_id = %s LIMIT 30
                                OFFSET {offset + 30} ;""",(self.id,)).fetchone()
        
        if count is not None:
            count = count["exists"]
        else:
            count = 0
        
        return result, count
    
    def follow(self,user):
        if not self.is_following(user):
            db.cur.execute("INSERT INTO followers(follower_id,followed_id) VALUES (%s,%s);",
                           (self.id,user.id))

    def unfollow(self,user):
        if self.is_following(user):
            db.cur.execute("DELETE FROM followers WHERE follower_id = %s AND followed_id = %s;",
                           (self.id,user.id))

    def followers_count(self):
        result = db.cur.execute("SELECT COUNT(1) FROM followers WHERE followed_id = %s;",
                                (self.id,)).fetchone()
        return result["count"]
    
    def followed_count(self):
        result = db.cur.execute("SELECT COUNT(1) FROM followers WHERE follower_id = %s;",
                                (self.id,)).fetchone()
        return result["count"]

    def is_following(self,user):
        result = db.cur.execute("SELECT 1 FROM followers WHERE followed_id = %s AND follower_id = %s;",
                                (user.id,self.id)).fetchone()
        return result is not None
    
    def following_posts(self,offset):
        result = db.cur.execute(f"""SELECT p.id,p.body,p.created_at,p.user_id, 
                                u.username, u.email, u.about_me, u.profile_picture, 
                                u.last_seen from posts p
                                INNER JOIN users u ON p.user_id = u.id
                                INNER JOIN followers f ON u.id = f.followed_id
                                WHERE f.follower_id = {self.id}
                                ORDER BY p.created_at DESC
                                LIMIT 30 OFFSET {offset};
                                """).fetchall()
        count = db.cur.execute(f"""SELECT 1 as "exists" from posts p
                                INNER JOIN users u ON p.user_id = u.id
                                INNER JOIN followers f ON u.id = f.followed_id
                                WHERE f.follower_id = {self.id}
                                LIMIT 30 OFFSET {offset + 30};
                                """).fetchone()
        
        if count is not None:
            count = count["exists"]
        else:
            count = 0

        return result, count
    
    def __str__(self):
        return f"Username:{self.username},email:{self.email},password:{self.password_hash}"
    
    def __repr__(self):
        return self
    
class Post():
    id: int
    body: str
    created_at: str
    user_id: int
    author: User

    def __init__(self,id,body,created_at,user_id,author):
        self.id = id
        self.body = body
        self.created_at = created_at
        self.user_id = user_id
        self.author = author

@login.user_loader
def load_user(id: int):
    user = db.cur.execute("SELECT username,email,password,profile_picture,last_seen,about_me FROM users WHERE id = %s;",(id,)).fetchone()
    return User(id=id,username=user["username"],email=user["email"],password_hash=user["password"],
                profile_picture=user["profile_picture"],last_seen=user["last_seen"],about_me=user.get("about_me")) or None