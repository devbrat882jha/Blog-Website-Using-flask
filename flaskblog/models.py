from flaskblog import db,app
import datetime
from flaskblog import login_manager
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as serializer

@login_manager.user_loader#passes load user function to this decorator
def load_user(user_id):
    # Return a user object based on the user_id.
    # This is typically done by querying a database.
    return User.query.get(int(user_id))



class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self,expires_in=1800):
        s=serializer(app.config['SECRET_KEY'] )
        return s.dumps({'user_id':self.id}) #.decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s=serializer(app.config['SECRET_KEY'] ,expires_sec=30)
        try:
            user_id=s.loads(token)['user_id']#it will give userid
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"user {self.username},{self.email},{self.image_file}"

class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"user {self.title},{self.datetime}"
    
