# QuickViz1
Data Visualization and Participant Analysis
This project is a web application built using Flask for visualizing merged datasets and displaying participant information. Users can upload CSV files, select columns for visualization, and view the generated charts along with participant data.

Table of Contents
Features
Technologies
Installation
Usage
Screenshots
License
Features
Upload multiple CSV files and merge them.
Select specific columns to visualize from the merged data.
Generate different types of plots such as bar charts, line charts, etc.
Display participant data extracted from the uploaded files.
Simple and intuitive user interface.
Secure login required to access the dashboard and features.
Technologies
Backend: Flask (Python)
Frontend: HTML, Bootstrap (for styling)
Data Handling: Pandas (for CSV merging and processing), Matplotlib/Seaborn (for visualization)
Authentication: Flask-Login
Storage: Filesystem-based CSV handling
Installation
Prerequisites
Python 3.x
Pip (Python package installer)
Steps
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/repository-name.git
cd repository-name
Create and activate a virtual environment (optional but recommended):

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Run the application:

bash
Copy code
flask run
Open your browser and navigate to:

arduino
Copy code
http://127.0.0.1:5000
Usage
Uploading CSV Files: Navigate to the dashboard and upload multiple CSV files. The application will merge them and allow you to select specific columns for visualization.
Visualizing Data: After selecting the columns and plot type, the application generates a chart and displays it along with participant data.
Login Required: Make sure to create an account or log in to access the dashboard.
Screenshots
Dashboard

Visualization
