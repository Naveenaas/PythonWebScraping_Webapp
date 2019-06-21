from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask import redirect

app = Flask(__name__)
database_file = "sqlite:///goodreeds.db"

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app);

class GoodReed(db.Model):
    ids = db.Column(db.Integer,
          primary_key=True)
    
    name = db.Column(db.String(80), 
           nullable=False,
           unique=True)
    
    author = db.Column(db.String(80), 
           nullable=False)
    
    year = db.Column(db.Integer,
           nullable=False)
    
    rating = db.Column(db.Integer,
           nullable=False)
    
    def __repr__(self):
        return "<Name: {}>".format(self.name)
    
db.create_all()

@app.route("/", methods=["GET", "POST"])
def home():
    try:
        gReeds = GoodReed.query.limit(50).all()
    except:
        print("Error in reading the Names!")
    return render_template("links.html", gReeds=gReeds)

@app.route("/add", methods=["GET", "POST"])
def add():
    try:
        if request.form:
            #random_number = random.randint(1, 1000)
            names = GoodReed(name=request.form.get("addname"), author="xyz", year=2020, rating=5)
            db.session.add(names)
            db.session.commit()
    except:
        print("Error in adding the Name!")
    return redirect("/")

@app.route("/delete/<title>", methods=["GET", "POST"])
def delete(title):
    try:
        gReed = GoodReed.query.filter_by(name=title).first()
        db.session.delete(gReed)
        db.session.commit()
    except:
        print("Error in deleting the Name!")
    return redirect("/")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    try:
        if request.form:
                newname = request.form.get("newtitle")
                oldname = request.form.get("oldtitle")
                gReed = GoodReed.query.filter_by(name = oldname).first()
                gReed.name = newname
                db.session.commit()
    except:
        print("Error in editing the Name!")
    return redirect("/")

@app.route("/search", methods=["GET", "POST"])
def search():
    try:
        if request.form:
            searchname = request.form.get("searchname")
            gReeds = GoodReed.query.filter_by(name=searchname).limit(50).all()
    except:
        print("Error in searching the Name!")
    return render_template("links.html", gReeds=gReeds)
       
if __name__ == "__main__" :
    app.run(debug=True)