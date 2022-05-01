def plants_for_soil_type(cursor, soil_type_name):
  """
  List first 10 plants for a given soil type
  Parameters:
    common_name : the common name of the plant
  """

  query = """
    SELECT common_name
    FROM plant
    INNER JOIN favored_soil ON plant_id = plant.id
    JOIN soil_type USING (soil_ID)
    WHERE soil_type.type = '{}'
    LIMIT 10""".format(soil_type_name)
  
  cursor.execute(query)
  resultset = cursor.fetchall()
  if(len(resultset) < 1):
    print("No plants found.")
  else: 
    print('\nPlants fit for {} soil type'.format(soil_type_name))
    for common_name in resultset:
      print(common_name[0])

def view_annual_plants(cursor): 
  """List the view of annual plants that have their season in spring or summer"""

  query = """
  SELECT *
  FROM annual_plants 
  """
  cursor.execute(query)
  resultset = cursor.fetchall()
  if(len(resultset) < 1):
    print("No plants found.")
  else: 
    print('Plant : Season')
    for (common_name, season) in resultset:
      print("{} : {}".format(common_name, season))

def print_plant_details(cursor, plant_name):
  """Print the details of a specific plant"""

  query = """
  SELECT p1.common_name, p1.family, p1.season, p1.soil_moisture, p1.sun_exposure, p2.common_name AS companion_plant, cp.notes AS companion_plant_notes
  FROM plant p1
  JOIN companion_plant cp ON p1.id IN (cp.plant_id, cp.companion_id)
  JOIN plant p2 ON cp.plant_id = p1.id AND p2.id = companion_id
    OR cp.companion_id = p1.id AND p2.id = plant_id
  WHERE p1.common_name = '{}'
  """.format(plant_name)

  cursor.execute(query)
  resultset = cursor.fetchall()
  if(len(resultset) < 1):
    print("No plant found.")
  else:
    for(common_name, family, season, soil_moisture, sun_exposure, companion_plant, companion_plant_notes) in resultset:
      print(
        "\nCommon Name: {} \n"
      "Family: {} \n"
      "Season: {} \n"
      "Soil moisture: {} \n"
      "Sun Exposure: {} \n"
      "Companion Plant: {} \n"
      "Companion Plant Notes: {} \n"
      .format(common_name, family, season, soil_moisture, sun_exposure, companion_plant, companion_plant_notes)
      )

def plant_pest_risks(cursor, plant_name): 
  """Given a common name of a plant, list the pests and possible companions to help mitigate"""

  query="""
  SELECT common_name, GROUP_CONCAT(
  CONCAT(name, "(", pest_type.type, ")")
  SEPARATOR ', '
  ) AS pests
  FROM plant
  JOIN infects ON plant.id = infects.plant_id
  JOIN pest ON infects.pest_id = pest.pest_id
  JOIN pest_type ON pest.type = pest_type.pest_type_id
  WHERE common_name = "{}"
  """.format(plant_name)
  cursor.execute(query)
  resultset = cursor.fetchall()
  if(len(resultset) < 1):
    print("Not found.")
  else: 
    print('\nPlant :  Pests\n')
    for (common_name, pests) in resultset:
      print('{} : {}'.format(common_name, pests))


def most_common_pests(cursor):
  """Print the most common pests and their frequency"""

  query = """
  SELECT pest_type.type, COUNT(pest.pest_id) AS number
  FROM pest_type
  JOIN pest ON pest_type_id = pest.type
  JOIN infects ON infects.pest_id = pest.pest_id
  GROUP BY pest_type.type
  ORDER BY number desc
  """
  cursor.execute(query)
  resultset = cursor.fetchall()
  if(len(resultset) < 1):
    print("No pests were found.")
  else: 
    print('\nPests :  occurrences\n')
    for (type, number) in resultset:
      print('{} : {}'.format(type, number))


def print_soil_types(cursor):
  """
  List all available soil types
  """

  query = """
    SELECT type FROM soil_type
  """

  cursor.execute(query)
  resultset = cursor.fetchall()
  print('Available soil types:')
  for (type) in resultset:
    print(type[0])
