QuickViz - Student Performance Visualization
QuickViz is a web-based tool designed to simplify data visualization and participant analysis, especially for handling and analyzing student performance data. 
It enables users to upload multiple CSV files, merge them seamlessly, and generate insightful visualizations quickly and efficiently.

Features
CSV Upload & Merge: Effortlessly upload multiple CSV files and merge them for combined analysis.
Column Selection: Select specific columns from the merged dataset for targeted visualizations.
Dynamic Plot Generation: Generate various types of visualizations like bar charts, line charts, pie charts, etc.
Participant Data Extraction: Extract and display participant information in a user-friendly format.
Secure Access: Login system that ensures only authenticated users can access the dashboard.
User-friendly Interface: Responsive design using Bootstrap.
Technologies
Backend: Flask (Python)
Frontend: HTML, Bootstrap
Data Handling: Pandas (for CSV reading and processing)
Visualization: Matplotlib and Seaborn
Authentication: Flask-Login
Installation
Prerequisites
Python (version 3.x)
Pip (Python package installer)
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/QuickViz.git
cd QuickViz
Install required packages:

bash
Copy code
pip install -r requirements.txt
Run the application:

bash
Copy code
python app.py
The application will be accessible at http://127.0.0.1:5000.
Usage
Uploading CSV Files:

Navigate to the dashboard, where you can upload multiple CSV files.
The files will be automatically merged for further analysis.
Visualizing Data:

Select the columns you want to analyze.
Choose a plot type (e.g., bar chart, line chart).
View the visualizations and participant data.
Login Requirement:

You must log in or create an account to access the dashboard.
Packages Used
Flask: For creating the backend of the web application.
Pandas: For handling and processing CSV files.
Matplotlib & Seaborn: For generating and styling visualizations.
Flask-Login: For user authentication and session management.
Jinja2: For rendering dynamic HTML templates.
Werkzeug: For routing and HTTP request handling.
Datetime, OS & Sys: For system and file management.
