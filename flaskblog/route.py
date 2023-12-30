from flaskblog import app,mail
from flask import render_template, redirect, url_for,request,abort,flash
from flask_login import login_user,current_user ,logout_user
import secrets,os
from flask_mail import Message

from flaskblog.form import RegistrationForm, LoginForm,UpdateForm,PostForm,PasswordReset,ResetForm
from flaskblog import bcrypt ,db
from flaskblog.models import User,Post

@app.route("/home")
@app.route("/")
def home():
    return render_template('home.html')


@app.route("/login", methods=['GET', 'POST'])
def Login():
    if current_user.is_authenticated:
       
        return redirect('homepage')
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)#this function helps in login 
            print('hello')
            return redirect(url_for('homepage'))
    return render_template('login.html', form=form)

@app.route("/registration", methods=['GET', 'POST'])
def Registration():
  
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed=bcrypt.generate_password_hash(form.password.data).decode('utf-8')#hased password coming fromo user
        user=User(username=form.username.data,email=form.email.data,password=hashed)
       
        
           
        db.session.add(user)
        db.session.commit()
        print('success')
        return redirect(url_for('Login'))
   
       
    return render_template('registration.html', form=form)




@app.route("/logout")
def Logout():
    logout_user()#if you go to this route user will be logged out
    return redirect(url_for('home'))#and redirected to this

#you go to this route then that decorated function will be called

@app.route("/account")
def account():
    if current_user.is_authenticated:
        image_file=url_for('static',filename='profile_pics/'+ current_user.image_file)#current user
        return render_template('account.html',image_file=image_file)
    else:
      return redirect(url_for('Login'))
    
@app.route("/homepage")
def homepage():
    page=request.args.get('page',1,type=int)
    print(page)#it returns what we write after?page=number that number will be returned
    posts=Post.query.order_by(Post.datetime.desc()).paginate(page=page,per_page=5)
    
  
  
    return render_template('homepage.html',posts=posts)

def save(image):
    random_hex=secrets.token_hex(8)
    _, file_extension = os.path.splitext(image.filename)
    file_name=random_hex+file_extension
    path=os.path.join(app.root_path,'static/profile_pics',file_name)
    image.save(path)
    return file_name

def delete(filename):
    path=os.path.join(app.root_path,'static/profile_pics',filename)
    if os.path.exists(path):
       os.remove(path)
 


@app.route("/update", methods=['GET', 'POST'])
def update_profile():
    if current_user.is_authenticated:
        form = UpdateForm()
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

        if form.validate_on_submit():
            if form.profile.data:
                delete(current_user.image_file)#it will delete older pro pic in case user is updating
                picture_file = save(form.profile.data)
                current_user.image_file = picture_file
            current_user.email = form.email.data
            current_user.username = form.username.data
            db.session.commit()
            return redirect(url_for('account'))

        elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email

        return render_template('update.html', image_file=image_file, form=form)

    return redirect(url_for('Login'))


@app.route("/post/new", methods=['GET', 'POST'])
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('homepage'))


    
    return render_template('newpost.html',form=form)

@app.route("/post/update", methods=['GET', 'POST'])
def update_post():
    post=Post.query.filter_by(user_id=current_user.id).first()
    print(post)
    if current_user.is_authenticated:
      if not post:
         abort(404)
      form=PostForm()
      if form.validate_on_submit():
        post.title= form.title.data 
        post.content=form.content.data
        db.session.commit()
        return redirect(url_for('homepage'))
        
      elif request.method == 'GET':
        form.title.data =post.title
        form.content.data =post.content

      return render_template('updatepost.html',form=form)
    


@app.route("/post/delete", methods=['GET', 'POST'])
def delete_post():
    post=Post.query.filter_by(user_id=current_user.id).first()
    print(post)
    if current_user.is_authenticated:
      if not post:
         abort(404)
      
      db.session.delete(post)
      db.session.commit()
      return redirect(url_for('homepage'))
    
def send_reset_email(user):
    token = user.get_reset_token()#generate token
    msg = Message('Password Reset Request',sender='######',recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_password', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)




   
    



@app.route("/reset/email", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated: 
        return redirect(url_for('homepage'))  
    form=ResetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
 
    return render_template('resetrequest.html',form=form)


@app.route("/reset/password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated: 
        return redirect(url_for('homepage')) 
    user=User.verify_reset_token(token) #return userid
    form=ResetForm()
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = PasswordReset()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('Login'))
   
 
    return render_template('passwordreset.html',form=form)



    

        
      

      
    





