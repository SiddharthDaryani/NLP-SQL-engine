from logger import logging
from transformers import pipeline
import mysql.connector
import re


try:
    nl2sql = pipeline(
    "text2text-generation",
    model="gaussalgo/T5-LM-Large-text2sql-spider"
    )
    logging.info("Loaded Salesforce/T5_base_Spider model successfully.")
except Exception as e:
    logging.error(f"Failed to load Salesforce/T5_base_Spider model: {e}")
    raise

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="0000",
        database="tshirt_store"
    )
    logging.info("Connected to MySQL database successfully.")
except Exception as e:
    logging.error(f"Failed to connect to MySQL database: {e}")
    raise

def build_prompt(question):
    schema = "products(id, name, color, size, quantity)"
    return f"Database schema: {schema}\nQuestion: {question}"



def generate_sql(prompt):
    generated = nl2sql(prompt, max_new_tokens=128)
    output = generated[0]['generated_text'].strip()
    logging.info(f"Model raw output: {output}")
    return output


# ... rest of your existing code for is_valid_sql, execute_sql etc.


def is_valid_sql(sql_query, allowed_tables=['products']):
    sql_lower = sql_query.lower()
    if not sql_lower.startswith(('select', 'insert', 'update', 'delete', 'with')):
        return False
    
    # Only allow queries referencing allowed tables
    tokens = sql_lower.replace(",", " ").split()
    tables_in_query = [t for t in allowed_tables if t in tokens]
    if not tables_in_query:
        return False
    
    # Disallow known hallucinated table names
    banned_tables = ['columns', 'sql', 'information_schema']
    if any(banned in sql_lower for banned in banned_tables):
        return False
    
    return True



def execute_sql(sql_query):
    cursor = db.cursor(dictionary=True)
    cursor.execute(sql_query)
    result = cursor.fetchall()
    cursor.close()  # Close cursor after use
    # Don't close db here if reused across requests
    return result




def clean_generated_sql_output(output):
    output = output.strip().lower()
    # Remove any prefix like "query:", "sql:", etc.
    for prefix in ['query:', 'sql:', 'answer:', 'using a sql query']:
        if output.startswith(prefix):
            output = output[len(prefix):].strip()

    # Extract SQL starting with SELECT ... till end (or semicolon)
    match = re.search(r'(select.*?;|select.*)', output, re.DOTALL | re.IGNORECASE)
    if match:
        output = match.group(0).strip()
    return output


