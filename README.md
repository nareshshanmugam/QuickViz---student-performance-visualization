# QuickViz1

QuickViz1: Data Visualization and Participant Analysis
QuickViz1 is a powerful web-based tool designed to simplify data visualization and participant analysis. This application allows users to upload multiple CSV files, merge them seamlessly, and generate insightful visualizations from the selected data. Along with visual analytics, the system also extracts and displays participant information in a user-friendly format.

This project is ideal for those who need to quickly analyze large datasets, generate charts, and gain insights without the need for manual data merging or visualization using separate tools.

Table of Contents
Features
Technologies
Installation
Usage
Packages Used
Screenshots
License
Features
CSV Upload & Merge: Upload multiple CSV files and automatically merge them for analysis.
Column Selection: Select specific columns from the merged dataset for targeted visualizations.
Dynamic Plot Generation: Generate various types of plots (bar charts, line charts, pie charts, etc.) for better data visualization.
Participant Data Extraction: Automatically extract and display participant information from the datasets.
Secure Access: A login system ensures that only authenticated users can access the dashboard and perform operations.
User-friendly Interface: Built using Bootstrap for an intuitive and responsive design.
Technologies
Backend: Flask (Python)
Frontend: HTML, Bootstrap (for responsive design and styling)
Data Handling: Pandas (for reading, merging, and processing CSV files)
Visualization: Matplotlib and Seaborn (for generating dynamic visualizations)
Authentication: Flask-Login (to handle user authentication and session management)
Storage: File-based handling of uploaded CSV files
Installation
Prerequisites
Python 3.x
Pip (Python package installer)
Usage
Uploading CSV Files:
Navigate to the dashboard.
Upload multiple CSV files.
The application will automatically merge them for analysis.
Visualizing Data:
Select specific columns from the merged data.
Choose a plot type (bar chart, line chart, etc.).
View the generated visualizations along with participant data.
Login Required:
Log in or create an account to access the dashboard and features.
Packages Used
Python Libraries:
Flask: A lightweight WSGI web application framework used to build the backend of the web application.
Pandas: A powerful data manipulation and analysis library used for reading, merging, and processing CSV files.
Matplotlib: A comprehensive library for creating static, animated, and interactive visualizations in Python.
Seaborn: Built on top of Matplotlib, Seaborn is used for making statistical graphics and improving the aesthetics of the plots.
Flask-Login: A user session management tool that provides authentication and session management features.
Jinja2: A templating engine used by Flask to render HTML templates dynamically.
Werkzeug: A comprehensive WSGI web application library that Flask is built on, which handles routing and HTTP requests.
OS & Sys: Used for handling file paths and system operations.
Datetime: For generating timestamps and file names for charts and session handling.
Frontend:
Bootstrap: A responsive CSS framework for creating user-friendly web pages and making sure the application is mobile-friendly
