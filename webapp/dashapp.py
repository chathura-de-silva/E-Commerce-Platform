import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import random
from .dbaccess import Quarterly_sales, select_year

# Sample data
df = pd.DataFrame(
    {
        "Sales": [0, 0, 0, 0],
        "Quarters": ["Q1", "Q2", "Q3", "Q4"],
    }
)


# Sample function to calculate sales based on the selected year
# def Quarterly_sales(selected_year):
#     # Replace this with your actual logic to calculate sales based on the selected year
#     # For demonstration, just returning the same sales values for all years
#     return [random.randint(1, 100) for _ in range(4)]

def create_dash_application(flask_app):
    dash_app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/dash/")
    years, selected_value = select_year()
    dash_app.layout = html.Div(
        children=[
            html.H1("Total Quarterly Sales Over Years", style={'textAlign': 'center', 'font-family': 'Arial', 'font-size': '24px'}),
            html.Div("Select a year", style={'font-family': 'Arial', 'font-size': '20px'}),
            
            dcc.Dropdown(
                id="year-dropdown",

                options=[
                    {"label": year[0], "value": year[0]} for year in years
                ],
                value=selected_value,  # Set default value
                style={'width': '50%', 'font-family': 'Arial', 'font-size': '20px', 'border-radius': '15px'},
            ),
            dcc.Graph(id="example-graph"),
        ]
    )

    # Callback to update graph based on selected year
    @dash_app.callback(
        Output("example-graph", "figure"),
        [Input("year-dropdown", "value")]
    )
    def update_graph(selected_year):
        # Call the calc_sales function to get the new sales values
        new_sales = Quarterly_sales(selected_year)

        # Update the DataFrame with the new sales values
        df["Sales"] = new_sales

        # Create the updated graph
        fig = px.bar(df, x="Quarters", y="Sales", color="Quarters", barmode="group",
                     title=f"Sales in each quarter for {selected_year}")
        
        fig.update_layout(

        font=dict(family="Arial", size=18),
        legend=dict(font=dict(family="Arial", size=15)),
   
    )

        return fig

    return dash_app
