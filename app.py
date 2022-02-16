from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from weather import weather

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class Garden_DB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vegetable = db.Column(db.String(200), nullable=False)
    sow_timeline = db.Column(db.String(200))  # When to sow (direct, indoors) data
    sow_type = db.Column(db.String)  # Direct, Indoors, key used to filter later
    harvest_days = db.Column(db.Integer)  # How many days to harvest
    plant_spacing = db.Column(db.Integer)  # Inches between plants
    seed_depth = db.Column(db.Integer)  # Inches for seed depth
    sow_window_start = db.Column(db.String)  # Window to sow, regardless of sow type
    sow_window_end = db.Column(db.String)  # Window to sow, regardless of sow type
    transplant_window_start = db.Column(db.String)  # Window to transplant if applicable
    transplant_window_end = db.Column(db.String)  # Window to transplant if applicable
    harvest_window_start = db.Column(db.String)  # Window to harvest
    harvest_window_end = db.Column(db.String)  # Window to harvest
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # db.create_all


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
        sow_timeline_creation = request.form["sow_timeline"]
        sow_type_creation = request.form["sow_type"].title()
        harvest_days_creation = request.form["harvest_days"]
        plant_spacing_creation = request.form["plant_spacing"]
        seed_depth_creation = request.form["seed_depth"]
        sow_window_begin = request.form["sow_window_start"]
        sow_window_close = request.form["sow_window_end"]
        transplant_window_begin = request.form["transplant_window_start"]
        transplant_window_close = request.form["transplant_window_end"]
        harvest_window_begin = request.form["harvest_window_start"]
        harvest_window_close = request.form["harvest_window_end"]
        # new_vegetable = Garden_DB(
        #     vegetable=vegetable_creation,
        #     sow_timeline=sow_timeline_creation,
        #     sow_type=sow_type_creation,
        #     harvest_days=harvest_days_creation,
        #     plant_spacing=plant_spacing_creation,
        #     seed_depth=seed_depth_creation,
        #     sow_window_start=sow_window_begin,
        #     sow_window_end=sow_window_close,
        #     transplant_window_start=transplant_window_begin,
        #     transplant_window_end=transplant_window_close,
        #     harvest_window_start=harvest_window_begin,
        #     harvest_window_end=harvest_window_close,
        # )

        try:
            db.session.add(new_vegetable)
            db.session.commit()
            return redirect("/all")
        except Exception as ex:
            return ex
    else:
        return render_template("update.html")


if __name__ == "__main__":
    app.run(debug=True)
