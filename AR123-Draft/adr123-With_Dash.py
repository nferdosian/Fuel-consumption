
from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd

# Load the dataset
file_path = 'cleaned_fuel_consumption.csv'
data = pd.read_csv(file_path)

# Handle NaN values in the 'COEMISSIONS' column
data['COEMISSIONS'] = data['COEMISSIONS'].fillna(0)  # Replace NaN with 0

# Initialize the Dash app
app = Dash(__name__)

# Interactive Visualization: Bar Chart and Scatter Plot
avg_emissions_by_make = data.groupby('MAKE')['COEMISSIONS'].mean().sort_values(ascending=False).head(10)
bar_chart = px.bar(
    avg_emissions_by_make,
    x=avg_emissions_by_make.values,
    y=avg_emissions_by_make.index,
    orientation='h',
    title="Top 10 Manufacturers by Average CO2 Emissions",
    labels={'x': 'Average CO2 Emissions (g/km)', 'y': 'Manufacturer'},
    color=avg_emissions_by_make.values,
    color_continuous_scale='Viridis'
)

scatter_plot = px.scatter(
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

# Layout for the dashboard
app.layout = html.Div([
    html.H1("Vehicle Data Dashboard", style={'textAlign': 'center'}),

    # Interactive Visualizations
    html.Div([
        html.H2("Top Manufacturers by CO2 Emissions"),
        dcc.Graph(figure=bar_chart),

        html.H2("Engine Size vs. Fuel Consumption"),
        dcc.Graph(id='scatter-plot', figure=scatter_plot),
    ]),

    # Form or Poll Section
    html.Div([
        html.H2("User Preferences Form"),
        html.Label("Preferred Maximum Fuel Consumption (L/100 km):"),
        dcc.Input(id='fuel-input', type='number', placeholder='e.g., 10', debounce=True),

        html.Label("Preferred Maximum CO2 Emissions (g/km):"),
        dcc.Input(id='emissions-input', type='number', placeholder='e.g., 200', debounce=True),

        html.Button('Submit Preferences', id='submit-button', n_clicks=0),
        html.Div(id='form-response', style={'marginTop': '20px'})
    ], style={'marginTop': '50px'}),

    # Recommendations Section
    html.Div([
        html.H2("Vehicle Recommendations"),
        html.Div(id='recommendations-output', style={'marginTop': '20px'})
    ])
])

# Callback for Recommendations
@app.callback(
    Output('recommendations-output', 'children'),
    Input('submit-button', 'n_clicks'),
    State('fuel-input', 'value'),
    State('emissions-input', 'value')
)
def generate_recommendations(n_clicks, max_fuel, max_emissions):
    if n_clicks > 0:
        filtered_data = data
        if max_fuel is not None:
            filtered_data = filtered_data[filtered_data['FUEL CONSUMPTION'] <= max_fuel]
        if max_emissions is not None:
            filtered_data = filtered_data[filtered_data['COEMISSIONS'] <= max_emissions]

        if filtered_data.empty:
            return html.Div("No vehicles match your preferences.", style={'color': 'red'})

        # Create a table of recommendations
        recommendations = filtered_data[['MAKE', 'ENGINE SIZE', 'FUEL CONSUMPTION', 'COEMISSIONS']]
        return html.Table([
            html.Thead(html.Tr([html.Th(col) for col in recommendations.columns])),
            html.Tbody([
                html.Tr([html.Td(row[col]) for col in recommendations.columns])
                for _, row in recommendations.iterrows()
            ])
        ])
    return "Submit your preferences to see recommendations."

# Run the app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7002, debug=False)