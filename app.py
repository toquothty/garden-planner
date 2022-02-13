from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from weather import weather

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)


class Garden_DB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vegetable = db.Column(db.String(200), nullable=False)
    sow_timeline = db.Column(db.String(200))  # When to sow (direct, indoors)
    sow_type = db.Column(db.String)  # Direct, Indoors
    harvest_days = db.Column(db.Integer)  # How many days to harvest
    plant_spacing = db.Column(db.Integer)  # Inches between plants
    seed_depth = db.Column(db.Integer)  # Inches for seed depth
    sow_window = db.Column(db.Date)  # Window to sow, regardless of sow type
    transplant_window = db.Column(db.Date)  # Window to transplant if applicable
    harvest_window = db.Column(db.Date)  # Window to harvest
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
@app.route("/home", methods=["GET"])
def index():
    time_period, temperature, forecast, temp_icon = weather()
    return render_template(
        "index.html",
        time_period=time_period,
        temperature=temperature,
        forecast=forecast,
        temp_icon=temp_icon,
    )


@app.route("/all", methods=["POST", "GET"])
def display_vegetables():
    vegetables = Garden_DB.query.order_by(Garden_DB.vegetable).all()
    return render_template("all.html", vegetables=vegetables)


@app.route("/update", methods=["POST", "GET"])
def update_vegetable():
    if request.method == "POST":
        vegetable_creation = request.form["vegetable"].title()
        new_vegetable = Garden_DB(vegetable=vegetable_creation)

        try:
            db.session.add(new_vegetable)
            db.session.commit()
            return redirect("/all")
        except:
            return "There was an issue adding your task"
    else:
        return render_template("update.html")


if __name__ == "__main__":
    app.run(debug=True)
