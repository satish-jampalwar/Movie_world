from sqlalchemy import create_engine, Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

# Define Base for ORM models
Base = declarative_base()

# Define the Movie table as a class


class Movie(Base):
    __tablename__ = 'movies'

    tconst = Column(Text, primary_key=True)
    titleType = Column(Text)
    primaryTitle = Column(Text)
    originalTitle = Column(Text)
    isAdult = Column(Integer)
    startYear = Column(Integer)
    endYear = Column(Integer)
    runtimeMinutes = Column(Integer)
    genres = Column(Text)

# Define the Persons table as a class


class Persons(Base):
    __tablename__ = 'persons'

    nconst = Column(Text, primary_key=True)
    primaryName = Column(Text)
    birthYear = Column(Integer)
    deathYear = Column(Integer)
    primaryProfession = Column(String)
    knownForTitles = Column(String)


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    email = Column(String)


# Database connection string
DATABASE_URL = "sqlite:///movieworld.db"

# Create the engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Create tables in the database
Base.metadata.create_all(engine)

# Load data from TSV and insert into the database
# Load Movie data
movies_file = "title.basics.tsv"
movies_df = pd.read_csv(movies_file, sep="\t", nrows=2000)

# Convert Movie data to a list of Movie objects
movies = [
    Movie(
        tconst=row["tconst"],
        titleType=row["titleType"],
        primaryTitle=row["primaryTitle"],
        originalTitle=row["originalTitle"],
        isAdult=row["isAdult"],
        startYear=row.get("startYear", None),
        endYear=row.get("endYear", None),
        runtimeMinutes=row.get("runtimeMinutes", None),
        genres=row["genres"]
    )
    for _, row in movies_df.iterrows()
]

# Add Movies to the session
session.bulk_save_objects(movies)

# Load Persons data
persons_file = "name.basics.tsv"
persons_df = pd.read_csv(persons_file, sep="\t", nrows=2000)

# Convert Persons data to a list of Persons objects
persons = [
    Persons(
        nconst=row["nconst"],
        primaryName=row["primaryName"],
        birthYear=row["birthYear"],
        deathYear=row["deathYear"],
        primaryProfession=row["primaryProfession"],
        knownForTitles=row["knownForTitles"]
    )
    for _, row in persons_df.iterrows()
]

# Add Persons to the session
session.bulk_save_objects(persons)


users = [
    Users(
        id=1,
        name="John Doe",
        email="john.doe@example.com",
        password="abc",

    ),
    Users(
        id=2,
        name="Amy Jackson",
        email="amy.jackson@example.com",
        password="abc"),

    Users(
        id=3,
        name="John Smith",
        email="john.smith@example.com",
        password="abc"),
    Users(
        id=4,
        name="Tim Smith",
        email="tim.smith@example.com",
        password="abc"),


]

session.bulk_save_objects(users)

# Commit the session
session.commit()

print("Inserted data into movies and persons tables.")
