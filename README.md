# Artistic Commission Tracker
A web application for artists to track clients, commissions, and payments. This project allows direct insertion of data from the frontend to the MySQL database through a Flask backend.

Project Structure
artistic-commission-tracker/
├── static/
│   └── script.js           # JavaScript for form handling and table data
├── templates/
│   └── final.html          # Main HTML template
├── app.py                  # Flask application with routes
├── db.py                   # Database connection configuration
├── schema.sql              # SQL database schema
└── style.css               # CSS styles
Setup Instructions
1. Set Up the Database
First, set up your MySQL database using the provided schema:

bash
## Log into MySQL
mysql -u root -p

## Run the schema file (while in MySQL)
source schema.sql
Alternatively, you can use a MySQL client to run the schema.sql file.

2. Install Python Dependencies
Make sure you have Python and pip installed, then run:

bash
pip install flask mysql-connector-python
3. Configure Database Connection
Edit the db.py file to match your MySQL credentials:

python
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        database='art_commission_db'
    )
    return connection
4. Project File Structure
Make sure your project has the following structure:

Create a static folder and place script.js inside it
Create a templates folder and move the HTML file into it, renamed as final.html
Keep app.py, db.py, and style.css in the root directory
5. Run the Application
Execute the following command to start the Flask application:

bash
python app.py
The application will be available at http://localhost:5000

Features
Client Management: Add and view client information
Commission Tracking: Create new commissions and track their status
Payment Processing: Record and manage payments for commissions
Responsive UI: Clean, artistic design that works on various screen sizes
Real-time Updates: Tables update automatically when new data is added
How It Works
When a user submits a form, JavaScript intercepts the submission
The data is sent to the Flask backend via fetch API
The Flask route receives the data and inserts it into the MySQL database
Upon successful insertion, the tables are refreshed with the updated data
Technologies Used
Frontend: HTML, CSS, JavaScript
Backend: Flask (Python)
Database: MySQL
Design: Custom CSS with responsive design
