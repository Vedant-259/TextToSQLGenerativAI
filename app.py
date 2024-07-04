from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google API key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt, question])
    return response.text.strip()  # Ensure there are no leading/trailing spaces

# Function to retrieve query results from the database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    print(f"Executing SQL query: {sql}")  # Debug print
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        column_names = [description[0] for description in cur.description]  # Get column names
    except sqlite3.OperationalError as e:
        print(f"SQL error: {e}")
        rows = []
        column_names = []
    conn.commit()
    conn.close()
    return rows, column_names

# Define the prompt for the model
prompt = """
You are an expert in converting English questions to SQL codes!
The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION.

For example:
1. How many entries of records are present? 
   SQL: SELECT COUNT(*) FROM STUDENT;
2. Tell me all the students studying in the data science class? 
   SQL: SELECT * FROM STUDENT WHERE CLASS='Data Science';

Ensure the SQL code does not have ''' in the beginning or end of the SQL word in the output.
"""

# Streamlit app
st.set_page_config(page_title="I can retrieve any SQL queries")
st.header("Gemini app to retrieve SQL Data")

# User input
question = st.text_input("Input:", key="input")
submit = st.button("Ask the question")

# If submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    print(f"Generated response: {response}")  # Debug print
    response = response.replace('```sql', '').replace('```', '').replace('SQL:', '').strip()  # Sanitize the response
    
    sql_query = response
    st.write(f"Generated SQL Query: {sql_query}")  # Display the generated SQL query
    
    # Validate the generated SQL query
    if not sql_query.lower().startswith("select"):
        st.error("The generated response is not a valid SELECT SQL query.")
    else:
        # Execute and display the results of the SQL query
        try:
            rows, column_names = read_sql_query(sql_query, "student.db")
            
            if rows:
                st.subheader("The response is:")
                if len(rows) == 1 and len(rows[0]) == 1:  # Check if the result is a single value
                    st.text(f"{rows[0][0]}")  # Display the single value without column names
                else:
                    for row in rows:
                        st.text("\n".join(str(val) for val in row))  # Display each row without column names
            else:
                st.error("No data returned or SQL error.")
        except sqlite3.OperationalError as e:
            st.error(f"SQL error: {e}")
            print(f"SQL error: {e}")
