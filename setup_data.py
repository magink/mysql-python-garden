# Author: Magnus Brink mb224gw
import csv
import mysql.connector
from mysql.connector import errorcode

SOIL_TYPES = "./data/soil_types.csv"
PEST_TYPES = "./data/pest_types.csv"
PESTS = "data/pests.csv"
PLANTS = "data/plants.csv"
FAVORED_SOIL = "data/favored_soil.csv"
COMPANION_PLANTS = "data/companion_plants.csv"
INFECTS = "data/infects.csv"

def insert_data(cnx):
  insert_file(SOIL_TYPES, soil_types_statement(), cnx)
  insert_file(PEST_TYPES, pest_types_statement(), cnx)
  insert_file(PESTS, pests_statement(), cnx)
  insert_file(PLANTS, plants_statement(), cnx)
  insert_file(FAVORED_SOIL, favored_soil_statement(), cnx)
  insert_file(COMPANION_PLANTS, companion_plants_statement(), cnx)
  insert_file(INFECTS, infects_statement(), cnx)

def insert_file(csv_file, statement, cnx):
  """Insert a table into the database
  Parameters:s
    csv_file : csv file with data to insert
    insert_statement : the query for targetting tables and attributes for insert
  """
  cursor = cnx.cursor()
  with open(csv_file, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader) # Skip headers§
    data = []
    for i, row in enumerate(reader):
      if (len(row) == 0): # If row is empty
        continue
      if (row[0] == "NA"): # If name is NA, we skip that tuple and print a message
        print("Tuple {} doesn't have key.  Skipping...".format(i))
        continue
      row = _replace_with_null(row)
      data.append(row) 
    try :
      cursor.executemany(statement, data)
      print("Insert successfull")
    except mysql.connector.Error as err:
      print("Couldn't insert data. {} Error {}".format(statement,err))
      exit(0)
    cnx.commit()

def _replace_with_null(row):
  """We replace NA with NULL"""
  for i in range(len(row)):
    if row[i] == 'na':
        row[i] = None
  return row

def soil_types_statement():
  return """INSERT INTO
  soil_type(soil_id, type)
  VALUES(%s, %s);
  """
def pest_types_statement():
  return """INSERT INTO
  pest_type(pest_type_id, type)
  VALUES(%s, %s);
  """

def pests_statement():
  return """INSERT INTO
  pest(pest_id, type, name)
  VALUES(%s, %s, %s);
  """

def plants_statement():
  return """INSERT INTO
  plant(id, common_name, botanical_name, family, type, lifespan, season, soil_moisture, sun_exposure)
  VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);
  """

def favored_soil_statement():
  return """INSERT INTO
  favored_soil(plant_id, soil_id)
  VALUES(%s, %s);
  """

def companion_plants_statement():
  return """INSERT INTO
  companion_plant(plant_id, companion_id, pest_id, notes)
  VALUES(%s, %s, %s, %s)
  """
def infects_statement():
  return """INSERT INTO
  infects(plant_id, pest_id)
  VALUES(%s, %s)
  """

