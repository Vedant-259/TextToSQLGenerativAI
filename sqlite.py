import sqlite3
## connect to sqlite database
connection = sqlite3.connect("student.db")

#Create a cursor object to insert records , create table

cursor =connection.cursor()

## create the table

table_info = """
Create table STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25), SECTION VARCHAR(25), MARKS INT);

"""
cursor.execute(table_info)

## insert some more records
cursor.execute("""INSERT INTO STUDENT values('vedant', 'WEb tech', 'B', 90) """)
cursor.execute("""INSERT INTO STUDENT values('krish', 'Networking', 'A', 85) """)
cursor.execute("""INSERT INTO STUDENT values('sahil', 'Cyber security', 'A', 95) """)
cursor.execute("""INSERT INTO STUDENT values('pratik', 'Data Science', 'B', 90) """)
cursor.execute("""INSERT INTO STUDENT values('kunal', 'Aiml', 'B', 80) """ )

## Display
print("The inserted data")
data=cursor.execute("""SELECT * FROM STUDENT;""")
for row in data:
    print(row)


# commit the changes
connection.commit()
connection.close()