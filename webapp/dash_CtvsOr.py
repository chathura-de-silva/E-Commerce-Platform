import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from .dbaccess import getCategoriesandOrders

# Sample data

category, orders = getCategoriesandOrders()
df = pd.DataFrame(
    {
        "category": category,
        "orders": orders,
    }
)


def categories_Orders(flask_app):
    dash_app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/dash3/")
    dash_app.layout = html.Div(
        children=[
            html.H1(children="Trending Categories"),
            html.Div(
                children="""
                Categories with highest orders
            """
            ),
            dcc.Graph(id="example-graph"),
        ]
    )

    @dash_app.callback(
        Output("example-graph", "figure"),
        [Input("example-graph", "id")]
    )
    def update_graph(selected_id):
        # Create a bar chart using Plotly Express
        fig = px.bar(df, x="orders", y="category", title="Categories with Orders")
        return fig

    return dash_app
