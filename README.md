# **Chat Assistant - Employee Management System**

## **Overview**
This project is a Flask-based **employee management system** that provides an interactive **chatbot interface** to query employee details, department information, and salary details. It utilizes **Natural Language Processing (NLP)** with `spaCy`, `SQLite` for database management, and `Flask` for backend API integration. The frontend is built using **HTML, CSS, and JavaScript (Axios for API requests).**

## **Features**
- **Employee Queries**: Get details about employees by department.
- **Salary Queries**: Fetch total salary expense for a department.
- **Hiring Queries**: Retrieve employees hired after a given date.
- **Manager Queries**: Identify the manager of a department.
- **User-Friendly Interface**: Simple web-based UI with interactive chatbot functionality.
- **NLP Processing**: Extracts key details like intent, department, and dates from user input.

## **Technologies Used**
### **Backend**
- Flask
- SQLite
- spaCy (NLP)
- Flask-CORS

### **Frontend**
- HTML
- CSS (**Pinky Page UI** 🎀)
- JavaScript (Axios for API requests)

### **Database**
- SQLite

## **Installation and Setup**
```# 1. Clone the Repository
git clone https://github.com/bubbles1001/brand_new_chat_b0t
cd your-repo
```

# 2. Create a Virtual Environment
```
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```
# 3. Install Dependencies
```
pip install -r requirements.txt
```
# 4. Setup the Database
```
python create_database.py
```
# 5. Run the Flask Backend
```
python app.py
```
Backend will start running at http://127.0.0.1:5000/

# 6. Start the Frontend
```
cd sensor
node server.js
```
Frontend will be available at http://localhost:3000/

# API Endpoints

# 1. Home Page
# Endpoint: GET /
# Returns a confirmation message that the server is running.

# 2. Query API
# Endpoint: POST /query
# Request Format:
```
 {
   "query": "Who is the manager of sales?"
 }
```
# Response Format:
```
 {
   "manager": "Alice"
 }
```
# 3. Error Handling
# If the query is invalid, the API returns an appropriate error message.
```
 {
   "error": "Please specify a department for the salary query."
 }
```
# File Structure
```
# ├── app.py                # Flask API Backend
# ├── create_database.py    # SQLite Database Setup
# ├── company.db            # SQLite Database File
# ├── sensor/               # Frontend Code
# │   ├── server.js         # Node.js Server for Frontend
# │   ├── index.html        # Frontend UI
# │   ├── style.css         # Stylesheet
# │   ├── favicon.ico       # Favicon
# ├── README.md             # Project Documentation
# └── requirements.txt      # Python Dependencies
```
# Future Enhancements
- Add authentication and user roles.
- Improve NLP processing with advanced models.
- Implement a more responsive and interactive UI though the colour is pink we can make it more vibrant .

# Contributors
# Name - V Sai Pradyumna  
👩‍💻 **Bubbles1001** - [GitHub Profile](https://github.com/bubbles1001)

# License
# This project is licensed under the MIT License.

