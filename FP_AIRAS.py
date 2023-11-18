# Final Project - Analyzing the Impact of Recession on Automobile Sales

# You have been hired by XYZAutomotives as a data scientist. 
# Your first task is to analyze the historical data and give the company directors insights on how the sales were affected during times of recession. 
# You will provide a number of charts/plots to visualize the data and make it easy for the directors to understand your analysis.

'''
About the dataset
In this assignment you will be presented with varies question for analysing data to understand the historical trends in automobile sales during recession periods:

recession period 1 - year 1980
recession period 2 - year 1981 to 1982
recession period 3 - year 1991
recession period 4 - year 2000 to 2001
recession period 5 - year end 2007 to mid 2009
recession period 6 - year 2020 -Feb to April (Covid-19 Impact)
The data used in this lab has been artifically created for the purpose of this assignment only. No real data has been used.

Data Description.
The dataset includes the following variables:

Date: The date of the observation.
Recession: A binary variable indicating recession perion; 1 means it was recession, 0 means it was normal.
Automobile_Sales: The number of vehicles sold during the period.
GDP: The per capita GDP value in USD.
Unemployment_Rate: The monthly unemployment rate.
Consumer_Confidence: A synthetic index representing consumer confidence, which can impact consumer spending and automobile purchases.
Seasonality_Weight: The weight representing the seasonality effect on automobile sales during the period.
Price: The average vehicle price during the period.
Advertising_Expenditure: The advertising expenditure of the company.
Vehicle_Type: The type of vehicles sold; Supperminicar, Smallfamiliycar, Mediumfamilycar, Executivecar, Sports.
Competition: The measure of competition in the market, such as the number of competitors or market share of major manufacturers.
Month: Month of the observation extracted from Date.
Year: Year of the observation extracted from Date.
By examining various factors mentioned above from the dataset, you aim to gain insights into how recessions impact automobile sales for your company.

'''

# Part 1: Create visualizations using Matplotib, Seaborn & Folium
# Objective: The objective of this part of the project is to analyze the historical trends in automobile sales during recession periods. 
# The goal is to provide insights into how the sales of XYZAutomotives, a company specializing in automotive sales, were affected during times of recession.


'''
Tasks to be performed
TASK 1.1: Develop a Line chart using the functionality of pandas to show how automobile sales fluctuate from year to year.

TASK 1.2: Plot different lines for categories of vehicle type and analyse the trend to answer the question “Is there a noticeable difference in sales trends between different vehicle types during recession periods?”

TASK 1.3: Use the functionality of Seaborn Library to create a visualization to compare the sales trend per vehicle type for a recession period with a non-recession period.

TASK 1.4: Use sub plotting to compare the variations in GDP during recession and non-recession period by developing line plots for each period.

TASK 1.5: Develop a Bubble plot for displaying the impact of seasonality on Automobile Sales.

TASK 1.6: Use the functionality of Matplotlib to develop a scatter plot to identify the correlation between average vehicle price relate to the sales volume during recessions.

TASK 1.7: Create a pie chart to display the portion of advertising expenditure of XYZAutomotives during recession and non-recession periods.

TASK 1.8: Develop a pie chart to display the total Advertisement expenditure for each vehicle type during recession period.

TASK 1.9: Develop a countplot to analyse the effect of the unemployment rate on vehicle type and sales during the Recession Period.
'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium


url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
df = pd.read_csv(url)
print('Data downloaded and read into a dataframe!')

# Display statistical summary of the DataFrame using the describe() function.
print(df.describe())

# Print the column names of the DataFrame.
print(df.columns)

print(df.head(4))


# Creating Visualizations for Data Analysis
# TASK 1.1: Develop a Line chart using the functionality of pandas to show how automobile sales fluctuate from year to year.
# to group the year and calculate the average on the 'Automobile Sales', as the data has years and months column make use of .plot() with kind = 'line'

#create data for plotting
df_line = df.groupby(df['Year'])['Automobile_Sales'].mean()

#create figure
plt.figure(figsize=(10, 6))
df_line.plot(kind = 'line')
plt.xlabel('Year')
plt.ylabel('Sales Volume')
plt.title('Automobile Sales over Time')
plt.show()


# Include the following on the plot ticks on x- axis with all the years, to identify the years of recession annotation for at least two years of recession
# Title as Automobile Sales during Recession

#create data for plotting
df_line = df.groupby(df['Year'])['Recession'].mean()

plt.figure(figsize=(10, 6))
#create figure
df_line.plot(kind = 'line')
plt.xticks(list(range(1980,2024)), rotation = 90)
plt.xlabel('Year')
plt.ylabel('Sales Volume')
plt.title('Automobile Sales during Recession')
plt.text(1982, 650, '1981-82 Recession')
plt.legend()
plt.show()


# TASK 1.2: Plot different lines for categories of vehicle type and analyse the trend to answer the question Is there a noticeable difference in sales trends 
# between different vehicle types during recession periods?


# create a separate dataframe where the column recession has a value of '1' to group the year, vehicle_type and calculate the average on the 'Automobile Sales' one way is to 
# use as_index as false else you will endup with multiple-indexed datafame, later set year as index and groupby vehicle over Sales and plot
# make use of .plot() with kind = 'line'
#do not forget to include labels and title

df_Mline = df.groupby(['Year','Vehicle_Type'], as_index=False)['Automobile_Sales'].sum()
df_Mline.set_index('Year', inplace=True)
df_Mline = df_Mline.groupby(['Vehicle_Type'])['Automobile_Sales']
df_Mline.plot(kind='line')
plt.xlabel('Year')
plt.ylabel('Sales Volume')
plt.title('Sales Trend Vehicle-wise during Recession')
plt.legend(title='Vehicle Type')
plt.show()


# TASK 1.3: Use the functionality of Seaborn Library to create a visualization to compare the sales trend per vehicle type for a recession period with a non-recession period.
# To visualize the average number of vehicles sold during recession and non-recession periods, you can use a bar chart. 
# You will need to group recession average Automobile_Sales and then plot it
# Make use of sns.barplot(x=x,y=y, data = df)

new_df = df.groupby('Recession')['Automobile_Sales'].mean().reset_index()

# Create the bar chart using seaborn
plt.figure(figsize=(10, 6))
sns.barplot(x='Recession', y='Automobile_Sales', hue='Recession',  data=new_df)
plt.xlabel('Period')
plt.ylabel('Average Sales')
plt.title('Average Automobile Sales during Recession and Non-Recession')
plt.xticks(ticks=[0, 1], labels=['Non-Recession', 'Recession'])
plt.show()

# Now you want to compare the sales of different vehicle types during a recession and a non-recession period

# To visualize sales of different vehicles during recession and non-recession periods, you can use a bar chart
# You will need to group Recession, Vehicle_Type for average Automobile_Sales and then plot it
# Make use of sns.barplot(x=x,y=y, data = df)


# Filter the data for recessionary periods
recession_data = df[df['Recession'] == 1]

dd=df.groupby(['Recession','Vehicle_Type'])['Automobile_Sales'].mean().reset_index()

# Calculate the total sales volume by vehicle type during recessions
#sales_by_vehicle_type = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].sum().reset_index()

# Create the grouped bar chart using seaborn
plt.figure(figsize=(10, 6))
sns.barplot(x='Recession', y='Automobile_Sales', hue='Vehicle_Type', data=dd)
plt.xticks(ticks=[0, 1], labels=['Non-Recession', 'Recession'])
plt.xlabel('Period')
plt.ylabel('Average Sales')
plt.title('Vehicle-Wise Sales during Recession and Non-Recession Period')

plt.show()

# TASK 1.4: Use sub plotting to compare the variations in GDP during recession and non-recession period by developing line plots for each period.

# Now, you want to find more insights from the data to understand the reason.
# Plot a two line charts using subplotting to answer:
# How did the GDP vary over time during recession and non-recession periods


#Create dataframes for recession and non-recession period
rec_data = df[df['Recession'] == 1]
non_rec_data = df[df['Recession'] == 0]

#Figure
fig=plt.figure(figsize=(12, 6))

#Create different axes for subploting
ax0 = fig.add_subplot(1, 2, 1) # add subplot 1 (1 row, 2 columns, first plot)
ax1 = fig.add_subplot(1, 2, 2 ) # add subplot 2 (1 row, 2 columns, second plot). 

#plt.subplot(1, 2, 1)
sns.lineplot(x='Year', y='GDP', data=rec_data, label='Recession', ax=ax0)
ax0.set_xlabel('Year')
ax0.set_ylabel('GDP')
ax0.set_title('GDP Variation during Recession Period')

#plt.subplot(1, 2, 2)
sns.lineplot(x='Year', y='GDP', data=non_rec_data, label='Non-Recesion',ax=ax1)
ax1.set_xlabel('Year')
ax1.set_ylabel('GDP')
ax1.set_title('GDP Variation during Non - Recession Period')

plt.tight_layout()
plt.show()

# TASK 1.5: Develop a Bubble plot for displaying the impact of seasonality on Automobile Sales.

# How has seasonality impacted the sales, in which months the sales were high or low? Check it for non-recession years to understand the trend

# Develop a Bubble plot for displaying Automobile Sales for every month and use Seasonality Weight for representing the size of each bubble
# Title this plot as 'Seasonality impact on Automobile Sales'
# You can create Bubble Chart by calling the scatter()
# Pass the 'Month' and 'Automobile_Sales' to the functions as x and y and then use Seasonality weight for size parameter

non_rec_data = df[df['Recession'] == 0]
    
size=non_rec_data['Seasonality_Weight'] #for bubble effect

sns.scatterplot(data=non_rec_data, x='Month', y='Automobile_Sales', size=size)

#you can further include hue='Seasonality_Weight', legend=False)

plt.xlabel('Month')
plt.ylabel('Automobile_Sales')
plt.title('Seasonality impact on Automobile Sales')

plt.show()

# TASK 1.6: Use the functionality of Matplotlib to develop a scatter plot to identify the correlation between average vehicle price relate to the sales volume during recessions

# From the data, develop a scatter plot to identify if there a correlation between consumer confidence and automobile sales during recession period?
# Title this plot as 'Consumer Confidence and Automobile Sales during Recessions'
# You can create dataframe where recession is '1'.
# Pass the 'Consumer_Confidence' and 'Automobile_Sales' to the plt.scatter()

#Create dataframes for recession and non-recession period
rec_data = df[df['Recession'] == 1]
plt.scatter(recession_data['Consumer_Confidence'], rec_data['Automobile_Sales'])

plt.xlabel('Consumer_Confidence')
plt.ylabel('Automobile_Sales')
plt.title('Consumer Confidence and Automobile Sales during Recessions')
plt.show()


# TASK 1.7: Create a pie chart to display the portion of advertising expenditure of XYZAutomotives during recession and non-recession periods.

# How did the advertising expenditure of XYZAutomotives change during recession and non-recession periods?
# You can create two dataframe for recession and nonreccession period. Calculate the sum of Advertising_Expenditure for both dataframes
# Pass these total values to plt.pie(). May include labels as ['Recession', 'Non-Recession'] Feel Free to customie the pie further
# title this plot as - Advertising Expenditure during Recession and Non-Recession Periods

# Filter the data 
Rdata = df[df['Recession'] == 1]
NRdata = df[df['Recession'] == 0]

# Calculate the total advertising expenditure for both periods
RAtotal = Rdata['Advertising_Expenditure'].sum()
NRAtotal = NRdata['Advertising_Expenditure'].sum()

# Create a pie chart for the advertising expenditure 
plt.figure(figsize=(8, 6))

labels = ['Recession', 'Non-Recession']
sizes = [RAtotal, NRAtotal]
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
plt.title('Advertising Expenditure during Recession and Non-Recession Periods')
plt.show()


# TASK 1.8: Develop a pie chart to display the total Advertisement expenditure for each vehicle type during recession period.

# Can we observe the share of each vehicle type in total sales during recessions?
# Create another pie plot to display the total advertisement expenditure for each vehicle type
# You will be required to group vehicle type for sum of advertisement expenditure.
# the plot a pie with the data, May include relevant labels
# title this plot as - Share of Each Vehicle Type in Total Sales during Recessions

# Filter the data 
Rdata = df[df['Recession'] == 1]

# Calculate the sales volume by vehicle type during recessions
VTsales = Rdata.groupby('Vehicle_Type')['Advertising_Expenditure'].sum()

# Create a pie chart for the share of each vehicle type in total sales during recessions
plt.figure(figsize=(8, 6))

labels = VTsales.index
sizes = VTsales.values
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)

plt.title('Share of Each Vehicle Type in Total Sales during Recessions')

plt.show()

# TASK 1.9: Develop a countplot to analyse the effect of the unemployment rate on vehicle type and sales during the Recession Period.

# Analyze the effect of the unemployment rate on vehicle type and sales during the Recession Period
# You can create a countplot and title the plot as 'Effect of Unemployment Rate on Vehicle Type and Sales'
# Filter out the data for recession period. Make use of countplot() from seaborn and pass the relavent data

data= df[df['Recession'] == 1]
    
plt.figure(figsize=(10, 6))

sns.countplot(data=data, x='unemployment_rate', hue='Vehicle_Type')

plt.xlabel('Unemployment Rate')
plt.ylabel('Count')
plt.title('Effect of Unemployment Rate on Vehicle Type and Sales')
plt.legend(loc='upper right')
plt.show()


# TASK 1.10 Create a map on the hightest sales region/offices of the company during recession period
# You found that the datset also contains the location/city for company offices. Now you want to show the recession impact on various offices/city sales by developing a choropleth

from folium import Choropleth

# Pobierz dane o sprzedaży w różnych biurach firmy podczas recesji
# Załóżmy, że masz DataFrame 'sales_data' zawierający informacje o lokalizacji, sprzedaży, itp.
# sales_data = pd.read_csv('ścieżka/do/twoich/danych.csv')

# Wczytaj dane geojson o stanach w USA
geo_path = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/us-states.json'
geo_data_1 = pd.read_json(geo_path)

# Filter the data for the recession period and specific cities
recession_data = data[data['Recession'] == 1]

# Calculate the total sales by city
sales_by_city = recession_data.groupby('City')['Automobile_Sales'].sum().reset_index()

# Create a base map centered on the United States
map1 = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

# Create a choropleth layer using Folium
choropleth = folium.Choropleth(
    geo_data= geo_data_1,  # GeoJSON file with state boundaries
    data=sales_by_city,
    columns=['City', 'Automobile_Sales'],
    key_on='feature.properties.name',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Automobile Sales during Recession'
).add_to(map1)


# Add tooltips to the choropleth layer
choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(['name'], labels=True)
)

# Display the map
map1

