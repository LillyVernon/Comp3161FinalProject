import mysql.connector

#mydb1 = mysql.connector.connect(
  #host="localhost",
 # user="root",
 # password=""
#)

hostName = "localhost"
databaseUser = "root"
databasePassword = ""

mydb1 = mysql.connector.connect(host= hostName, user=databaseUser, passwd=databasePassword)
mycursor1 = mydb1.cursor()
mycursor1.execute("show databases")
print(mycursor1)

#db="COMP3161FinalProject" 
''' if db not in result:
    mycursor1.execute("CREATE DATABASE COMP3161FinalProject;")
else:
    print("database already exist")
         '''

mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="COMP3161FinalProject")
mycursor = mydb.cursor()
mycursor.execute("Show tables;")
myresult = mycursor.fetchall()
tables=['user', 'recipe', 'manual','meal','mealplan','ingredient','measurement','groceryList','kitchensupply']
create = {}
create['user']="CREATE TABLE user (UID INT NOT NULL auto_increment, firstname varchar(255), lastname varchar(255), email varchar(255), password varchar(255), primary key(UID))"
create['Recipe']="CREATE TABLE Recipe (RecipeID VARCHAR(255), DateCreated Date, specification VARCHAR(255), totalcal float,  primary key(RecipeID))"
create['Manual']="CREATE TABLE Manual (ManualID VARCHAR(255), instructions VARCHAR(255),  primary key(ManualID))"
create['Meal']="CREATE TABLE Meal (MealID varchar(255), Mimage varchar(255),  primary key(MealID))"
create['MealPlan']="CREATE TABLE MealPlan (MPID varchar(255), UID varchar(255),  primary key(MPID))"
create['Ingredient']="CREATE TABLE Ingredient (IngredientID varchar(255), IName varchar(255), calories float, primary key(IngredientID))"
create['Measurement']="CREATE TABLE Measurement (MID varchar(255), Quantity varchar(255), measurements float,  primary key(MID))"
create['GroceryList']="CREATE TABLE Meal (GLID varchar(255), IngredientID varchar(255),  primary key(GLID))"
create['KitchenSupply']="CREATE TABLE Meal (IngredientID varchar(255), MID varchar(255), KSID varchar(255), primary key(KSID))"

for table in create:
    if table not in myresult:
        try:
            #print("Creating table {}: ".format(table), end='')
            mycursor.execute(create[table])
        except:
            print("Table cant be created")
    else:
        print("table already created")