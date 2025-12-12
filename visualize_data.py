from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load combined sales data
df = pd.read_csv("output/combined_sales.csv")
df["date"] = pd.to_datetime(df["date"])

# Initialize Dash app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Pink Morsel Sales Visualiser",
            style={"textAlign": "center", "color": "#2C3E50", "fontFamily": "Arial"}),

    html.Div([
        html.Label("Select Region:",
                   style={"fontWeight": "bold", "margin-right": "10px", "fontSize": "18px"}),
        dcc.RadioItems(
            id="region-selector",
            options=[
                {"label": "North", "value": "north"},
                {"label": "East", "value": "east"},
                {"label": "South", "value": "south"},
                {"label": "West", "value": "west"},
                {"label": "All", "value": "all"}
            ],
            value="all",
            inline=True,
            style={"margin-bottom": "20px"}
        )
    ], style={"textAlign": "center", "margin-top": "20px"}),

    dcc.Graph(id="sales-chart",
              style={"margin": "auto", "width": "90%", "border": "1px solid #ccc",
                     "padding": "10px", "boxShadow": "2px 2px 5px #888"})
])

# Callback for region filter
@app.callback(
    Output("sales-chart", "figure"),
    Input("region-selector", "value")
)
def update_chart(region):
    if region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["region"].str.lower() == region]

    daily_sales = filtered_df.groupby("date")["sales"].sum().reset_index()
    fig = px.line(daily_sales, x="date", y="sales",
                  title="Pink Morsel Sales Over Time",
                  labels={"date": "Date", "sales": "Total Sales"})

    # Price increase line
    price_increase_date = pd.to_datetime("2021-01-15")
    fig.add_shape(
        type="line",
        x0=price_increase_date,
        x1=price_increase_date,
        y0=0,
        y1=daily_sales["sales"].max(),
        line=dict(color="red", dash="dash")
    )
    fig.add_annotation(
        x=price_increase_date,
        y=daily_sales["sales"].max(),
        text="Price Increase",
        showarrow=True,
        arrowhead=3,
        ay=-40
    )
    return fig

# Run app
if __name__ == "__main__":
    app.run(debug=True)
