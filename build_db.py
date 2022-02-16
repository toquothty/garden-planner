from sqlalchemy import Column, create_engine, Column, DateTime, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine("sqlite///database.db", echo=True)

Base = declarative_base()


class Garden_DB(Base):
    __tablename__ = "Garden_Planner"

    id = Column(Integer, primary_key=True)
    vegetable = Column(String(200), nullable=False)
    sow_timeline = Column(String(200))  # When to sow (direct, indoors) data
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
