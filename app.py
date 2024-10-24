from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import pandas as pd
import seaborn as sns
import os
import uuid
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for plots
import matplotlib.pyplot as plt
from flask import send_file, flash, redirect, url_for

app = Flask(__name__, template_folder='templates')
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret')
login_manager = LoginManager()
login_manager.init_app(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Basic authentication check
        if username == 'admin' and password == 'password':
            login_user(User(username))
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('dashboard'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'warning')
        return redirect(url_for('dashboard'))
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    flash('File uploaded successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    columns_info = {}
    merged_columns = []
    dataframes = []

    if request.method == 'POST' and 'files' in request.files:
        uploaded_files = request.files.getlist('files')

        for file in uploaded_files:
            if file and file.filename.endswith('.csv'):
                try:
                    df = pd.read_csv(file)
                    if not df.empty:
                        dataframes.append(df)
                        columns_info[file.filename] = df.columns.tolist()
                    else:
                        flash(f"The file '{file.filename}' is empty and will be skipped.", 'warning')
                except Exception as e:
                    flash(f"Error reading '{file.filename}': {str(e)}", 'danger')

        if len(dataframes) > 1:
            merged_df = pd.concat(dataframes, axis=0)
            merged_columns = merged_df.columns.tolist()
            session['uploaded_files'] = [os.path.join(UPLOAD_FOLDER, file.filename) for file in uploaded_files]

    return render_template('dashboard.html', columns_info=columns_info, merged_columns=merged_columns)

@app.route('/visualize', methods=['GET', 'POST'])
@login_required
def visualize():
    if request.method == 'POST':
        # Get data from the form
        selected_file = request.form.get('selected_file')
        columns = request.form.getlist('columns')  # Handling multiple columns
        plot_type = request.form.get('plot_type')

        # Load CSV file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], selected_file)
        df = pd.read_csv(file_path)

        # Generate the plot and get participant data
        chart_path = generate_chart_path()
        participant_data = generate_dynamic_plot(df[columns], plot_type, chart_path)

        return render_template('visualization.html', chart_path=chart_path, participant_data=participant_data)

    return redirect(url_for('dashboard'))
 # For GET requests, return the dashboard

@app.route('/visualize_merged', methods=['POST'])
@login_required
def visualize_merged():
    merged_columns = request.form.getlist('merged_columns')
    plot_type = request.form.get('plot_type')

    if not merged_columns:
        flash("Please select columns for visualization.", 'warning')
        return redirect(url_for('dashboard'))

    merged_file_paths = session.get('uploaded_files', [])
    if not merged_file_paths:
        return redirect(url_for('dashboard'))

    # Read and concatenate CSV files into a single DataFrame
    merged_df = pd.concat([pd.read_csv(file_path) for file_path in merged_file_paths], ignore_index=True)
    
    # Validate selected columns against merged DataFrame columns
    valid_merged_columns = [col for col in merged_columns if col in merged_df.columns]
    
    if not valid_merged_columns:
        flash("Selected columns do not exist in the merged data.", 'warning')
        return redirect(url_for('dashboard'))

    # Filter the DataFrame to include only the valid columns
    df = merged_df[valid_merged_columns]

    # Check if the "Name" column exists in the selected columns
    if "Name" in valid_merged_columns:
        # Extract participant names from the "Name" column
        participants = df["Name"].tolist()
    else:
        # If "Name" is not present, default to the first column
        participants = df.iloc[:, 0].tolist() if not df.empty else []

    # Generate the chart path and create the plot
    chart_path = generate_chart_path()
    generate_dynamic_plot(df, plot_type, chart_path)

    # Render the visualization page with the chart and participant details
    return render_template('visualization_merged.html', chart_path=chart_path, participants=participants)

def generate_dynamic_plot(df, plot_type, chart_path):
    """Generate and save the plot based on the selected type and display participant names below the graph."""
    numeric_df = df.select_dtypes(include=['number'])

    if numeric_df.empty:
        flash("No numeric data available to plot.", 'warning')
        return {}

    plt.figure(figsize=(10, 6))
    participant_data = {}

    # Handle bar plot
    if plot_type == 'bar':
        numeric_df.plot(kind='bar', ax=plt.gca(), color='skyblue')
        plt.title('Bar Plot', fontsize=16)

        # Store participant names and scores for tooltip (assuming index contains participant names)
        participant_data = {
            'participants': df.index.tolist(),  # Assuming the index contains participant names
            'scores': numeric_df.iloc[:, 0].tolist()  # Assuming the first column contains scores
        }

    # Handle line plot
    elif plot_type == 'line':
        numeric_df.plot(kind='line', marker='o', ax=plt.gca(), color='orange')
        plt.title('Line Plot', fontsize=16)

        # Store participant names and scores
        participant_data = {
            'participants': df.index.tolist(),
            'scores': numeric_df.iloc[:, 0].tolist()
        }

    # Handle pie chart
    elif plot_type == 'pie' and numeric_df.shape[1] == 1:
        numeric_df.iloc[:, 0].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
        plt.title('Pie Chart', fontsize=16)

        # Store categories and percentages for tooltip
        participant_data = {
            'categories': numeric_df.iloc[:, 0].value_counts().index.tolist(),
            'percentages': numeric_df.iloc[:, 0].value_counts(normalize=True).mul(100).round(1).tolist()
        }

    # Handle scatter plot (requires at least 2 numeric columns)
    elif plot_type == 'scatter' and numeric_df.shape[1] >= 2:
        plt.scatter(numeric_df.iloc[:, 0], numeric_df.iloc[:, 1], color='purple', alpha=0.6)
        plt.title('Scatter Plot', fontsize=16)
        plt.xlabel(numeric_df.columns[0])
        plt.ylabel(numeric_df.columns[1])

        # Store X and Y values for tooltip
        participant_data = {
            'x_values': numeric_df.iloc[:, 0].tolist(),
            'y_values': numeric_df.iloc[:, 1].tolist()
        }

    # Handle histogram
    elif plot_type == 'histogram' and numeric_df.shape[1] >= 1:
        numeric_df.hist(bins=30, ax=plt.gca(), color='green', alpha=0.7)
        plt.title('Histogram', fontsize=16)

        # Store histogram data
        participant_data = {
            'bins': numeric_df.iloc[:, 0].value_counts().index.tolist(),
            'frequencies': numeric_df.iloc[:, 0].value_counts().tolist()
        }

    # Handle box plot
    elif plot_type == 'box' and numeric_df.shape[1] >= 1:
        sns.boxplot(data=numeric_df, ax=plt.gca())
        plt.title('Box Plot', fontsize=16)

        # Store quartile data for tooltip
        participant_data = {
            'min': numeric_df.min().tolist(),
            'q1': numeric_df.quantile(0.25).tolist(),
            'median': numeric_df.median().tolist(),
            'q3': numeric_df.quantile(0.75).tolist(),
            'max': numeric_df.max().tolist()
        }

    # Handle heatmap
    elif plot_type == 'heatmap':
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=plt.gca())
        plt.title('Heatmap', fontsize=16)

        # Store correlation matrix data
        participant_data = {
            'correlation_matrix': numeric_df.corr().to_dict()
        }

    # Add participant names below the plot
    participant_names = df["Name"].tolist()
    scores = numeric_df.iloc[:, 0].tolist()  # Assuming the first numeric column represents scores
    participant_data = dict(zip(participant_names, scores))

  

    plt.tight_layout()
    plt.savefig(chart_path, bbox_inches='tight')
    plt.close()

    return participant_data


def generate_chart_path():
    """Generate a unique chart path."""
    return f'static/{uuid.uuid4().hex}.png'
@app.route('/download')
@login_required
def download():
    file_path = "Data Visualize Project\Downloads"  # Replace with the actual path to the processed file
    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        flash(f"Error downloading file: {str(e)}", "danger")
        return redirect(url_for('dashboard'))
if __name__ == '__main__':
    app.run(debug=True)
