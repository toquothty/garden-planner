from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from weather import weather

# Establish basic global paramters
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

# Establish the database class/model
class Garden_DB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vegetable = db.Column(db.String(200), nullable=False)
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
    vegetable_picture_url = db.Column(db.String)  # Public URL for vegetable picture
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


# Establish the homepage URLs
@app.route("/forecast", methods=["GET"])
def forecast():
    # Utilize weather.py to grab the forecast for the next three time periods as defined by NWS
    time_period, temperature, forecast, temp_icon = weather()
    return render_template(
        "forecast.html",
        time_period=time_period,
        temperature=temperature,
        forecast=forecast,
        temp_icon=temp_icon,
    )


# Create a page to list all vegetables listed in the database
# Utilize this page to link to individual vegetable detail URLs
@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
@app.route("/home", methods=["GET"])
def display_vegetables():
    vegetables = Garden_DB.query.order_by(Garden_DB.id).all()
    return render_template("home.html", vegetables=vegetables)


# Use jinja templating to dynamically build URL based on vegetable clicked in /list
@app.route("/list/<get_vegetable>", methods=["GET"])
def get_user_vegetable(get_vegetable):
    # Uppercase the vegetable entry from the URL call to match case in DB
    transform_vegetable = get_vegetable.title()
    # Query the database to return the database row data based on vegetable
    transform_vegetable = (
        db.session.query(Garden_DB).filter_by(vegetable=transform_vegetable).first()
    )
    # Grab the appropriate column data for the row called
    vegetable = transform_vegetable.vegetable
    sow_type = transform_vegetable.sow_type
    harvest_days = transform_vegetable.harvest_days
    plant_spacing = transform_vegetable.plant_spacing
    seed_depth = transform_vegetable.seed_depth
    # If direct sow type, we'll feed the sow window dates
    if sow_type == "Direct":
        window_start = transform_vegetable.sow_window_start
        window_end = transform_vegetable.sow_window_end
    # If transplant type, we'll feed the transplant window dates
    else:
        window_start = transform_vegetable.transplant_window_start
        window_end = transform_vegetable.transplant_window_end
    harvest_window_start = transform_vegetable.harvest_window_start
    harvest_window_end = transform_vegetable.harvest_window_end

    return render_template(
        "vegetable.html",
        vegetable=vegetable,
        sow_type=sow_type,
        harvest_days=harvest_days,
        plant_spacing=plant_spacing,
        seed_depth=seed_depth,
        window_start=window_start,
        window_end=window_end,
        harvest_window_start=harvest_window_start,
        harvest_window_end=harvest_window_end,
    )


# Created a URL that will query/filter the database and show items with
# vegetables that have windows based on the current date
@app.route("/todays-tasks", methods=["GET"])
def display_tasks():
    today = date.today()
    vegetable_list = Garden_DB.query.order_by(Garden_DB.vegetable).all()

    render_task_dict = {}

    for item in vegetable_list:
        sow_type = item.sow_type
        if sow_type == "Direct":
            window_start = item.sow_window_start
            window_end = item.sow_window_end
            window_start_transfrom = datetime.strptime(window_start, "%Y-%m-%d").date()
            window_end_transfrom = datetime.strptime(window_end, "%Y-%m-%d").date()
        else:
            window_start = item.transplant_window_start
            window_end = item.transplant_window_end
            window_start_transfrom = datetime.strptime(window_start, "%Y-%m-%d").date()
            window_end_transfrom = datetime.strptime(window_end, "%Y-%m-%d").date()
        harvest_window_start = item.harvest_window_start
        harvest_window_end = item.harvest_window_end
        harvest_start_transfrom = datetime.strptime(
            harvest_window_start, "%Y-%m-%d"
        ).date()
        harvest_end_transfrom = datetime.strptime(harvest_window_end, "%Y-%m-%d").date()

        if window_start_transfrom <= today <= window_end_transfrom:
            render_task_dict[item.vegetable] = sow_type

        elif harvest_start_transfrom <= today <= harvest_end_transfrom:
            render_task_dict[item.vegetable] = "Harvest"

    return render_template("todays-tasks.html", tasks=render_task_dict)


# Removing access to this method until login features are added.
# @app.route("/update", methods=["POST", "GET"])

# def update_vegetable():
#     if request.method == "POST":
#         vegetable_creation = request.form["vegetable"].title()
#         sow_type_creation = request.form["sow_type"].title()
#         harvest_days_creation = request.form["harvest_days"]
#         plant_spacing_creation = request.form["plant_spacing"]
#         seed_depth_creation = request.form["seed_depth"]
#         sow_window_begin = request.form["sow_window_start"]
#         sow_window_close = request.form["sow_window_end"]
#         transplant_window_begin = request.form["transplant_window_start"]
#         transplant_window_close = request.form["transplant_window_end"]
#         harvest_window_begin = request.form["harvest_window_start"]
#         harvest_window_close = request.form["harvest_window_end"]
#         new_vegetable = Garden_DB(
#             vegetable=vegetable_creation,
#             sow_type=sow_type_creation,
#             harvest_days=harvest_days_creation,
#             plant_spacing=plant_spacing_creation,
#             seed_depth=seed_depth_creation,
#             sow_window_start=sow_window_begin,
#             sow_window_end=sow_window_close,
#             transplant_window_start=transplant_window_begin,
#             transplant_window_end=transplant_window_close,
#             harvest_window_start=harvest_window_begin,
#             harvest_window_end=harvest_window_close,
#         )

#         try:
#             db.session.add(new_vegetable)
#             db.session.commit()
#             return redirect("/all")
#         except Exception as ex:
#             return ex
#     else:
#         return render_template("update.html")


if __name__ == "__main__":
    app.run()
