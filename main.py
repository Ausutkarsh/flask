from  flask import Flask, session,render_template,request,redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import pymysql
from werkzeug.utils import secure_filename
import json
import os
import math
from flask_mail import Mail
pymysql.install_as_MySQLdb()

with open('config.json','r') as c:
    params=json.load(c)["params"]
local_server=True


app=Flask(__name__)
app.secret_key='super-sexret-key'
app.config['UPLOAD_FOLDER'] = params['upload_location']
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-password']
)
mail=Mail(app)
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI']=params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db = SQLAlchemy(app)

class Contacts(db.Model):
    #sno name phone_num msg date email

    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    phone_num = db.Column(db.String(12), unique=True, nullable=False)

    msg = db.Column(db.String(600), unique=False, nullable=False)

    date = db.Column(db.String(12), unique=False, nullable=False)

    email =db.Column(db.String(80), unique=False, nullable=False)


class Posts(db.Model):
    #sno name title slug content date

    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    slug = db.Column(db.String(30), unique=True, nullable=False)
    tagline = db.Column(db.String(600), unique=False, nullable=False)
    content = db.Column(db.String(600), unique=False, nullable=False)
    img_file = db.Column(db.String(12), unique=False, nullable=False)
    date = db.Column(db.String(12), unique=False, nullable=False)

@app.route("/post/<string:post_slug>",methods=['GET']) # end point ut
def post_route(post_slug):
    post=Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html',params=params,post=post)#name2 can be any word which is used in html file about



@app.route("/dashboard",methods=['GET','POST'])# end point
def dashboard():
    #checking user is already login or not
    if 'user' in session and session['user'] == params['admin_user']:
        posts = Posts.query.all()
        return render_template('dashboard.html', params=params, posts=posts)

        # checking for login credentials

    # redirect to admin
    username = request.form.get('uname')
    userpass = request.form.get('pass')
    if username == params['admin_user'] and userpass == params['admin_password']:
        session['user'] = username
        posts=Posts.query.all()
        return render_template('dashboard.html',params=params,posts=posts)
    return render_template('signin.html',params=params)


@app.route("/")# end point
def home():
    posts=Posts.query.filter_by().all()#       [: params['no_of_posts']]---to calc number of post
    last=math.ceil(len(posts)/int(params['no_of_posts']))
    #logic of pagination ie button older post and newer page
    page= (request.args.get('page'))
    if (not str(page).isnumeric()):
        page=1
    page=int(page)
    posts = posts[(page-1)*int(params['no_of_posts']):(page-1)* int(params['no_of_posts'])+int(params['no_of_posts'])]
    if page==1:
        prev="#"
        next="/?page="+str(page+1)
    elif page==last:
        prev = "/?page=" + str(page - 1)
        next = "#"
    else:
        prev="/?page=" + str(page -1)
        next="/?page=" + str(page + 1)

    return render_template('index.html', params=params, posts=posts,prev=prev,next=next)


@app.route("/edit/<string:sno>", methods=['GET','POST'])# end point ut
def edit(sno):
    if 'user' in session and session['user']==params['admin_user']:
        if request.method=='POST':
            box_title=request.form.get('title')
            box_tline = request.form.get('tline')
            box_slug = request.form.get('slug')
            box_content = request.form.get('content')
            box_img_file = request.form.get('img_file')

            if sno=='0':
                post=Posts(title=box_title,slug=box_slug,content=box_content,img_file=box_img_file,tagline=box_tline,date=datetime.now())
                db.session.add(post)
                db.session.commit()
            else:
                post=Posts.query.filter_by(sno=sno).first()
                post.title=box_title
                post.slug=box_slug
                post.content=box_content
                post.tagline=box_tline
                post.img_file=box_img_file
                post.date=datetime.now()
                db.session.add(post)
                db.session.commit()
                return redirect('/edit/'+sno)
        post=Posts.query.filter_by(sno=sno).first()
        return render_template('edit.html',params=params,post=post)
@app.route("/uploader", methods=['GET','POST'])# end point ut
def uploader():
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method=='POST':
            f=request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
            return "Uploaded Successfully"

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/dashboard')

@app.route("/delete/<string:sno>", methods=['GET','POST'])# end point ut
def delete(sno):

    if 'user' in session and session['user']==params['admin_user']:
        post=Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
        return redirect('/dashboard')









@app.route("/contact", methods=['GET','POST'])# end point ut
def contact():
    if request.method=='POST':
        #add entry to database
        name=request.form.get('name')#name inside bracket as same as used in contact.html
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        entry=Contacts(name=name, phone_num=phone,msg=message,date=datetime.now(),email=email)
        db.session.add(entry)
        db.session.commit()
        mail.send_message("New Message Received",
                          sender=email,
                          recipients=[params['gmail-user']],
                          body=message+"\n"+phone
                          )
    return render_template('contact.html',params=params)#name2 can be any word which is used in html file about

@app.route("/about")# end point ut
def about():
    return render_template('about.html',params=params)#name2 can be any word which is used in html file about

@app.route("/signin")# end point ut
def signin():
    return render_template('signin.html',params=params)#name2 can be any word which is used in html file about

app.run(debug=True)