import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from .dbaccess import getProductQuantityList, select_year

df = pd.DataFrame(
    {
        "Sales": [],
        "month": [],
    }
)


# def getProductQuantityList(from_year , to_year):
#     return ['How', 'The', 'Refrig', 'Coffee', 'Denim', 'Cotton', 'DellXPS', 'MacBook', 'Samsung', 'iPhone'], [20, 20, 20, 20, 20, 20, 20, 20, 20, 20]

def dash_productVStime(flask_app):
    dash_app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/dash2/")
    years, selected_value = select_year()

    dash_app.layout = html.Div(
    children=[
        html.H1(
            "Product Sales Quantities",
            style={
                'textAlign': 'center',
                'font-family': 'Arial',
                'font-size': '28px',
                'margin-bottom': '10px',  # Add some spacing below the title
            }
        ),
        html.Div(
            "Product vs Quantity",
            style={
                'textAlign': 'center',
                'font-family': 'Arial',
                'font-size': '20px',
                'margin-bottom': '20px',  # Add more spacing below this text
            }
        ),
        html.P(
            "Select From Year:",
            style={
                'font-family': 'Arial',
                'font-size': '20px',
            }
        ),
        dcc.Dropdown(
            id="from_year",
            options=[
                {"label": year[0], "value": year[0]} for year in years
            ],
            value=years[-1][0],
            style={'width': '50%', 'font-family': 'Arial', 'font-size': '20px'}
        ),
        html.P(
            "Select To Year:",
            style={
                'font-family': 'Arial',
                'font-size': '20px',
            }
        ),
        dcc.Dropdown(
            id="to_year",
            options=[
                {"label": year[0], "value": year[0]} for year in years
            ],
            value=selected_value,
            style={'width': '50%', 'font-family': 'Arial', 'font-size': '20px'}
        ),
        dcc.Graph(
            id="example-graph",
            style={'width': '100%'},
            config={'displayModeBar': False}  # Hide the plotly toolbar
        ),
    ],
    style={
        'maxWidth': '800px',
        'margin': '0 auto',
        'padding': '20px'  # Add padding around the entire content
    }
)


    @dash_app.callback(
        Output("example-graph", "figure"),
        [Input("from_year", "value"),
         Input("to_year", "value")]
    )
    def update_graph(from_year, to_year):
        product_list, quantity_list = getProductQuantityList(from_year, to_year)

        df = pd.DataFrame({"products": product_list, "quantity": quantity_list})

        fig = px.bar(df, x="quantity", y="products", title=f"product sales quantity over {from_year} to {to_year}")
          
        fig.update_layout(

        font=dict(family="Arial", size=18),
        legend=dict(font=dict(family="Arial", size=15)),
   
    )
        return fig

    return dash_app
