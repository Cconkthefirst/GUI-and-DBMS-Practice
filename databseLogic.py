#====================================================================================
# SOURCES:
# https://doc.qt.io/qtforpython-6/
# https://dev.mysql.com/doc/
# https://realpython.com/qt-designer-python/
# https://www.w3schools.com/sql/
# https://www.geeksforgeeks.org/creating-tables-with-prettytable-library-python/
# https://pypi.org/project/prettytable/
# https://www.w3schools.com/python/python_lambda.asp
# https://www.geeksforgeeks.org/python-lambda-anonymous-functions-filter-map-reduce/
# https://www.pythonguis.com/tutorials/pyqt6-layouts/
# https://regex101.com/
# https://www.geeksforgeeks.org/string-formatting-in-python/
# https://www.w3schools.com/python/python_dictionaries.asp
# https://www.geeksforgeeks.org/python-dictionary/
# https://www.pythonguis.com/tutorials/pyqt6-creating-multiple-windows/
# https://www.pythonguis.com/tutorials/pyqt6-dialogs/
# https://www.youtube.com/watch?v=Cc_zaUbF4LM
# https://www.youtube.com/watch?v=N2JfygnWJaA
#====================================================================================

import pymysql              # Import the pymysql module for database connectivity
import re
from prettytable import *

# Create a cursor for the database connection
workingDb = pymysql.connect(host='localhost', user='root', password='', database='northwind')
workingCrsr = workingDb.cursor()

# Define the columns for the PrettyTable
# I think we need make these formats for each table
table = PrettyTable(['ID', 'Company', 'Last Name', 'First Name', 'E-mail Address', 
                    'Job Title', 'Business Phone', 'Home Phone', 'Mobile Phone',
                    'Fax Number', 'Address', 'City', 'State/Province', 'ZIP/Postal Code',
                    'Country/Region', 'Web Page', 'Notes', 'Attachments'])

# Define a list of predefined queries with their names and SQL queries
predefined_queries = [
    #samples
    {"name": "Query 1", "query": "SELECT ID, `first name`, `last name` FROM `employees`;"},
    {"name": "Query 2", "query": "SELECT ID, `first name`, `last name` FROM `employees` WHERE `first name` LIKE '%I%' OR `last name` LIKE '%I%';"},
    {"name": "Query 3", "query": "SELECT `first name`, `Last name` FROM `employees` WHERE `City` LIKE '%S%';"},
    #MDLT specific Queries:
    #Query 4 return all purchases ever made
    {"name": "Return All Purchases", "query": "SELECT `purchasesID`, `totalPaid`, `paymentType`, `cardnumber`, `productIDs` FROM `purchases` as `p`;"},
    #Query 6 return all customers 
    {"name": "Show all customers", "query": "SELECT `customersID`, `phonenumber`, `address`, `city`, `organizationID`;"},
    #Query 7 return all orginization ID information
    {"name": "Show all organizations", "query": "SELECT `organizationID`, `organizationName`, `contactPerson`, `email`, `phonenumber`, `LicenseID`;"},
    #Query 8 Return all shipments
    {"name": "Show all shipements", 'query': "SELECT `shipmentID`, `companyShipping`, `trackingNumber`, `weight(kg)`, `inventoryCOP`, `shipper`, `shipperHandlerFee`, `importationFee`, `contents`;"},
    #Query 9 Return all suppliers information
    {"name": "Show all supplier information", 'query': "SELECT `supplierID`, `Fname`, `Lname`, `email`, `phoneNumber`, `city`, `productID's`;"},
    #Query 10 Return all licensing information
    {"name": "Show all licensing information", 'query': "SELECR `LicensingID`, `Percent/Royality`, `ContractedStarted`, `Contract Expire`, `ContractURL`;"},
    

    
    
    
    # Add more queries as needed
    #Most important Querries for Analysis:
    #-------------------------------------
    # - Listed Exchange upon purchase
    # - All data on transactions specifically involving cash
    # - Estimate the sales tax for all transactions 
]

  
def save_original_state():   # Begin a transaction to capture the original state 
    workingDb.begin()        # Begin a transaction to capture the original state   
    workingDb.commit()       # Commit the transaction to save the original state


def revert_to_original_state():                                 # Rollback the transaction to revert to the original state
    try:
        workingDb.rollback()                                    # Rollback the transaction to revert to the original state
        print("Database reverted to the original state.")
    except Exception as e:
        print(f"Error reverting to the original state: {e}")


def displayTable(tableName):                                    # Define a function to display a table with the given table name
    sql = f"SELECT * FROM {tableName}; "                        # SQL query to select all columns from the specified table
    workingCrsr.execute(sql)
    rows = workingCrsr.fetchall()                               # Fetch all rows from the result set
    columns = [desc[0] for desc in workingCrsr.description]     # Get the column names (attribute names) from the cursor description
    table = PrettyTable(columns)                                # Create a PrettyTable with column names                             

    # Add rows to the PrettyTable
    for row in rows:
        table.add_row(row)

    # Convert PrettyTable to HTML
    table_html = table.get_html_string(
        format=True,                                            # Apply formatting (including borders)
        border=1,                                               # Include table borders
    )
    return table_html


def updateDatabase(tableName, ID, attribute, newdata):
    #this function will take in the table you are updating
    #the exact entry you want to update this is found by the ID
    #the attibute of that Entry changed to what newdata hold
    #End goal should be to prepair an sql statement that will be ran by the cursor on the database
    #After that the data should be updated, the function can never change the ID though
    #Cant change ID because that is the KEy 
    try:
        if isinstance(newdata, str):                    # Ensure that the attribute value is properly quoted for string types
            newdata = f'{newdata}'

        sql = f"UPDATE {tableName} "                    # Construct the SQL update statement
        sql += f"SET `{attribute}` = '{newdata}' "
        sql += f"WHERE `ID` = {ID}; "
        workingCrsr.execute(sql)                        # Execute the SQL update statement
        workingDb.commit()

    except Exception as e:                              # Handle any exceptions, print an error message, and rollback the changes
        print(f"Error updating the database: {e}")
        workingDb.rollback()


def fetchAllTables():
    try:
        workingCrsr.execute("SHOW TABLES;")             # Execute an SQL query to fetch all table names from the information_schema.tables
        tables = workingCrsr.fetchall()
        table_list = [table[0] for table in tables]     # Extract table names from the result set
        return table_list

    except Exception as e:
        print(f"Error fetching table list: {e}")
        return None


def getTableSchema(tableName):
    workingCrsr.execute(f"DESCRIBE {tableName};")
    columns_info = workingCrsr.fetchall()
    return columns_info                             # Return the column information


def enterData(entry, tableName):
    # ======================================================================================================================
    # Convert the entry into a readable format for the database
    # Send the entry via SQL statement
    # Ensure that data in entry is the proper type
    # Each attribute of an entry is separated by a ',' EX: name,phoneNumber,height
    # If there is a gap in the entry, skip to the next attribute
    # Meaning if the entry is not the same size as the schema, then some attributes have no value
    # Start at the first attribute in entry; if it has no value, set it to the default value from the schema
    # After the code has processed the data of the entry and created the new attribute based on the user's entry,
    # it has finished its job and is done
    # Important Notes: Never update the key values of the table
    # The code to insert the data into the database is missing here
    # ======================================================================================================================
    attributes = entry.split(',')                                               # Split the entry into a list of attributes using ',' as the separator
    schema = getTableSchema(tableName)                                          # Get the schema (column information) for the specified table
    column_names = [column[0] for column in schema]                             # Extract column names from the schema
    matchValue = {}                                                             # Create a dictionary to store attribute-value pairs
    for i in range(len(attributes)):
        if i < len(column_names):                                               # Check if the index i is within the range of column_names
            matchValue[column_names[i]] = attributes[i].strip()
        else:
            raise ValueError(f"Index {i} out of range in attributes")           # Raise a ValueError if the index i is out of range in attributes

    columns = ', '.join([f"`{col}`" for col in matchValue.keys()])              # Joining column names with backticks to ensure proper formatting for SQL identifiers
    values = ', '.join(f"'{value}'" for value in matchValue.values())           # Joining values with single quotes to ensure proper formatting for SQL string values
    sql_statement = f"INSERT INTO {tableName} ({columns}) VALUES ({values});"   # Creating the final SQL statement for the INSERT query, using the provided table name, columns, and values

    try:
        workingCrsr.execute(sql_statement)                                      # Execute the SQL statement to insert data into the specified table
        workingDb.commit()                                                      # Commit the changes to the database
        print(f"Data inserted successfully into {tableName} table.")            # Print a success message
    except Exception as e:
        print(f"Error inserting data into the database: {e}")                   # Handle any exceptions that may occur during the execution of the insert operation
        workingDb.rollback()                                                    # If there was an error, rollback the changes to the state of the database before the insert command


def deleteRow(tableName, ID):
    try:                        
        sql = f"DELETE FROM {tableName} WHERE ID = {ID};"               # Construct the SQL delete statement
        workingCrsr.execute(sql)                                        # Execute the SQL delete statement
        workingDb.commit()                                              # Commit the changes to the database
        print(f"Row with ID {ID} deleted from the {tableName} table.")  # Print the row that was deleted from X table

    except Exception as e:                                              #Error Handling
        print(f"Error deleting row from the database: {e}")             # Handle any exceptions, print an error message, and rollback the changes
        workingDb.rollback()                                            #If there was an error dont execite antyhing rollback to state of db before comand


def createTable(schema):
    match = re.match(r'(\w+)\{([^}]+)\}', schema)    # The schema will be in this format "TableName(attribute1-datatype-, attribute2-datatype-, ...)" - Use regular expression to match the pattern and extract table name and attributes
    if not match:                                    # If the pattern doesn't match, raise a ValueError indicating an invalid schema format
        raise ValueError("Invalid schema format")
    tableName, attributes_str = match.groups()                          # Extract the table name and attributes from the matched groups
    attributes = [attr.strip() for attr in attributes_str.split(',')]   # Split the attributes string into a list of individual attributes
    primaryKey = attributes[0].split('-')[0] 
    sql = f"CREATE TABLE `{tableName}` ("                               # Start building the SQL CREATE TABLE statement with the table name

    for attribute in attributes:                                        # Iterate over each attribute and add it to the SQL statement
        name, dataType = map(str.strip, attribute.split('-'))           # Split the attribute into name and data type    
        sql += f"{name} {dataType}, "                                   # Add the attribute to the SQL statement

    sql += f"PRIMARY KEY (`{primaryKey}`));"     
    print(sql)
    try:
        workingCrsr.execute(sql)                                        # Execute the SQL CREATE TABLE statement
        workingDb.commit()                                              # Commit the changes to the database
        print(f"Table {tableName} created successfully.")               # Inform that dev that table was created 
    except Exception as e:                                              # Case a failure in table building
        print(f"Error creating table in the database: {e}")             # Inform the dev
        workingDb.rollback()                                            # Dont make any changes to the db and rollback to original state


def deleteTable(tableName):
    try:
        sql = f"DROP TABLE {tableName};"                         # Construct the SQL statement to drop (delete) the specified table
        workingCrsr.execute(sql)                                 # Execute the SQL drop table statement using the cursor (assuming 'workingCrsr' is a cursor object)
        workingDb.commit()                                       # Commit the changes to the database
        print(f"Table {tableName} deleted successfully.")        # Print a message indicating that the table was deleted successfully
    except Exception as e:
        print(f"Error deleting table: {e}")                      # Handle any exceptions that may occur during the execution of the drop table operation
        workingDb.rollback()                                     # If there was an error, rollback the changes to the state of the database before the drop table command


def runPredefinedQuery(queryName):
    try:
        query = next(q["query"] for q in predefined_queries if q["name"] == queryName)        # Find the predefined query in the list of predefined_queries based on the queryName
        workingCrsr.execute(query)                                                            # Execute the predefined query using the cursor (assuming 'workingCrsr' is a cursor object)
        rows = workingCrsr.fetchall()                                                         # Fetch all rows from the result set
        columns_info = workingCrsr.description                                                # Assuming that the columns_info is available (you may need to adjust this based on your code structure)
        columns = [desc[0] for desc in columns_info]                                          # Get the column names from the cursor description
        table = PrettyTable(columns)                                                          # Create a PrettyTable with column names

        for row in rows:                                                                      # Add rows to the PrettyTable
            table.add_row(row)

        table_html = table.get_html_string(                                                   # Convert PrettyTable to HTML
            format=True,                                                                      # Apply formatting (including borders)
            border=1,                                                                         # Include table borders
        )

        return table_html                                                                     # Return the HTML representation of the PrettyTable
    except Exception as e:
        print(f"Error running predefined query: {e}")                                         # Handle any exceptions that may occur during the execution of the predefined query
        return f"Error running predefined query: {e}"                                         # If there was an error, you might want to handle it accordingly (e.g., log the error, return an error message, etc.)
