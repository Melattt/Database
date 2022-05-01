import mysql.connector
import csv

def createTables():
    cnx = mysql.connector.connect( user = 'root' , password = 'root' ,host = '127.0.0.1', db='cattle')
    cursor = cnx.cursor()
    if cnx.is_connected():
        cursor.execute("use cattle;")
        cursor.execute("CREATE TABLE IF NOT EXISTS vaccine(vaccine_id INT NOT NULL AUTO_INCREMENT, vaccine_name NVARCHAR(100), PRIMARY KEY(vaccine_id));")
        file =  open('vaccine.csv')
        csv_data = csv.reader(file)
        skipHeader = True
        for row in csv_data:
            if skipHeader:
                skipHeader = False
                continue
            cursor.execute('INSERT INTO vaccine(vaccine_id,vaccine_name)' 'VALUES(%s,%s)', row)
            cursor.execute("commit;")
        cursor.execute("CREATE TABLE IF NOT EXISTS sex(sex_id INT NOT NULL AUTO_INCREMENT, sex_name NVARCHAR(10), PRIMARY KEY(sex_id));")
        file =  open('sex.csv')
        csv_data = csv.reader(file)
        skipHeader = True
        for row in csv_data:
            if skipHeader:
                skipHeader = False
                continue
            cursor.execute('INSERT INTO sex(sex_id,sex_name)' 'VALUES(%s,%s)', row)
            cursor.execute("commit;")
        cursor.execute("CREATE TABLE IF NOT EXISTS calves(calf_id INT NOT NULL AUTO_INCREMENT,calf_tag NVARCHAR(20),date_of_birth NVARCHAR(50),vaccine_id INT,sex_id INT,mother_cow INT, PRIMARY KEY(calf_id));")
        file =  open('calves.csv')
        csv_data = csv.reader(file)
        skipHeader = True
        for row in csv_data:
            if skipHeader:
                skipHeader = False
                continue
            cursor.execute('INSERT INTO calves(calf_tag,date_of_birth,vaccine_id,sex_id,mother_cow)' 'VALUES(%s, %s, %s, %s, %s)', row)
            cursor.execute("commit;")
        cursor.execute("CREATE TABLE IF NOT EXISTS adult_cattle(cattle_id INT NOT NULL AUTO_INCREMENT,cattle_tag NVARCHAR(10), color NVARCHAR(100), weight INT, breed NVARCHAR(200), date_of_birth NVARCHAR(20), sex_id INT NOT NULL, PRIMARY KEY(cattle_id), FOREIGN KEY (sex_id) REFERENCES sex(sex_id));")
        file =  open('adult_cattle.csv')
        csv_data = csv.reader(file)
        skipHeader = True
        for row in csv_data:
            if skipHeader:
                skipHeader = False
                continue
            cursor.execute('INSERT INTO adult_cattle(cattle_tag,color,weight,breed,date_of_birth,sex_id)' 'VALUES( %s, %s, %s, %s, %s, %s)', row)
            cursor.execute("commit;")
    
        


try:
    cnx = mysql.connector.connect( user = 'root' , password = 'root' ,host = '127.0.0.1', db='cattle')
except mysql.connector.Error as e:
        print(e)
        cnx = mysql.connector.connect( user = 'root' , password = 'root' ,host = '127.0.0.1')
        cursor = cnx.cursor()
        cursor.execute("CREATE DATABASE cattle")
        createTables()
        
# Connected.
if cnx.is_connected():
    cursor = cnx.cursor()
    cursor.execute("use cattle;")
    print("Database is now connected.")

    # Display menu.
    while True:
        select = input( "---------------------------------------------------------------------------\n"+
                        "1. To group by breed all adult cattle on the farm.\n"+
                        "2. To list all male and female calves on the farm.\n"+
                        "3. To search for a breed and list its adult cattle and calves.\n"+
                        "4. To search for a calf by tag and list the vaccinations the calf recieved.\n"+
                        "5. To get the average weight of adult cattle using VIEW.\n"+
                        "0. Exit\n"
                        "---------------------------------------------------------------------------\n")
        
        # Check if the input is a number.
        if select.isnumeric():
            menu = int(select)

            # To group by breed all Adult cattle on the farm.
            if menu == 1:
                cursor = cnx.cursor()
                cursor.execute("select cattle_tag, breed, sex_name from adult_cattle INNER JOIN sex ON adult_cattle.sex_id = sex.sex_id GROUP BY breed;")
                print("------------------------------------------------------------------------------------")
                print("      Cattle tag        |              Breed                 |          Sex         ")
                print("------------------------------------------------------------------------------------")
                for cattle_tag, breed, sex_name in cursor:
                    print('%15s' % cattle_tag, '%35s' % breed, '%25s' % sex_name)
                print("------------------------------------------------------------------------------------")
                input("Press any key to go to the main menu")

            # To list all male and female calves on the farm.
            elif menu == 2:
                cursor = cnx.cursor()
                cursor.execute("select calf_tag, sex_name from calves INNER JOIN sex ON calves.sex_id = sex.sex_id;")
                print("----------------------------------------------------------")
                print("        Calf tag          |          Sex                  ")
                print("----------------------------------------------------------")
                for calf_tag, sex_name in cursor:
                    print('%15s' % calf_tag, '%25s' % sex_name)
                print("------------------------------------------------------------------")
                input("Press any key to go to the main menu")
            
            # To search for a breed and list its adult cattle and calves.
            elif menu == 3:
                print("---------------------------------------------------------------------")
                breed = input("Enter the breed of the cattle: ")
                print(breed)
                cursor = cnx.cursor()
                cursor.execute("select cattle_tag,breed,calf_tag,calves.date_of_birth from adult_cattle INNER JOIN calves ON calves.mother_cow = adult_cattle.cattle_id  where adult_cattle.breed = "+"'" + breed + "'"+" ;")
                print("----------------------------------------------------------------------")
                print("   Cattle tag   |       Breed       |    Calf tag   |  Date of birth  ")
                print("----------------------------------------------------------------------")
                for cattle_tag, breed, calf_tag, date_of_birth in cursor:
                    print('%10s' % cattle_tag, '%20s' % breed, '%15s' % calf_tag, '%15s' % date_of_birth)
                print("-----------------------------------------------------------------------")
                input("Press any key to go to the main menu")

            # To search for a calf by tag and list the vaccinations the calf recieved.
            elif menu == 4:
                print("----------------------------------------------------------")
                calf_tag = input("Enter the name of the calf tag: ")
                cursor = cnx.cursor()
                print("----------------------------------------------------------")
                print("    Calf tag   |       Vaccination                        ")
                print("----------------------------------------------------------")
                cursor.execute("select calf_tag,vaccine.vaccine_name from calves INNER JOIN vaccine ON calves.vaccine_id = vaccine.vaccine_id where calves.calf_tag =" +"'" + calf_tag +"'"+" ;")
                for calf_tag, vaccine in cursor:
                    print('%10s' % calf_tag, '%35s' % vaccine)
                print("----------------------------------------------------------")
                input("Press any key to go to the main menu")

            # To get the average weight of adult cattle using VIEW.
            elif menu == 5:
                cursor = cnx.cursor()
                try:
                    cursor.execute("CREATE VIEW cattle_weight AS select cattle_tag,weight from adult_cattle;")
                    cursor.execute("select AVG(weight) from cattle_weight;")
                    print("----------------------")
                    for cattle_weight in cursor:
                        print('%10s' % cattle_weight)
                    print("----------------------")
                    input("Press any key to go to the main menu")
                except:
                    cursor.execute("select AVG(weight) from cattle_weight;")
                    print("----------------------")
                    for weight in cursor:
                        print('%10s' % weight)
                    print("----------------------")
                    input("Press any key to go to the main menu")
            elif menu == 0:
                cnx.close()
                break

