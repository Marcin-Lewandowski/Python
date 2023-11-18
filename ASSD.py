# This is Final Project - Analyzing the Impact of Recession on Automobile Sales part 2

# Part 2 (ASSD.py): Create Dashboard using Plotly and Dash
# Objective: The objective of this part of the Fnal assignment is to create dashboards to contain your plots and charts and to provide the directors with the ability 
# to select a particular report or a period of time so they can discuss the data in detail.

# You will create dashboards using Dash and Plotly and then add user-interactions to your dashboards.

# Creating dashboards and adding customizations to the dashboards
# The directors of XYZAutomobiles have requested a dashboard to be developed so they can drill into the data in more detail for specific years or by different categories. 
# Your second task is to create a suitable dashboard and add in user interactions so that the directors can select the data they want to review without the need to request new plots.

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Sales Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    # Title
    html.H1("Automobile Sales Statistics Dashboard", style={
        'textAlign': 'center', 
        'color': '#503D36', 
        'fontSize': 24
    }),

    # TASK 2.2: Add drop-down menus
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'},
            ],
            value='Select Statistics',
            placeholder='Select a report type'
        )
    ]),

    html.Div(dcc.Dropdown(
        id='select-year',
        options=[{'label': i, 'value': i} for i in year_list],
        value=year_list[0]
    )),

    # TASK 2.3: Add a division for output
    html.Div(id='output-container', className='chart-grid', style={'display': 'flex'})
])

#TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value'))




def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True


#Callback for plotting
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-year', component_property='value'), Input(component_id='dropdown-statistics', component_property='value')])



def update_output_container(selected_year, selected_statistics):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        
        #TASK 2.5: Create and display graphs for Recession Report Statistics
        #Plot 1 Automobile sales fluctuate over Recession Period (year wise)
        # use groupby to create relevant data for plotting
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        # Plotting  the line graph
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, 
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales fluctuation over Recession Period"))

        #Plot 2 Calculate the average number of vehicles sold by vehicle type       
        # use groupby to create relevant data for plotting
        average_sales = data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()             
        R_chart2 = dcc.Graph(
            figure=px.bar(
            average_sales,
            x='Vehicle_Type',  
            y='Automobile_Sales', 
            title="Average Number of Vehicles Sold by Vehicle Type"
            )
        )
        
        # Plot 3 Pie chart for total expenditure share by vehicle type during recessions
        # use groupby to create relevant data for plotting
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(

            figure=px.pie(
            exp_rec,
            values='Advertising_Expenditure',
            names='Vehicle_Type', 
            title='Total Expenditure Share by Vehicle Type During Recessions'
            )
        )


        # Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales
        # Group by 'Vehicle_Type' and calculate the mean of 'Unemployment_Rate' and sum of 'Automobile_Sales'
        unemployment_effect = data.groupby('Vehicle_Type').agg({'unemployment_rate': 'mean', 'Automobile_Sales': 'sum'}).reset_index()

        # Plotting the bar graph
        R_chart4 = dcc.Graph(
            
            figure=px.bar(
                unemployment_effect,
                x='Vehicle_Type',  
                y=['unemployment_rate', 'Automobile_Sales'],  
                title='Effect of Unemployment Rate on Vehicle Type and Sales',
                labels={'unemployment_rate': 'Mean Unemployment Rate', 'Automobile_Sales': 'Total Sales'},
            )
        )

        # Return the updated layout
        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)])
        ]
        

# TASK 2.6: Create and display graphs for Yearly Report Statistics
# Yearly Statistic Report Plots                             
    elif (selected_year and selected_statistics == 'Yearly Statistics'):
        yearly_data = data[data['Year'] == selected_year]
        
        #TASK 2.5: Creating Graphs Yearly data
        # Plot 1 Yearly Automobile sales using line chart for the whole period.         
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(
            yas,
            x='Year', 
            y='Automobile_Sales', 
            title='Yearly Automobile Sales Over the Whole Period'                       
        ))

        # Plot 2 Total Monthly Automobile sales using line chart.
        monthly_data = yearly_data.groupby('Month')['Automobile_Sales'].mean().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(
            monthly_data,
            x='Month',
            y='Automobile_Sales', 
            title='Total Monthly Automobile Sales Over the Whole Period{}'.format(selected_year)
        ))

        # Plot 3 Bar chart for average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(
            avr_vdata,
            x='Vehicle_Type', 
            y='Automobile_Sales', 
            title='Average Vehicles Sold by Vehicle Type in the year {}'.format(selected_year)
        ))
        
        # Plot 4 Total Advertisement Expenditure for each vehicle using pie chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(
            exp_data,
            values='Advertising_Expenditure',
            names='Vehicle_Type', 
            title='Total Advertisement Expenditure for Each Vehicle in the year {}'.format(selected_year)
        ))



        # Return the updated layout
        return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)])
        ]
        
                               
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

