from flask import Flask, request, render_template, request, redirect, url_for, session, jsonify, Response
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)




#Database attributes
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(50))
    password = db.Column(db.String(50))
    details = db.relationship('detailsuser', backref='user')
    loc = db.relationship('userloc', backref='user')

class userloc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.String(50))
    lng = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class serviceloc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.String(50))
    lng = db.Column(db.String(50))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))

class detailsuser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    email = db.Column(db.String(50))
    contact = db.Column(db.String(50))
    publicid = db.Column(db.String(50))
    profession = db.Column(db.String(50))
    experience = db.Column(db.String(50))
    status = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(50))
    password = db.Column(db.String(50))
    details = db.relationship('detailsservice', backref='service')
    loc = db.relationship('serviceloc', backref='service')


class detailsservice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    email = db.Column(db.String(50))
    contact1 = db.Column(db.String(50))
    contact2 = db.Column(db.String(50))
    publicid = db.Column(db.String(50))
    profession = db.Column(db.String(50))
    field = db.Column(db.String(50))
    status = db.Column(db.Boolean)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))




@app.route("/")
def index():
    return render_template('index.html')

@app.route("/registerUser", methods=["GET","POST"])
def registerUser():
    if request.method == "GET":
        return render_template("registerUser.html")
    if request.method == "POST":
        uname = request.form.get("uname")
        password = request.form.get("password")
        if not User.query.filter_by(uname=uname).first():
            if uname and password:
                # hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
                new_user = User(uname=uname, password=password)
                db.session.add(new_user)
                db.session.commit()
                return redirect("/loginUser")
            else:
                error = "Please enter the username and password"
                return render_template('registerUser.html', error=error)
        else:
            error = "Username already exists"
            return render_template('registerUser.html', error=error)

    return render_template('registerUser.html')



@app.route("/registerService", methods=["GET","POST"])
def registerService():
    if request.method == "GET":
        return render_template("registerService.html")
    if request.method == "POST":
        uname = request.form.get("uname")
        password = request.form.get("password")
        if not Service.query.filter_by(uname=uname).first():
            if uname and password:
                # hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
                new_user = Service(uname=uname, password=password)
                db.session.add(new_user)
                db.session.commit()
                return redirect("/loginService")
            else:
                error = "Please enter the username and password"
                return render_template('registerService.html', error=error)
        else:
            error = "Username already exists"
            return render_template('registerService.html', error=error)
    return render_template('registerService.html')



@app.route("/loginUser", methods=["GET", "POST"])
def loginUser():
    if request.method == "POST":
        uname = request.form.get("uname")
        password = request.form.get("password")
        # user = User.query.filter_by(uname = session["uname"]).first()
        user = User.query.filter_by(uname = uname).first()
        if user:
            # if check_password_hash(user.password, password):
            if user.password == password:
                session.permanent = False
                session["uname"] = uname
                return redirect("/userDashboard")
            else:
                error = "Invalid username or password"
                return render_template('loginUser.html', error=error)
        else:
            error = "Invalid username or password"
            return render_template('loginUser.html', error=error)
    return render_template('loginUser.html')


@app.route("/loginService", methods=["GET", "POST"])
def loginService():
    if request.method == "POST":
        uname = request.form.get("uname")
        password = request.form.get("password")
        # user = User.query.filter_by(uname = session["uname"]).first()
        user = Service.query.filter_by(uname = uname).first()
        if user:
            # if check_password_hash(user.password, password):
            if user.password == password:
                session.permanent = False
                session["uname"] = uname
                return redirect("/serviceDashboard")
            else:
                error = "Invalid username or password"
                return render_template('loginService.html', error=error)
        else:
            error = "Invalid username or password"
            return render_template('loginService.html', error=error)
    return render_template('loginService.html')


# Location functionalities
@app.route("/getLoc", methods=["GET", "POST"])
def getLoc():
    if request.method == "POST":
        user = User.query.filter_by(uname = session["uname"]).first()
        lat=request.form.get("cord1")
        lng=request.form.get("cord2")    
        user_loc = userloc(lat=lat,lng=lng,user_id=user.id)
        db.session.add(user_loc)
        db.session.commit()
    return Response(status = 204)

@app.route("/getLoc1", methods=["GET", "POST"])
def getLoc1():
    if request.method == "POST":
        user = Service.query.filter_by(uname = session["uname"]).first()
        lat=request.form.get("cord1")
        lng=request.form.get("cord2")    
        user_loc = serviceloc(lat=lat,lng=lng,service_id=user.id)
        db.session.add(user_loc)
        db.session.commit()
    return Response(status = 204)    
    

#Dashboard functionalities
@app.route("/userDashboard")
def userDashboard():
    user = User.query.filter_by(uname = session["uname"]).first()
    user_details = detailsuser.query.filter_by(user_id = user.id)
    service_details = detailsservice.query.all()
    countAmb = detailsservice.query.filter_by(profession="Ambulance").count()
    countDoc = detailsservice.query.filter_by(profession="Doctor").count()
    countDon = detailsservice.query.filter_by(profession="Blood Donor").count()
    countPharm = detailsservice.query.filter_by(profession="Pharmacy").count()
    return render_template('userDashboard.html',user_details=user_details, service_details=service_details,countAmb=countAmb,countDoc=countDoc,countDon=countDon,countPharm=countPharm)


@app.route("/serviceDashboard")
def serviceDashboard():
    user_details = detailsuser.query.all()
    user1 = Service.query.filter_by(uname = session["uname"]).first()
    service_details = detailsservice.query.filter_by(service_id = user1.id)
    return render_template('serviceDashboard.html', service_details=service_details, user_details = user_details)

@app.route("/userDetails",  methods=["GET", "POST"])
def userDetails():
    if request.method == "POST":
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        email = request.form.get("email")
        contact = request.form.get("contact")
        publicid = request.form.get("publicid")
        profession = request.form.get("profession")
        experience = request.form.get("experience")
        user = User.query.filter_by(uname = session["uname"]).first()
        user_details = detailsuser(firstName=firstName, lastName=lastName,email=email,contact=contact,publicid=publicid,profession=profession,experience=experience, status=False, user_id=user.id)
        db.session.add(user_details)
        db.session.commit()
        return redirect('/userDashboard')
    return render_template('userDetails.html')

@app.route("/changeStatus")
def changeStatus():
    user = Service.query.filter_by(uname = session["uname"]).first()
    service = detailsservice.query.filter_by(service_id = user.id).first()
    service.status = not service.status
    db.session.commit()

    service_details = detailsservice.query.filter_by(service_id = user.id)
    return render_template('serviceDashboard.html', service_details=service_details)

@app.route("/changeStatus1")
def changeStatus1():
    user = User.query.filter_by(uname = session["uname"]).first()
    user_pick = detailsuser.query.filter_by(user_id = user.id).first()
    user_pick.status = not user_pick.status
    db.session.commit()
    service_details = detailsservice.query.all()
    user_details = detailsuser.query.filter_by(user_id = user.id)
    countAmb = detailsservice.query.filter_by(profession="Ambulance").count()
    countDoc = detailsservice.query.filter_by(profession="Doctor").count()
    countDon = detailsservice.query.filter_by(profession="Blood Donor").count()
    countPharm = detailsservice.query.filter_by(profession="Pharmacy").count()
    return render_template('userDashboard.html',user_details=user_details, service_details=service_details,countAmb=countAmb,countDoc=countDoc,countDon=countDon,countPharm=countPharm)
    

@app.route("/serviceDetails",  methods=["GET", "POST"])
def serviceDetails():
    if request.method == "POST":
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        email = request.form.get("email")
        contact1 = request.form.get("contact1")
        contact2 = request.form.get("contact2")
        publicid = request.form.get("publicid")
        profession = request.form.get("profession")
        field = request.form.get("field")
        service = Service.query.filter_by(uname = session["uname"]).first()
        service_details = detailsservice(firstName=firstName, lastName=lastName,email=email,contact1=contact1,contact2=contact2,publicid=publicid,profession=profession,field=field, status=True,service_id=service.id)
        db.session.add(service_details)
        db.session.commit()
        return redirect('/serviceDashboard')
        # elif Service.query.filter_by(uname = session["uname"]).first():
    return render_template('serviceDetails.html')



@app.route("/logout")
def logout():
    session["uname"] = None
    return redirect("/")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=2000)