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
            html.H1(children="Product Sales Quantities"),
            html.Div(
                children="""
                Product vs Quantity
            """
            ),
            html.P("Select From Year:"),
            dcc.Dropdown(
                id="from_year",
                options=[
                    {"label": year[0], "value": year[0]} for year in years
                ],
                value=years[-1][0],

            ),
            html.P("Select To Year:"),
            dcc.Dropdown(
                id="to_year",
                options=[
                    {"label": year[0], "value": year[0]} for year in years
                ],
                value=selected_value,

            ),
            dcc.Graph(id="example-graph"),
        ]
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
        return fig

    return dash_app
