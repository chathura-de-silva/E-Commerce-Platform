import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from .dbaccess import product_list, get_product_sales

df = pd.DataFrame(
    {
        "Sales": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    }
)


def sales_for_product(flask_app):
    dash_app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/dash4/")
    id_product = product_list()
    dash_app.layout = html.Div(
    children=[
        html.H1(
            "Sales throughout the year",
            style={
                'textAlign': 'center',
                'font-family': 'Arial',
                'font-size': '28px',  # Increase the font size
                'margin-bottom': '10px',
            }
        ),
        html.Div(
            "Select the product:",
            style={
                'font-family': 'Arial',
                'font-size': '20px',  # Increase the font size
            }
        ),
        dcc.Dropdown(
            id="products-dropdown",
            options=[
                {"label": product, "value": id} for id, product in id_product
            ],
            value=id_product[0][0],  # Set default value
            style={'width': '50%', 'font-family': 'Arial', 'font-size': '20px'},  # Increase the font size
        ),
        dcc.Graph(
            id="example-graph",
            style={'width': '100%'},
            config={'displayModeBar': False}  # Hide the plotly toolbar
        ),
        html.Div(
            id="highest-month-text",
            style={
                'font-family': 'Arial',
                'font-size': '25px',  # Increase the font size
                'margin-top': '20px',  # Add some spacing above this element
            }
        ),
    ],
    style={
        'maxWidth': '800px',
        'margin': '0 auto',
        'padding': '20px',
    }
)


    # Callback to update graph based on selected product
    @dash_app.callback(
        [Output("example-graph", "figure"), Output("highest-month-text", "children")],
        [Input("products-dropdown", "value")]
    )
    def update_graph(value):
        new_sales = get_product_sales(value)
        # Update the DataFrame with the new sales values
        df = pd.DataFrame(
            {
                "Sales": new_sales,
                "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            }
        )

        # Find the month with the highest sales
        highest_month = df.loc[df["Sales"].idxmax()]["month"]

        # Create the updated graph
        fig = px.bar(df, x="month", y="Sales", title=f"Monthly Sales for selected product:")
          
        fig.update_layout(

        font=dict(family="Arial", size=18),
        legend=dict(font=dict(family="Arial", size=15)),
   
    )

        return fig, f" Month with Highest Sales :   {highest_month}"

    return dash_app
