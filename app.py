from flask import Flask ,render_template, abort, redirect, url_for, flash , request , make_response , session ,jsonify
from flask_login import login_user, current_user, logout_user, login_required,LoginManager
from datetime import datetime
from forms import loginform , signupform
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail ,Message
import os
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd 
from oauthlib.oauth2 import WebApplicationClient
import requests
import json
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_pymongo import PyMongo



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/test.db'
db = SQLAlchemy(app)
from models import student , gender , country , level , faculty ,spiciality, service_category,service

db.create_all()

mail = Mail(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = '/login'
mail.init_app(app)

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = "khasarou@gmail.com"
app.config['MAIL_PASSWORD'] = "toma1998$A"
app.config['MAIL_USE_SSL'] = True


UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) 
UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER,'static')        
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif' , 'xlsx'}

app.config["MONGO_URI"] = "mongodb+srv://user:name@cluster0.oz4o7.mongodb.net/mustapha?retryWrites=true&w=majority"
mongodb_client = PyMongo(app)
db = mongodb_client.db
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mail = Mail(app)






app.config['SECRET_KEY'] = 'the random string'    


@app.route("/login" ,methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if  request.method == 'POST':
        user = student.query.filter_by(username=request.form['username']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html' )





@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return 'ya  kho rah  kayn un probleme ' 

x  = [["mustapha",["algerie","belgique"]],["belkassem",["ecre","mop"]],["fares",["free","fires"]]]
def add_services(x) : 
    for i in range(len(x)) : 
        if service_category.query.filter_by(name=x[i][0]).first() : 
            serca = service_category.query.filter_by(name=x[i][0]).first()
        else : 
            serca = service_category(name = x[i][0])
            for j in range(len(x[i][1])):
                service_added = service(name = x[i][1][j], serca = serca)
                db.session.add(service_added)
                db.session.commit()

add_services(x)

def add_student(username ,password , email,phone , gen ,cntry,levl,facult, spiciali ) : 
    """. function to add new student to the database."""
    gender_id = gender(name = gen)
    if gender.query.filter_by(name=gen).first() : 
        gender_id = gender.query.filter_by(name=gen).first()
    
    country_id = country(name = cntry)
    if country.query.filter_by(name=cntry).first() : 
        country_id = country.query.filter_by(name=cntry).first()
    
    level_id = level(name = levl)
    if level.query.filter_by(name=levl).first() : 
        level_id = level.query.filter_by(name=levl).first()
    
    faculty_id = faculty(name = facult)
    if faculty.query.filter_by(name=facult).first() : 
        faculty_id = faculty.query.filter_by(name=facult).first()
    
    spiciality_id = spiciality(name = spiciali)
    if spiciality.query.filter_by(name=spiciali).first() : 
        spiciality_id = spiciality.query.filter_by(name=spiciali).first()

    student_added = student(username = username ,password =password , email = email,phone =phone , gen =gender_id,cntry = country_id,
        levl =level_id ,facult = faculty_id, spiciali =spiciality_id)

    db.session.add(student_added)
    db.session.commit()
@app.route("/signup",methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form['username']
        x =  request.form.get('toma')
        password = request.form['phone']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        gender_id = request.form['fav_language'] 
        country_id = request.form['country']
        level_id = request.form['level']
        faculty_id =request.form['faculty']
        spiciality_id = request.form['speciality']
        add_student(username = username ,password =hashed_password , email = email,phone =phone , gen =gender_id,cntry = country_id,
        levl =level_id ,facult = faculty_id, spiciali =spiciality_id)
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect('/profile')
    return render_template('signup.html')



@app.route("/profile")
@login_required
def profile():
    student =  current_user
    return render_template('landing.html' , user = student)

@login_manager.user_loader
def load_user(user_id):
    return student.query.filter_by(id=user_id).first()



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' in request.files :
            f = request.files['file']
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect('/moh')
        else:
            return redirect('/moh')
    return render_template('signup.html')



#login using goole 
# Configuration
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
GOOGLE_CLIENT_ID = "GOOGLE_CLIENT_ID"
GOOGLE_CLIENT_SECRET = "GOOGLE_CLIENT_SECRET"
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)
def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route("/login_google")
def login_google():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login_google/callback")
def callback_google():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    client.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
        user = student.query.filter_by(email=users_email).first()
        if user :
            login_user(user, remember=True)
            return redirect('/home')
        else:
            return redirect('/login')



#end construction of api 

# part of login using twitter 
blueprint = make_twitter_blueprint(
    api_key="my-key-here",
    api_secret="my-secret-here",
)
app.register_blueprint(blueprint, url_prefix="/login_twitter")
@app.route("/login_twitter")
def login_twitter():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login_twitter/callback")
def callback_twitter():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    client.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
        user = student.query.filter_by(email=users_email).first()
        if user :
            login_user(user, remember=True)
            return redirect('/home')
        else:
            return redirect('/login')

# end part of loging using facebook


@app.route('/')
def first():
    return render_template('landing.html')

@app.route('/main')
def home():
    return render_template('main.html')



@app.route('/who_us')
def who():
    return render_template('who_us.html')

@app.route('/our_experts')
def experts():
    return render_template('our_experts.html')

@app.route('/portofolio')
def potofolio():
    return render_template('potofolio.html')

@app.route('/blogs')
def blogs():
    list_blogs=db.blogs.find()
    list_blogs = list(list_blogs)
    for blog in list_blogs :
        blog['_id'] = str(blog['_id'])  
    return render_template('blogs.html' ,list_blogs = list_blogs)

@app.route('/blogs/blog/<int:id>')
def blog(id):
    list_blogs=db.blogs.find({'id':id})
    blog=list_blogs[0]
    return render_template('blog.html' ,blog = blog)

@app.route('/challenge')
def challenge():
    return render_template('challenge.html')

@app.route('/join_us')
def join():
    return render_template('join_us.html')



@app.route('/jobs',methods=['GET', 'POST'])
def jobs():
    list_jobs=db.jobs.find()
    list_jobs = list(list_jobs)
    for job in list_jobs :
        job['_id'] = str(job['_id'])    
    return render_template('jobs.html' , list_jobs =list_jobs )

@app.route('/jobs/job/<int:job>',methods=['GET', 'POST'])
def job(job):
    job=db.jobs.find({"id":job})[0]
    return render_template('job.html' ,job = job)


@app.route('/jobs/job/<int:job>/apply',methods=['GET', 'POST'])
def apply(job) : 
    if request.method == 'POST':
        print('start')
        name = request.form['username']
        email = request.form['email']
        print(name,email)
        lnkedin = request.form['linkedin']
        phone = request.form['phone']
        f = request.files['cv']
        filename = secure_filename(name +'.pdf')
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        condidate = {'job_id':job,"name":name,
                    "email":email,
                    "linkedin":  lnkedin,
                    "phine_number" : phone }
        print(condidate)
        add = db.condidate.insert_one(condidate)
    return render_template('appy_job.html')


@app.route('/services')
def services():
    list_services=db.services.find()
    list_services = list(list_services)
    for service in list_services :
        service['_id'] = str(service['_id'])
    categories = [service['category'] for service in list_services]    
    return render_template('services.html' , categories = categories)

@app.route('/services/<category>')
def service_category(category) : 
    list_services=db.services.find({'category':category})
    list_services = list(list_services)
    for service in list_services :
        service['_id'] = str(service['_id'])
    return render_template('services_category.html' ,list_services = list_services)


@app.route('/services/<category>/<int:id>')
def service(id,category):
    service_return=db.services.find({'category':category,'id':id})
    service_return = service_return[0]
    service_return['_id'] = str(service_return['_id'])
    return render_template('service.html',service_return = service_return)


if __name__ == '__main__':
    app.run(debug=True )
