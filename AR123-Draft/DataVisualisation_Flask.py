import pandas as pd
import plotly.express as px
from flask import Flask, render_template  # Corrected import

# Load and clean the dataset
DATA_FILE = "cleaned_fuel_consumption.csv"  # Replace with your data file
df = pd.read_csv(DATA_FILE)
df.columns = df.columns.str.strip().str.upper()  # Clean column names

# Select numerical columns for statistical calculations
numerical_columns = ['ENGINE SIZE', 'CYLINDERS', 'FUEL CONSUMPTION', 'COEMISSIONS']

# Calculate statistics: mean, median, minimum, and maximum
statistics = pd.DataFrame({
    'Mean': df[numerical_columns].mean(),
    'Median': df[numerical_columns].median(),
    'Minimum': df[numerical_columns].min(),
    'Maximum': df[numerical_columns].max()
})

# Print statistics
print("Statistics:")
print(statistics)

# Visualization 1: Bar Chart (Average Fuel Consumption by Vehicle Make)
avg_fuel_by_make = df.groupby('MAKE')['FUEL CONSUMPTION'].mean().sort_values()
bar_chart = px.bar(
    x=avg_fuel_by_make.index,
    y=avg_fuel_by_make.values,
    labels={"x": "Vehicle Make", "y": "Average Fuel Consumption (L/100km)"},
    title="Average Fuel Consumption by Vehicle Make"
)
bar_chart_html = bar_chart.to_html(full_html=False, include_plotlyjs="cdn")

# Visualization 2: Scatter Plot (Engine Size vs. CO2 Emissions)
scatter_plot = px.scatter(
    df,
    x='ENGINE SIZE',
    y='COEMISSIONS',
    color='CYLINDERS',
    title="Engine Size vs. CO2 Emissions",
    labels={"ENGINE SIZE": "Engine Size (L)", "COEMISSIONS": "CO2 Emissions (g/km)"},
    color_continuous_scale='Viridis'
)
scatter_plot_html = scatter_plot.to_html(full_html=False, include_plotlyjs="cdn")

# Visualization 3: Histogram (Distribution of CO2 Emissions)
histogram = px.histogram(
    df,
    x='COEMISSIONS',
    nbins=20,
    title="Distribution of CO2 Emissions",
    labels={"COEMISSIONS": "CO2 Emissions (g/km)"},
    color_discrete_sequence=['orange']  # Valid color
)
histogram_html = histogram.to_html(full_html=False, include_plotlyjs="cdn")

# Visualization 4: Box Plot (Fuel Consumption by Transmission Type)
box_plot = px.box(
    df,
    x='TRANSMISSION',
    y='FUEL CONSUMPTION',
    title="Fuel Consumption by Transmission Type",
    labels={"TRANSMISSION": "Transmission Type", "FUEL CONSUMPTION": "Fuel Consumption (L/100km)"},
    color_discrete_sequence=px.colors.qualitative.Pastel  # Use a valid color sequence
)
box_plot_html = box_plot.to_html(full_html=False, include_plotlyjs="cdn")  # Fixed typo

# Convert statistics to HTML table
stats_html = statistics.to_html(classes="table table-bordered table-striped", border=0)

# Create Flask web application
app = Flask(__name__)

# Home page with links to individual charts
@app.route('/')
def index():
    return render_template("index.html")

# Page for Bar Chart
@app.route('/bar_chart')
def bar_chart_page():
    return render_template("chart.html", chart_title="Bar Chart", chart=bar_chart_html)

# Page for Histogram (Fixed Route Name)
@app.route('/histogram_chart')  # Fixed spelling error
def histogram_page():
    return render_template("chart.html", chart_title="Histogram", chart=histogram_html)

# Page for Scatter Plot
@app.route('/scatter_chart')
def scatter_chart_page():
    return render_template("chart.html", chart_title="Scatter Plot", chart=scatter_plot_html)

# Page for Scatter Plot
@app.route('/box_plot')
def box_plot_page():
    return render_template("chart.html", chart_title="box Plot", chart=box_plot_html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7002, debug=False)
