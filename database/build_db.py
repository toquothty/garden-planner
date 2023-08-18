from sqlalchemy import Column, create_engine, Column, DateTime, Float, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, date

import csv

engine = create_engine("sqlite:///app/database.db")

Base = declarative_base()


class Garden_DB(Base):
    __tablename__ = "garden_DB"

    id = Column(Integer, primary_key=True)
    vegetable = Column(String(200), nullable=False)
    sow_type = Column(String)  # Direct, Indoors, key used to filter later
    harvest_days = Column(Integer)  # How many days to harvest
    plant_spacing = Column(Integer)  # Inches between plants
    seed_depth = Column(Integer)  # Inches for seed depth
    sow_window_start = Column(String)  # Window to sow, regardless of sow type
    sow_window_end = Column(String)  # Window to sow, regardless of sow type
    transplant_window_start = Column(String)  # Window to transplant if applicable
    transplant_window_end = Column(String)  # Window to transplant if applicable
    harvest_window_start = Column(String)  # Window to harvest
    harvest_window_end = Column(String)  # Window to harvest
    vegetable_picture_url = Column(String)  # Public URL for vegetable picture
    date_created = Column(DateTime, default=datetime.utcnow)


# Create the database table
Base.metadata.create_all(engine)
# Establish a persistent session function
Session = sessionmaker(bind=engine)


with open("garden_data.csv", encoding="utf-8", newline="") as csv_file:
    # Read in csv, establish session to Database, loop through rows in csv
    csvreader = csv.DictReader(csv_file)
    session = Session()
    for row in csvreader:
        vegetable = row["vegetable"]
        sow_type = row["sow_type"]
        harvest_days = row["harvest_days"]
        plant_spacing = row["plant_spacing"]
        seed_depth = row["seed_depth"]
        sow_window_start = row["sow_window_start"]
        sow_window_end = row["sow_window_end"]
        transplant_window_start = row["transplant_window_start"]
        transplant_window_end = row["transplant_window_end"]
        harvest_window_start = row["harvest_window_start"]
        harvest_window_end = row["harvest_window_end"]
        vegetable_picture_url = row["vegetable_picture_url"]

        # While in loop, stage column/row data
        create_vegetable = Garden_DB(
            vegetable=vegetable,
            sow_type=sow_type,
            harvest_days=harvest_days,
            plant_spacing=plant_spacing,
            seed_depth=seed_depth,
            sow_window_start=sow_window_start,
            sow_window_end=sow_window_end,
            transplant_window_start=transplant_window_start,
            transplant_window_end=transplant_window_end,
            harvest_window_start=harvest_window_start,
            harvest_window_end=harvest_window_end,
            vegetable_picture_url=vegetable_picture_url,
        )
        # Stage and commit per vegetable in loop
        session.add(create_vegetable)
        session.commit()

