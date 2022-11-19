from flask import Flask, request, render_template, request, redirect, url_for, session
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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(50))
    password = db.Column(db.String(50))

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(50))
    password = db.Column(db.String(50))


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
                return redirect("/")
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
                return redirect("/")
            else:
                error = "Please enter the username and password"
                return render_template('registerService.html', error=error)
        else:
            error = "Username already exists"
            return render_template('registerService.html', error=error)
    return render_template('registerService.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=2000)