from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
import spacy
import re
from flask_cors import CORS

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")
CORS(app)

@app.route('/')
def home():
    return "Flask is working!"

def execute_query(query, params=()):
    """Executes an SQL query and returns results."""
    conn = sqlite3.connect("company.db")
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
    except Exception as e:
        print(f"SQL ERROR: {str(e)}")  # Debugging output
        result = None
    finally:
        conn.close()
    return result

def normalize_department(dept):
    """Maps common synonyms to department names."""
    synonyms = {
        "tech": "engineering",
        "software": "engineering",
        "sales team": "sales",
        "hr team": "hr",
        "finance team": "finance",
        "marketing team": "marketing"
    }
    return synonyms.get(dept, dept)  # Return mapped name or original

def extract_info(user_input):
    """Extracts intent, department, and date from user queries dynamically."""
    doc = nlp(user_input.lower())  # Convert query to lowercase for consistency

    # Extracting Department Names
    departments = ["engineering", "marketing", "sales", "finance", "hr", "tech", "software"]
    detected_department = None
    for token in doc:
        if token.text in departments:
            detected_department = normalize_department(token.text)

    # Extracting Date
    detected_date = extract_date(user_input)

    # Extracting Keywords for Intent
    hiring_keywords = {"hired", "joined", "recruited", "started", "began"}
    salary_keywords = {"salary", "payroll", "wages", "compensation", "total pay"}
    manager_keywords = {"manager", "lead", "head", "supervisor"}
    list_employees_keywords = {"list", "show", "employees", "all"}
    intent = None
    for token in doc:
        if token.text in hiring_keywords:
            intent = "hiring"
        elif token.text in salary_keywords:
            intent = "salary"
        elif token.text in manager_keywords:
            intent = "manager"
        elif token.text in list_employees_keywords:
            intent = "list_employees"

    return {
        "intent": intent,
        "department": detected_department,
        "date": detected_date
    }

def extract_date(user_input):
    """Attempts to extract a date in multiple formats and converts it to YYYY-MM-DD."""
    date_formats = ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%m-%d-%Y"]
    match = re.search(r"\d{1,4}[-/]\d{1,2}[-/]\d{1,4}", user_input)  # Match date patterns with - or /
    if match:
        date_str = match.group()
        for format in date_formats:
            try:
                date = datetime.strptime(date_str, format)
                return date.strftime("%Y-%m-%d")  # Return date in YYYY-MM-DD format
            except ValueError:
                continue
    return None  # Return None if no valid date is found

@app.route('/query', methods=['POST'])
def query():
    """Handles user queries and returns relevant data from the SQLite database."""
    user_input = request.json.get("query", "").lower()

    if not user_input:
        return jsonify({"error": "No query provided"}), 400

    try:
        extracted_info = extract_info(user_input)  # Use NLP to extract intent, department, and date
        intent = extracted_info["intent"]
        department = extracted_info["department"]
        date = extracted_info["date"]

        if not intent:
            return jsonify({"error": "Sorry, I don't understand this query. Try asking about employees, salaries, or managers."}), 400

        # Handle salary query when department is missing
        if intent == "salary":
            if not department:
                return jsonify({
                    "error": "Please specify a department for the salary query. Example: 'What is the total salary expense for HR?'"
                }), 400
            
            query = "SELECT SUM(salary) FROM employees WHERE LOWER(department) = ?"
            data = execute_query(query, (department,))

            if data and data[0][0] is not None:
                return jsonify({
                    "message": f"The total salary for {department} is:",
                    "total_salary_expense": data[0][0]
                })
            else:
                return jsonify({
                    "message": f"No salary data found for the {department} department."
                })

        # Handle hiring query
        elif intent == "hiring":
            if not date:
                return jsonify({"error": "Missing date in query. Please specify a valid date for hiring queries."}), 400
            query = "SELECT name FROM employees WHERE DATE(hire_date) > ?"
            data = execute_query(query, (date,))
            if data:
                return jsonify({
                    "message": f"Here are the employees hired after {date}:",
                    "employees": [row[0] for row in data]
                })
            else:
                return jsonify({"message": f"No employees were hired after {date}."})

        # Handle manager query
        elif intent == "manager":
            if not department:
                return jsonify({"error": "Missing department in query. Please specify a valid department."}), 400
            query = "SELECT manager FROM departments WHERE LOWER(name) = ?"
            data = execute_query(query, (department,))
            if data:
                return jsonify({"manager": data[0][0]})
            else:
                return jsonify({"message": "Manager not found for this department."})

        # Handle employees listing query
        elif intent == "list_employees":
            if not department:
                return jsonify({"error": "Missing department in query. Please specify a valid department."}), 400
            query = "SELECT name FROM employees WHERE LOWER(department) = ?"
            data = execute_query(query, (department,))
            return jsonify({
                "message": f"Here are the employees in the {department} department:",
                "employees": [row[0] for row in data] if data else ["No employees found."]
            })

        else:
            return jsonify({"error": "Sorry, I don't understand this query. Try asking about employees, salaries, or managers."}), 400

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
