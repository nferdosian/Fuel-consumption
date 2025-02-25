import pandas as pd
import plotly.express as px
from flask import Flask, render_template, request
import csv
import os

# Load the dataset
file_path = 'cleaned_fuel_consumption.csv'
data = pd.read_csv(file_path)

# Handle NaN values in the 'COEMISSIONS' column
data['COEMISSIONS'] = data['COEMISSIONS'].fillna(0)  # Replace NaN with 0

app = Flask(__name__)

# CSV file to save user preferences
USER_PREFERENCES_FILE = "user_preferences.csv"

# Initialize CSV file if it doesn't exist
if not os.path.exists(USER_PREFERENCES_FILE):
    with open(USER_PREFERENCES_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'max_fuel', 'max_emissions'])  # Write the header

def create_bar_chart():
    avg_emissions_by_make = data.groupby('MAKE')['COEMISSIONS'].mean().sort_values(ascending=False).head(10)
    fig = px.bar(avg_emissions_by_make, x=avg_emissions_by_make.values, y=avg_emissions_by_make.index,
                 orientation='h', title="Top 10 Manufacturers by Average CO2 Emissions",
                 labels={'x': 'Average CO2 Emissions (g/km)', 'y': 'Manufacturer'},
                 color=avg_emissions_by_make.values, color_continuous_scale='Viridis')
    return fig.to_html(full_html=False, include_plotlyjs="cdn")

def create_scatter_plot():
    fig = px.scatter(
        data,
        x='ENGINE SIZE',
        y='FUEL CONSUMPTION',
        color='CYLINDERS',
        size='COEMISSIONS',
        hover_data=['MAKE', 'TRANSMISSION'],
        title="Engine Size vs. Fuel Consumption",
        labels={
            'ENGINE SIZE': 'Engine Size (L)',
            'FUEL CONSUMPTION': 'Fuel Consumption (L/100 km)',
            'CYLINDERS': 'Cylinders',
            'COEMISSIONS': 'CO2 Emissions (g/km)'
        },
        size_max=40,
        color_continuous_scale='Viridis'
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

        # Save user preferences to CSV file
        with open(USER_PREFERENCES_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            user_id = sum(1 for _ in open(USER_PREFERENCES_FILE))  # Increment user ID based on row count
            writer.writerow([user_id, max_fuel, max_emissions])

        # Filter data based on user preferences
        filtered_data = data
        if max_fuel is not None:
            filtered_data = filtered_data[filtered_data['FUEL CONSUMPTION'] <= max_fuel]
        if max_emissions is not None:
            filtered_data = filtered_data[filtered_data['COEMISSIONS'] <= max_emissions]

        # Generate recommendations
        if filtered_data.empty:
            recommendations_html = "<p style='color: red;'>No vehicles match your preferences.</p>"
        else:
            recommendations_html = filtered_data[['MAKE', 'ENGINE SIZE', 'FUEL CONSUMPTION', 'COEMISSIONS']].to_html(classes="table table-striped")

    return render_template("recommendations.html", recommendations_html=recommendations_html)

@app.route('/summary')
def summary():
    # Calculate summary from the CSV file
    if os.path.exists(USER_PREFERENCES_FILE):
        user_data = pd.read_csv(USER_PREFERENCES_FILE)
        avg_fuel = user_data['max_fuel'].mean()
        avg_emissions = user_data['max_emissions'].mean()
    else:
        avg_fuel = avg_emissions = None

    return render_template("summary.html", avg_fuel=avg_fuel, avg_emissions=avg_emissions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7002, debug=False)
