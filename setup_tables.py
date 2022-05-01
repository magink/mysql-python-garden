# Author: Magnus Brink mb224gw


import mysql.connector
from mysql.connector import errorcode

def create_tables(cursor):
  insert_table(soil_type_table(), cursor)
  insert_table(pest_type_table(), cursor)
  insert_table(pest_table(), cursor)
  insert_table(plant_table(), cursor)
  insert_table(companion_plant_table(), cursor)
  insert_table(favored_soil_table(), cursor)
  insert_table(infects_table(), cursor)
  create_view(annual_plants_view(), cursor)

def insert_table(sql_table_query, cursor):
  executeQuery(sql_table_query, cursor, "table")

def create_view(create_view_query, cursor): 
  executeQuery(create_view_query, cursor, "view")

def executeQuery(query, cursor, type):
  try : 
    cursor.execute(query)
  except mysql.connector.Error as err:
    print("Could't create {} {}. Error{}".format(type,query,err))
    exit(0)
  print("{} created successfully".format(type))

""">>>Create table queries<<<"""

def soil_type_table():
  return """
  CREATE TABLE `soil_type` (
    `soil_id` int,
    `type` varchar(50),
    PRIMARY KEY (`soil_id`)
  );
  """
def pest_type_table():
  return """
    CREATE TABLE `pest_type` (
      `pest_type_id` int,
      `type` varchar(50),
      PRIMARY KEY (`pest_type_id`)
    );
  """
def pest_table():
  return """
    CREATE TABLE `pest` (
      `pest_id` int,
      `type` int,
      `name` varchar(50),
      PRIMARY KEY (`pest_id`),
      FOREIGN KEY (`type`) REFERENCES `pest_type`(`pest_type_id`)
    );
  """

def plant_table():
  return """
    CREATE TABLE `plant` (
      `id` int,
      `common_name` varchar(200),
      `botanical_name` varchar(200),
      `family` varchar(50),
      `type` varchar(50), 
      `lifespan` varchar(50),
      `season` varchar(50),
      `soil_moisture` varchar(50),
      `sun_exposure` varchar(50),
      PRIMARY KEY (`id`)
    );
  """
def favored_soil_table():
  return """
    CREATE TABLE `favored_soil` (
      `plant_id` int,
      `soil_id` int,
      FOREIGN KEY (`plant_id`) REFERENCES `plant`(`id`),
      FOREIGN KEY (`soil_id`) REFERENCES `soil_type`(`soil_id`)
    );
  """

def companion_plant_table():
  return """
    CREATE TABLE `companion_plant` (
      `plant_id` int NOT NULL,
      `companion_id` int NOT NULL,
      `pest_id` int,
      `notes` text,
      FOREIGN KEY (`plant_id`) REFERENCES `plant`(`id`),
      FOREIGN KEY (`companion_id`) REFERENCES `plant`(`id`),
      FOREIGN KEY (`pest_id`) REFERENCES `pest`(`pest_id`)
    );
  """
def infects_table():
  return """
    CREATE TABLE `infects` (
      `plant_id` int,
      `pest_id` int
    );
  """
def annual_plants_view():
  return """
  CREATE OR REPLACE VIEW annual_plants AS 
  SELECT common_name, season
  FROM plant
  WHERE plant.lifespan = "annual" AND plant.season = "spring" OR season = "summer"
  ORDER BY season
  """