import mysql.connector
from mysql.connector import errorcode

#mydb1 = mysql.connector.connect(
  #host="localhost",
 # user="root",
 # password=""
#)

hostName = "localhost"
databaseUser = "root"
databasePassword = ""
db_name='comp3161FinalProject'
mydb1 = mysql.connector.connect(host= hostName, user=databaseUser, passwd=databasePassword)
mycursor1 = mydb1.cursor()
def create_db(mycursor1):
    try:
        mycursor1.execute("create database {}".format(db_name))
        print("Database Created")
    except mysql.connector.Error as err:
        print("Database creation failed:", err)
        exit(1)
try:
    mydb1.database = db_name
    print('Database {} already exist.'.format(db_name))
except mysql.connector.Error as err:
    # database doesn't exist, create one
    if errorcode.ER_BAD_DB_ERROR == err.errno:
        create_db(mycursor1)
        mydb1.database = db_name


mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="COMP3161FinalProject")
mycursor = mydb.cursor()
mycursor.execute("Show tables;")
myresult = mycursor.fetchall()
tables=['user', 'recipe', 'manual','meal','mealplan','ingredient','measurement','groceryList','kitchensupply']
create = {}
create['user']="CREATE TABLE user (UID INT NOT NULL auto_increment, firstname varchar(255), lastname varchar(255), email varchar(255), password varchar(255), primary key(UID))"

create['Recipe']="CREATE TABLE Recipe (RecipeID int,  DateCreated Date, specification VARCHAR(255), totalcal float,  primary key(RecipeID))"

create['Manual']="CREATE TABLE Manual (ManualID int, steps int, instructions VARCHAR(255), RecipeID int, primary key(ManualID), foreign key(RecipeID) references Recipe(RecipeID) on Delete cascade on update cascade)"

create['Meal']="CREATE TABLE Meal (MealID int, Mimage varchar(255), recipeID int,  primary key(MealID), foreign key(RecipeID) references Recipe(RecipeID))"

create['MealPlan']="CREATE TABLE MealPlan (MPID int, UID int,  primary key(MPID), MealID int, foreign key (UID) references user(UID)  on Delete cascade on update cascade,  foreign key (MealID) references meal(MealID)  on Delete cascade on update cascade)"

create['Ingredient']="CREATE TABLE Ingredient (IngredientID int, IName varchar(255), calories float, primary key(IngredientID))"

create['Measurement']="CREATE TABLE Measurement (MID int, Quantity float, measurements varchar(255),  primary key(MID))"

create['GroceryList']="CREATE TABLE GroceryList(GLID int, IngredientID int,  primary key(GLID))"

create['KitchenSupply']="CREATE TABLE KitchenSupply(IngredientID int, MID int, KSID int, primary key(KSID), foreign key(IngredientID) references ingredient(IngredientID) )"

create['recipeIngredients']="CREATE TABLE RecipeIngredient (RecipeID int not null, IngredientID int not null, MID int not null, servings float, foreign key(RecipeID) references Recipe(RecipeID), foreign key(IngredientID) references ingredient(IngredientID), foreign key(MID) references Measurement(MID))"


for tables in create:
    try:
        mycursor.execute(create[tables])
        print('Table {} created.'.format(tables))
    except mysql.connector.Error as err:
        if errorcode.ER_TABLE_EXISTS_ERROR == err.errno:
            print('Table {} already exists.'.format(tables))



""" for k,v in create:
    if table not in myresult:
        try:
            print("Creating table {}: ".format(table), end='')
            mycursor.execute(create[table])
        except:
            print("Table cant be created")
    else:
        print("table already created") """