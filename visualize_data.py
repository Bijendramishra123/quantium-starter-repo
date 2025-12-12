import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px
from datetime import datetime

# Load processed sales data
df = pd.read_csv("output/combined_sales.csv")

# Convert 'date' column to datetime
df["date"] = pd.to_datetime(df["date"])

# Aggregate sales per day
daily_sales = df.groupby("date")["sales"].sum().reset_index()

# Create line chart
fig = px.line(
    daily_sales,
    x="date",
    y="sales",
    title="Pink Morsel Sales Over Time",
    labels={"date": "Date", "sales": "Total Sales"}
)

# Highlight price increase date
price_increase_date = datetime(2021, 1, 15)
fig.add_shape(
    type="line",
    x0=price_increase_date,
    x1=price_increase_date,
    y0=0,
    y1=daily_sales["sales"].max(),
    line=dict(color="red", dash="dash")
)

# Add annotation
fig.add_annotation(
    x=price_increase_date,
    y=daily_sales["sales"].max(),
    text="Price Increase",
    showarrow=True,
    arrowhead=3,
    ay=-40
)

# Dash app
app = Dash(__name__)
app.layout = html.Div([
    html.H1("Pink Morsel Sales Visualiser", style={"textAlign": "center"}),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)
