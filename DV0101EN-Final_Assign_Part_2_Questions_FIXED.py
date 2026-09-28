#!/usr/bin/env python
# coding: utf-8

"""Final Assignment Part 2: dashboard with Plotly and Dash."""

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


DATA_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/"
    "historical_automobile_sales.csv"
)
data = pd.read_csv(DATA_URL)

app = dash.Dash(__name__)
app.title = "Automobile Statistics Dashboard"

dropdown_options = [
    {"label": "Yearly Statistics", "value": "Yearly Statistics"},
    {
        "label": "Recession Period Statistics",
        "value": "Recession Period Statistics",
    },
]
year_list = list(range(1980, 2024))


# TASK 2.1: Add a meaningful dashboard title.
# TASK 2.2: Add the report-type and year dropdown menus.
# TASK 2.3: Add a division for graph output.
app.layout = html.Div(
    [
        html.H1(
            "Automobile Sales Statistics Dashboard",
            style={"textAlign": "center", "color": "#503D36", "fontSize": 24},
        ),
        html.P(
            "Select a statistical report type and year to display the graphs.",
            style={"textAlign": "center", "color": "#503D36", "fontSize": 18},
        ),
        html.Div(
            [
                html.Label("Select Statistics:"),
                dcc.Dropdown(
                    id="dropdown-statistics",
                    options=dropdown_options,
                    value="Recession Period Statistics",
                    placeholder="Select a report type",
                    style={
                        "width": "80%",
                        "padding": "3px",
                        "fontSize": 20,
                        "textAlignLast": "center",
                    },
                ),
            ]
        ),
        html.Div(
            [
                html.Label("Select Year:"),
                dcc.Dropdown(
                    id="select-year",
                    options=[{"label": year, "value": year} for year in year_list],
                    value=1980,
                    placeholder="Select a year",
                    style={
                        "width": "80%",
                        "padding": "3px",
                        "fontSize": 20,
                        "textAlignLast": "center",
                    },
                ),
            ]
        ),
        html.Div(id="output-container", className="chart-grid"),
    ]
)


# TASK 2.4: Disable the year dropdown for recession statistics and enable it
# for yearly statistics.
@app.callback(
    Output("select-year", "disabled"),
    Input("dropdown-statistics", "value"),
)
def update_input_container(selected_statistics):
    return selected_statistics != "Yearly Statistics"


@app.callback(
    Output("output-container", "children"),
    [
        Input("dropdown-statistics", "value"),
        Input("select-year", "value"),
    ],
)
def update_output_container(selected_statistics, input_year):
    # TASK 2.5: Create and display four Recession Report graphs.
    if selected_statistics == "Recession Period Statistics":
        recession_data = data[data["Recession"] == 1]

        yearly_rec = (
            recession_data.groupby("Year", as_index=False)["Automobile_Sales"]
            .mean()
        )
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x="Year",
                y="Automobile_Sales",
                title="Average Automobile Sales during Recession Periods",
            )
        )

        average_sales = (
            recession_data.groupby("Vehicle_Type", as_index=False)[
                "Automobile_Sales"
            ].mean()
        )
        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title="Average Vehicles Sold by Vehicle Type during Recessions",
            )
        )

        advertising_data = (
            recession_data.groupby("Vehicle_Type", as_index=False)[
                "Advertising_Expenditure"
            ].sum()
        )
        R_chart3 = dcc.Graph(
            figure=px.pie(
                advertising_data,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title="Advertising Expenditure by Vehicle Type during Recessions",
            )
        )

        unemployment_data = (
            recession_data.groupby(
                ["unemployment_rate", "Vehicle_Type"], as_index=False
            )["Automobile_Sales"].mean()
        )
        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemployment_data,
                x="unemployment_rate",
                y="Automobile_Sales",
                color="Vehicle_Type",
                barmode="group",
                title="Effect of Unemployment Rate on Vehicle Type and Sales",
            )
        )

        return [
            html.Div(
                className="chart-item",
                children=[
                    html.Div(R_chart1, style={"width": "50%"}),
                    html.Div(R_chart2, style={"width": "50%"}),
                ],
                style={"display": "flex"},
            ),
            html.Div(
                className="chart-item",
                children=[
                    html.Div(R_chart3, style={"width": "50%"}),
                    html.Div(R_chart4, style={"width": "50%"}),
                ],
                style={"display": "flex"},
            ),
        ]

    # TASK 2.6: Create and display four Yearly Report graphs.
    if selected_statistics == "Yearly Statistics" and input_year is not None:
        yearly_data = data[data["Year"] == input_year]

        yearly_sales = data.groupby("Year", as_index=False)["Automobile_Sales"].mean()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yearly_sales,
                x="Year",
                y="Automobile_Sales",
                title="Yearly Average Automobile Sales",
            )
        )

        monthly_sales = (
            yearly_data.groupby("Month", as_index=False)["Automobile_Sales"].sum()
        )
        Y_chart2 = dcc.Graph(
            figure=px.line(
                monthly_sales,
                x="Month",
                y="Automobile_Sales",
                title=f"Total Monthly Automobile Sales in {input_year}",
            )
        )

        vehicle_sales = (
            yearly_data.groupby("Vehicle_Type", as_index=False)[
                "Automobile_Sales"
            ].mean()
        )
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                vehicle_sales,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title=f"Average Vehicles Sold by Vehicle Type in {input_year}",
            )
        )

        yearly_advertising = (
            yearly_data.groupby("Vehicle_Type", as_index=False)[
                "Advertising_Expenditure"
            ].sum()
        )
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                yearly_advertising,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title=f"Advertising Expenditure by Vehicle Type in {input_year}",
            )
        )

        return [
            html.Div(
                className="chart-item",
                children=[
                    html.Div(Y_chart1, style={"width": "50%"}),
                    html.Div(Y_chart2, style={"width": "50%"}),
                ],
                style={"display": "flex"},
            ),
            html.Div(
                className="chart-item",
                children=[
                    html.Div(Y_chart3, style={"width": "50%"}),
                    html.Div(Y_chart4, style={"width": "50%"}),
                ],
                style={"display": "flex"},
            ),
        ]

    return html.Div("Please select a report type and year.")


if __name__ == "__main__":
    app.run(debug=True)
