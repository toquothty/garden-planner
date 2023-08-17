from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

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