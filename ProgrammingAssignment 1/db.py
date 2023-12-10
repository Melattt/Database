import mysql.connector
import os
import csv

cnx = mysql.connector.connect(user='root', password='root', 
                              host='127.0.0.1')
cursor = cnx.cursor()

# Name of the database.
DB_NAME = 'Haile'
path = os.getcwd()
print(path)

try:
    cursor.execute('use ' + DB_NAME)
# Exception if the database not found and to create it.
except mysql.connector.Error as e:
    database = input("Database :" + DB_NAME + " is not found, do you want to create it now?(Y/N): ")
    if database == "Y" or database == "y":
        # Generating the database and names.
        table_of_planets = "create table planets (name VARCHAR(255) NOT NULL,rotation_period INT,orbital_period INT,diameter INT, climate nvarchar(20),gravity nvarchar(20),terrain nvarchar(255),surface_water INT,population INT,primary key(name));"
        table_of_species = "create table species (sp_name VARCHAR(255) NOT NULL,classification nvarchar(50),designation nvarchar(50),average_height nvarchar(50),skin_colors nvarchar(50),hair_colors nvarchar(50),eye_colors nvarchar(50),average_lifespan INT,language nvarchar(50),homeworld nvarchar(50),primary key(sp_name));"

        cursor.execute("create database " + DB_NAME + ";")
        cursor.execute("use " + DB_NAME + ";")
        cursor.execute(table_of_planets)
        cursor.execute(table_of_species)
        cursor.execute('SET SESSION sql_mode ="";')
        cursor.execute('SET GLOBAL sql_mode ="";')
        

        # Open files.
        file = open('planets.csv')
        csv1 = csv.reader(file)
        skip_header = True
        for row in csv1:
            if skip_header:
                skip_header = False
                continue
            cursor.execute(
                'Insert into planets(name, rotation_period,orbital_period, diameter, climate, gravity, terrain, surface_water, population)' 'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)', row)
            cursor.execute("commit;")

        # Open files.
        file = open('species.csv')
        skip_header = True
        csv2 = csv.reader(file)
        for row in csv2:
            if skip_header:
                skip_header = False
                continue
            cursor.execute('Insert into species(sp_name, classification, designation, average_height, skin_colors, hair_colors, eye_colors, average_lifespan, language, homeworld)' 'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', row)
            cursor.execute("commit;")

    else:
        # The database will not be created, if the answer is no.
        print("Database " + DB_NAME + " not created!")
        raise SystemExit

# Connected.
if cnx.is_connected():
    print("Database ", DB_NAME, " is connected and data is inserted into it.")

    # Show the menu.
    while True:
        userInput = input("**********************************************************************************\n" +
                          "| 0. Quit                                                                         |\n" +
                          "----------------------------------------------------------------------------------\n" +
                          "| 1. List all planets.                                                            |\n" +
                          "----------------------------------------------------------------------------------\n" +
                          "| 2. Search for planet details.                                                   |\n" +
                          "----------------------------------------------------------------------------------\n" +
                          "| 3. Search for species with height higher than given number.                     |\n" +
                          "----------------------------------------------------------------------------------\n" +
                          "| 4. What is the most likely desired climate of the given species?                |\n" +
                          "----------------------------------------------------------------------------------\n" +
                          "| 5. What is the average lifespan per species classification?                     |\n" +                
                          "**********************************************************************************\n" +
                          " Please choose one option: ")

        # Make sure the input is in the form of a number.
        if userInput.isnumeric():
            menuSelector = int(userInput)

        # If it is 1, make a list of the planets.
        if menuSelector == 1:
            cursor.execute("select name from planets;")
            print("**********************************************************************************")
            print("|                          Planets name                                          |")
            print("----------------------------------------------------------------------------------")
            for name in cursor:
                print('%35s' % name)
            print("**********************************************************************************")
            input("Press any key to go to the main menu: ")

        # If it is 2, look up information about the planet.
        elif menuSelector == 2:
            print("----------------------------------------------------------------------------------")
            planet_name = input(" Enter name of the planet: ")
            cursor.execute("select name,rotation_period,orbital_period,diameter,climate,gravity,terrain,surface_water,population from planets where name=" +
                           "'"+planet_name+"'"+";")
            print("*****************************************************************************************************************************************************")
            print("|   Name   | Rotation_period | Orbital_period | Diameter   |    Climate      |   Gravity     |        Terrain       |   Surface_water   | Population|")
            print("-----------------------------------------------------------------------------------------------------------------------------------------------------")
            for name, rotation_period, orbital_period, diameter, climate, gravity, terrain, surface_water, population in cursor:
                print('%5s' % name, '%10s' % rotation_period, '%20s' % orbital_period, '%12s' % diameter, '%20s' %
                      climate, '%13s' % gravity, '%25s' % terrain, '%10s' % surface_water, '%20s' % population)
            print("*****************************************************************************************************************************************************")
            input("Press any key to go to the main menu: ")

        # If it is 3, look for species that are higher than the specified number.
        elif menuSelector == 3:
            print("----------------------------------------------------------------------------------")
            height = int(
                input("Enter the average height of the species: "))
            cursor.execute(
                "select sp_name, average_height from species where average_height > " + str(height)+";")
            print("**********************************************************************************")
            print("|        Species name              |            Average height                   |")
            print("----------------------------------------------------------------------------------")
            for sp_name, average_height in cursor:
                print('%20s' % sp_name, '%35s' % average_height)
            print("**********************************************************************************")
            input("Press any key to go to the main menu: ")

        # If it is 4, display the species' most likely preferred climate.
        elif menuSelector == 4:
            species_name = input("Enter the name of the species: ")
            cursor.execute(
                "select climate from planets where name in (select homeworld from species where sp_name="+"'"+species_name+"'"+");")
            print("**********************************************************************************")
            print("|                                Climate                                         |")
            print("----------------------------------------------------------------------------------")
            for climate in cursor:
                print('%15s' % climate)
            print("**********************************************************************************")
            input("Press any key to go to the main menu: ")

        # If it is 5, show the average lifespan per species classification.
        elif menuSelector == 5:
            cursor.execute(
                "select classification ,AVG(average_lifespan) from species GROUP BY classification;")
            print("**********************************************************************************")
            print("|         Species classification       |        Average lifespan                 |")
            print("----------------------------------------------------------------------------------")
            for classification, average_lifespan in cursor:
                print('%25s' % classification, '%35s' % average_lifespan)
            print("**********************************************************************************")
            input("Press any key to go to the main menu: ")
        # If it is 0, quit.
        elif menuSelector == 0:
            cnx.close()
            break
