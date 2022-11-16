import unittest
import sqlite3
import json
import os
# starter code

# Create Database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


# Creates list of species ID's and numbers
def create_species_table(cur, conn):

    species = ["Rabbit",
    "Dog",
    "Cat",
    "Boa Constrictor",
    "Chinchilla",
    "Hamster",
    "Cobra",
    "Parrot",
    "Shark",
    "Goldfish",
    "Gerbil",
    "Llama",
    "Hare"
    ]

    cur.execute("DROP TABLE IF EXISTS Species")
    cur.execute("CREATE TABLE Species (id INTEGER PRIMARY KEY, title TEXT)")
    for i in range(len(species)):
        cur.execute("INSERT INTO Species (id,title) VALUES (?,?)",(i,species[i]))
    conn.commit()

# TASK 1
# CREATE TABLE FOR PATIENTS IN DATABASE
def create_patients_table(cur, conn):
    cur.execute("DROP TABLE IF EXISTS Patients")
    cur.execute("CREATE TABLE Patients (pet_id INTEGER PRIMARY KEY, name TEXT, species_id NUMBER, age INTEGER, cuteness INTEGER, aggressiveness NUMBER)")
    conn.commit()

# ADD FLUFFLE TO THE TABLE
def add_fluffle(cur, conn):
    # since Fluffle is a rabbit, the species_id is 0 (found from the Species table)
    cur.execute("INSERT INTO Patients (pet_id, name, species_id, age, cuteness, aggressiveness) VALUES (0, 'Fluffle', 0, 3, 90, 100)")
    conn.commit()
    # could also use question mark / tuple notation to add values
    # cur.execute("INSERT INTO Patients (pet_id, name, species_id, age, cuteness, aggressiveness) VALUES (?, ?, ?, ?, ?, ?)", (0, 'Fluffle', 0, 3, 90, 100))
    # ^^ this is safer

# TASK 2
# CODE TO ADD JSON TO THE TABLE
# ASSUME TABLE ALREADY EXISTS
def add_pets_from_json(filename, cur, conn):
    
    # WE GAVE YOU THIS TO READ IN DATA
    f = open(filename)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)

    # THE REST IS UP TO YOU
    patient_id = 1 #since Fluffle is patient_id 0, start with 1

    for item in json_data: #looping through each patient in the json file
        name = item['name']
        species = item['species']
        age = int(item['age'])
        cuteness = int(item['cuteness'])
        aggressiveness = item['aggressiveness']
        # creating variables to match the ones in the json file
    
        cur.execute("SELECT id FROM Species WHERE title = ?", (species, ))
        species_id = int(cur.fetchone()[0])
        # refer to Species table to match species with species_id
        # (species, ) is a tuple
        # fetchone gives us one 
        print((patient_id, name, species_id, age, cuteness, aggressiveness)) # tuple of length 6

        cur.execute("INSERT INTO Patients (pet_id, name, species_id, age, cuteness, aggressiveness) VALUES (?, ?, ?, ?, ?, ?)", (patient_id, name, species_id, age, cuteness, aggressiveness))

        patient_id += 1 #new for each patient
    conn.commit()


# TASK 3
# CODE TO OUTPUT NON-AGGRESSIVE PETS
def non_aggressive_pets(aggressiveness, cur, conn):
    cur.execute("SELECT name FROM Patients WHERE aggressiveness <= ?", (aggressiveness, ))
    rows = cur.fetchall()
    print(rows)
    non_agg_list = []
    for row in rows:
        non_agg_list.append(row[0])
    return non_agg_list
    



def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('animal_hospital.db')
    create_species_table(cur, conn)

    create_patients_table(cur, conn)
    add_fluffle(cur, conn)
    add_pets_from_json('pets.json', cur, conn)
    ls = (non_aggressive_pets(10, cur, conn))
    print(ls)
    
    
if __name__ == "__main__":
    main()

