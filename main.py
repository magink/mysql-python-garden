# Author: Magnus Brink mb224gw

import mysql.connector
import csv, os
from mysql.connector import errorcode
from setup_tables import create_tables
from setup_data import insert_data
from util import pause_for_any_key

from queries import plants_for_soil_type, print_soil_types, view_annual_plants, most_common_pests, print_plant_details, plant_pest_risks

db_srv_config = {
  'host': '127.0.0.1',
  'port': '8889',
  'user': 'root',
  'password': 'root',
}

DB_NAME = "GardenDB"

def connect(db_srv_config):
  """Connect to the database server
  Parameters:
  db_srv_config : dictionary of server settings

  Returns:
  A mysql connection object
  """
  try :
    return mysql.connector.connect(**db_srv_config)
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Wrong username or password")
    print("Couldn't connect to the database. Error: {} ".format(error))
    exit(0)

def setup_datebase():
  """Creates the database, selects it, insert the tables and corresponding data"""
  create_database(DB_NAME)
  select_database(DB_NAME)
  create_tables(cursor)
  insert_data(cnx)

def create_database(db_name):
  """Create a new database"""
  try:
    cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
    print("Database {} created successfully".format(db_name))
  except mysql.connector.Error as err: 
    print("Couldn't create database {} ".format(err))
    exit(0)

def select_database(db_name):
  """Select an existing database"""
  try: 
    cursor.execute("USE {}".format(db_name))
    print("Database {} selected".format(db_name))
  except mysql.connector.Error as error: 
    print("Couldn't select the database {} ".format(error))
    exit(0)

def database_exist():
  """Return True if database with DB_NAME already exist"""
  try:
    cursor.execute("SHOW DATABASES LIKE '{}'".format(DB_NAME))
    if cursor.rowcount > 0: # If it's more than 0 it has be true
      return True
    else :
      return False
  except mysql.connector.Error as error:
    print("Couldn't show databases {}".format(error))

def menu():
  while(True):
    print_menu()
    try :
      selection = int(input("> "))
    except ValueError:
      print("Not a number")
    if(selection == 1):
      print_soil_types(cursor)
      soil_type = input("enter a soil type: ")
      plants_for_soil_type(cursor, soil_type)
    elif(selection == 2):
      view_annual_plants(cursor)
    elif(selection == 3):
      print("selection 3")
      # try :
      plant_name = input("Enter a common name: ")
      print_plant_details(cursor, plant_name)
    elif(selection == 4):
      print("selection 4")
      most_common_pests(cursor)
    elif(selection == 5):
      print("selection 5")
      plant_name = input("Enter a common name: ")
      plant_pest_risks(cursor, plant_name)
    elif(selection == 6):
      print("Quitting...")
      break
    else :
      print("Not a valid selection")
    pause_for_any_key()
 
   
def print_menu():
  print(""""
  \t\t Main menu
  ----------------------------------------
  1: List plants fit for a given soil type.
  2: View all early annual plants.
  3. Choose and view plant details
  4. View the most common types of pests in order
  5. View pest risks for a given plant
  6: Quit
  ----------------------------------------
  """)



"""Main program flow"""
# 1: Connect to database application and get cnx. 
# Global variable. Bad practice but avoids having cnx, cursor 
# in every function mudding up the params that actually matter
cnx = connect(db_srv_config)

# Get the cursor from connection object. Global variable
cursor = cnx.cursor(buffered=True)

# Create database and data if not exist, otherwise just select
if not database_exist() :
  setup_datebase()
else :
  select_database(DB_NAME)
menu()

# Show main menu and enter running loop
## Finally close cursor and connection
# cursor.close() 
cnx.close()
