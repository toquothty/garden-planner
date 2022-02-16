from sqlalchemy import Column, create_engine, Column, DateTime, Float, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, date

import csv

engine = create_engine("sqlite:///database.db")

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
    date_created = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


# def prepare_row(row):
#     row["vegetable"] = parse_none(row["vegetable"])
#     return Garden_DB(**row)


with open("garden_data.csv", encoding="utf-8", newline="") as csv_file:
    csvreader = csv.DictReader(csv_file)
    # vegetable = [prepare_row(row) for row in csvreader]
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
        )

        session.add(create_vegetable)
        session.commit()
