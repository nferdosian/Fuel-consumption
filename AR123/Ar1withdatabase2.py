import sqlite3
import pandas as pd
import plotly.express as px
from flask import Flask, render_template, request, g

# Load the dataset
file_path = 'cleaned_fuel_consumption.csv'
data = pd.read_csv(file_path)

# Handle NaN values in the 'COEMISSIONS' column
data['COEMISSIONS'] = data['COEMISSIONS'].fillna(0)  # Replace NaN with 0

app = Flask(__name__)
DATABASE = "user_preferences.db"

# Function to get database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Initialize database
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        # Create the main table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS user_preferences (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          max_fuel REAL,
                          max_emissions REAL)''')

        # Check if migration or updates are needed
        try:
            # Example migration: Adding a new column if it doesn't exist
            cursor.execute("ALTER TABLE user_preferences ADD COLUMN user_notes TEXT")
        except sqlite3.OperationalError:
            # Column already exists; no migration required
            pass

        db.commit()

def create_bar_chart():
    avg_emissions_by_make = data.groupby('MAKE')['COEMISSIONS'].mean().sort_values(ascending=False).head(10)
    fig = px.bar(avg_emissions_by_make, x=avg_emissions_by_make.values, y=avg_emissions_by_make.index,
                 orientation='h', title="Top 10 Manufacturers by Average CO2 Emissions",
                 labels={'x': 'Average CO2 Emissions (g/km)', 'y': 'Manufacturer'},
                 color=avg_emissions_by_make.values, color_continuous_scale='Viridis')
    return fig.to_html(full_html=False, include_plotlyjs="cdn")

def create_scatter_plot():
    fig = px.scatter(data, x='ENGINE SIZE', y='FUEL CONSUMPTION', color='CYLINDERS', size='COEMISSIONS',
                     hover_data=['MAKE', 'TRANSMISSION'], title="Engine Size vs. Fuel Consumption",
                     labels={'ENGINE SIZE': 'Engine Size (L)', 'FUEL CONSUMPTION': 'Fuel Consumption (L/100 km)',
                             'CYLINDERS': 'Cylinders', 'COEMISSIONS': 'CO2 Emissions (g/km)'},
                     size_max=40, color_continuous_scale='Cool')
    return fig.to_html(full_html=False, include_plotlyjs="cdn")

def create_scatter_plot():
    fig = px.scatter(
    data,
    x='ENGINE SIZE',
    y='FUEL CONSUMPTION',
    color='CYLINDERS',
    size='COEMISSIONS',  # Ensure this column has no NaN values
    hover_data=['MAKE', 'TRANSMISSION'],
    title="Engine Size vs. Fuel Consumption",
    labels={
        'ENGINE SIZE': 'Engine Size (L)',
        'FUEL CONSUMPTION': 'Fuel Consumption (L/100 km)',
        'CYLINDERS': 'Cylinders',
        'COEMISSIONS': 'CO2 Emissions (g/km)'
    },
    size_max=40,
    color_continuous_scale='Viridis'  # Replaced 'Cool' with 'Viridis'
)
    return fig.to_html(full_html=False, include_plotlyjs="cdn")


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/bar_chart')
def bar_chart_page():
    return render_template("chart.html", chart_title="Bar Chart", chart=create_bar_chart())

@app.route('/scatter_chart')
def scatter_chart_page():
    return render_template("chart.html", chart_title="Scatter Plot", chart=create_scatter_plot())

@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    recommendations_html = ""
    if request.method == 'POST':
        max_fuel = request.form.get('max_fuel', type=float)
        max_emissions = request.form.get('max_emissions', type=float)

        if max_fuel is not None and max_emissions is not None:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO user_preferences (max_fuel, max_emissions) VALUES (?, ?)",
                           (max_fuel, max_emissions))
            db.commit()
        
        filtered_data = data
        if max_fuel is not None:
            filtered_data = filtered_data[filtered_data['FUEL CONSUMPTION'] <= max_fuel]
        if max_emissions is not None:
            filtered_data = filtered_data[filtered_data['COEMISSIONS'] <= max_emissions]

        if filtered_data.empty:
            recommendations_html = "<p style='color: red;'>No vehicles match your preferences.</p>"
        else:
            recommendations_html = filtered_data[['MAKE', 'ENGINE SIZE', 'FUEL CONSUMPTION', 'COEMISSIONS']].to_html(classes="table table-striped")
    
    return render_template("recommendations.html", recommendations_html=recommendations_html)

@app.route('/summary')
def summary():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT AVG(max_fuel), AVG(max_emissions) FROM user_preferences")
    avg_fuel, avg_emissions = cursor.fetchone()
    return render_template("summary.html", avg_fuel=avg_fuel, avg_emissions=avg_emissions)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=7002, debug=False)

