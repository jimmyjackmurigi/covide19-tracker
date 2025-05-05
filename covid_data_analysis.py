import pandas as pd

url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
df = pd.read_csv(url)

df_cleaned = df.drop(columns=['Province/State', 'Lat', 'Long'])
df_melted = df_cleaned.melt(id_vars=['Country/Region'], var_name='Date', value_name='Total_Cases')
df_melted['Date'] = pd.to_datetime(df_melted['Date'])

df_melted['Total_Cases'].fillna(0, inplace=True)

countries_of_interest = ['Algeria', 'Angola', 'Benin', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cameroon', 'Central African Republic', 'Chad', 'Comoros', 'Congo (Congo-Brazzaville)', 'Congo (Democratic Republic of the Congo)', 'Djibouti', 'Egypt', 'Equatorial Guinea', 'Eritrea', 'Eswatini (fmr. "Swaziland")', 'Ethiopia', 'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Ivory Coast', "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe", "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia"]
df_filtered = df_melted[df_melted['Country/Region'].isin(countries_of_interest)]

print(df_filtered.head())

import matplotlib.pyplot as plt
import seaborn as sns

# Plot total cases over time for a few countries (for example, the first 5 countries)
df_country = df_melted[df_melted['Country/Region'].isin(df_melted['Country/Region'].unique()[:5])]

plt.figure(figsize=(10, 6))
sns.lineplot(data=df_country, x='Date', y='Total_Cases', hue='Country/Region')
plt.title('Total Cases Over Time for Selected Countries')
plt.xlabel('Date')
plt.ylabel('Total Cases')
plt.xticks(rotation=45)
plt.show()

# Plot total deaths over time for the same countries
df_deaths = df_melted[df_melted['Country/Region'].isin(df_melted['Country/Region'].unique()[:5])]

plt.figure(figsize=(10, 6))
sns.lineplot(data=df_deaths, x='Date', y='Total_Cases', hue='Country/Region')
plt.title('Total Deaths Over Time for Selected Countries')
plt.xlabel('Date')
plt.ylabel('Total Deaths')
plt.xticks(rotation=45)
plt.show()

# Calculate the death rate and plot it
df_melted['Death_Rate'] = df_melted['Total_Cases'] / df_melted.groupby('Country/Region')['Total_Cases'].transform('sum')

# Plot Death Rate (ratio of deaths to total cases)
plt.figure(figsize=(10, 6))
sns.lineplot(data=df_melted, x='Date', y='Death_Rate', hue='Country/Region')
plt.title('Death Rate Over Time for Selected Countries')
plt.xlabel('Date')
plt.ylabel('Death Rate')
plt.xticks(rotation=45)
plt.show()
import matplotlib.pyplot as plt
import seaborn as sns

# Plot total cases over time for a few countries (for example, the first 5 countries)
df_country = df_melted[df_melted['Country/Region'].isin(df_melted['Country/Region'].unique()[:5])]

plt.figure(figsize=(10, 6))
sns.lineplot(data=df_country, x='Date', y='Total_Cases', hue='Country/Region')
plt.title('Total Cases Over Time for Selected Countries')
plt.xlabel('Date')
plt.ylabel('Total Cases')
plt.xticks(rotation=45)
plt.show()

# Plot total deaths over time for the same countries
df_deaths = df_melted[df_melted['Country/Region'].isin(df_melted['Country/Region'].unique()[:5])]

plt.figure(figsize=(10, 6))
sns.lineplot(data=df_deaths, x='Date', y='Total_Cases', hue='Country/Region')
plt.title('Total Deaths Over Time for Selected Countries')
plt.xlabel('Date')
plt.ylabel('Total Deaths')
plt.xticks(rotation=45)
plt.show()

# Calculate the death rate and plot it
df_melted['Death_Rate'] = df_melted['Total_Cases'] / df_melted.groupby('Country/Region')['Total_Cases'].transform('sum')

# Plot Death Rate (ratio of deaths to total cases)
plt.figure(figsize=(10, 6))
sns.lineplot(data=df_melted, x='Date', y='Death_Rate', hue='Country/Region')
plt.title('Death Rate Over Time for Selected Countries')
plt.xlabel('Date')
plt.ylabel('Death Rate')
plt.xticks(rotation=45)
plt.show()

# Calculate daily new cases
df_melted['New_Cases'] = df_melted.groupby('Country/Region')['Total_Cases'].diff().fillna(0)

# Plot daily new cases
plt.figure(figsize=(10, 6))
sns.lineplot(data=df_melted, x='Date', y='New_Cases', hue='Country/Region')
plt.title('Daily New Cases Over Time for Selected Countries')
plt.xlabel('Date')
plt.ylabel('New Cases')
plt.xticks(rotation=45)
plt.show()

# Vaccination Progress (assuming we have a "Total_Vaccinations" column)
# Note: Replace 'Total_Vaccinations' with the actual column if it's named differently.
if 'total_vaccinations' in df.columns:
    df_melted['Total_Vaccinations'] = df_melted.groupby('Country/Region')['total_vaccinations'].transform('last')

    # Plot cumulative vaccinations over time
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_melted, x='Date', y='Total_Vaccinations', hue='Country/Region')
    plt.title('Vaccination Progress Over Time for Selected Countries')
    plt.xlabel('Date')
    plt.ylabel('Total Vaccinations')
    plt.xticks(rotation=45)
    plt.show()
else:
    print("Vaccination data is not available in the dataset.")

import plotly.express as px
import plotly.io as pio

fig = pio.read_json(file='file.json')
fig.show()

# Prepare the data for the choropleth map
df_map = df_melted[df_melted['Date'] == df_melted['Date'].max()]  # Select the latest date
df_map = df_map[['Country/Region', 'Total_Cases']]  # Keep only relevant columns
df_map = df_map.groupby('Country/Region').agg({'Total_Cases': 'max'}).reset_index()  # Get max cases per country

# Create the choropleth map
fig = px.choropleth(df_map,
                    locations="Country/Region",  # Locations are countries
                    locationmode='country names',  # Use country names for matching
                    color="Total_Cases",  # Color the countries based on total cases
                    color_continuous_scale="Viridis",  # Set color scale
                    title="COVID-19 Total Cases by Country (Latest Date)",
                    labels={'Total_Cases': 'Total Cases'},
                    template="plotly_dark")  # Use dark template for visual appeal

# Show the map
fig.update_geos(showcoastlines=True, coastlinecolor="Black")
fig.show()

