from flaskblog import app



if __name__ == '__main__':
    app.run(debug=True)







# from flask import Flask,render_template,redirect,url_for
# from form import RegistrationForm,LoginForm
# from flask_sqlalchemy import SQLAlchemy
# import datetime

# app = Flask(__name__)

# # posts=[ { 'author':'devbrat jha','title':'politics','content':'pakistan has been a terrorist nation'},
# # { 'author':'hanish', 'title':'sports','content':'bowler'}
# # ]

# # @app.route("/")
# # def hello_world():
# #     return render_template('home.html',posts=posts,title='home')#left side of equal sign youre passing varible name and right side data,left side will be used in html right in list data in this app

# # @app.route("/about")
# # def about():
# #     return render_template('about.html')


# # Set the secret key
# app.config['SECRET_KEY'] = "47cbc83e5d0ca093b0f8fb560178904c"  #app.config is an object that stores configuration settings for your Flask application. Configuration settings are key-value pairs

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# db = SQLAlchemy(app)

# class User(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     username=db.Column(db.String(20),unique=True,nullable=False)
#     email=db.Column(db.String(20),unique=True,nullable=False)
#     password=db.Column(db.String(), nullable=False)
#     image_file=db.Column(db.String(20), nullable=False, default='default.jpg')
#     posts=db.relationship('Post',backref='author',lazy=True)#here we are referring to class,its not Column but relationship,it define all post for that user,with backref=author we can use author to relate with post

#     def __repr__(self):
#         return f"user {self.username},{self.email},{self.image_file}"

# class Post(db.Model):
#     # id=db.Column(db.Integer,primary_key=True)
#     title=db.Column(db.String(100),nullable=False)
#     content=db.Column(db.String(),nullable=False)
#     datetime=db.Column(db.Datetime,nullable=False,default=datetime.utcnow)#we are passing function instead of its value
#     user_id=db.Column(db.Integer,db.foreign_key('user.id'))#here we are referring to Column,auto converted into lowercase

#     def __repr__(self):
#         return f"user {self.title},{self.datetime}"#to return in readable format 



# @app.route("/home")
# @app.route("/")
# def home():
#     return render_template('home.html')
# @app.route("/registration",methods=['GET','POST'])
# def Registration():
#     form=RegistrationForm()
#     if form.validate_on_submit():
      
#         print('success')
#         return redirect(url_for('home'))#its function
#     return render_template('registration.html',form=form)

# @app.route("/login",methods=['GET','POST'])
# def Login():
#     form=LoginForm()
#     return render_template('login.html',form=form)#always provide data into parametre to send it into template



# if __name__ == '__main__':#this means we are running this file only , if we wish to run another file that we have put its file name is this
#     app.run(debug=True)

