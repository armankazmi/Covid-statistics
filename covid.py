#Script to plot and view the latest statistics of Covid -19 of any country.
#author: Arman Kazmi
#Getting the latest covid data and saving as covid_data.csv
import requests
r = requests.get('https://covid.ourworldindata.org/data/owid-covid-data.csv')
url_content = r.content
csv_file = open('covid_data.csv','wb')
csv_file.write(url_content)


#Importing the data
import pandas as pd
data =  pd.read_csv("covid_data.csv",parse_dates=['date'])


#Country specific data
def country_data(country_name,data):
    try:
        stats = {}
        covid_country = data[data['location']==country_name]
        covid_country = covid_country[['location', 'date', 'total_cases', 'new_cases','total_deaths', 'new_deaths','new_cases_per_million',
                                       'new_deaths_per_million', 'total_tests', 'new_tests','total_tests_per_thousand',
                                        'new_tests_per_thousand','tests_units']]
        covid_country = covid_country.reset_index()
        covid_country = covid_country.drop('index',axis = 1)
        stats['Total Cases'] = covid_country.total_cases.iloc[-1]
        stats['New Cases'] = covid_country.new_cases.iloc[-1]
        stats['New Deaths'] = covid_country.new_deaths.iloc[-1]
        stats['Total Deaths'] = covid_country.total_deaths.iloc[-1]
        stats['Total Tests'] = covid_country.total_tests.iloc[-1]
        stats['New Cases per million'] = covid_country.new_cases_per_million.iloc[-1]
        stats['New Deaths per million'] = covid_country.new_deaths_per_million.iloc[-1]
        stats['New Tests per thousand'] = covid_country.new_tests_per_thousand.iloc[-1]
        return plot(covid_country,country_name,stats)
    except:
        print("Country name invalid.")
        print("Available country names are : ",data.location.unique())

#Plot
def plot(covid_country,country_name,stats):
    import numpy as np
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    lines = ['Total Cases till today :- ' +str(stats['Total Cases']),
             'New Cases in last 24 hours :- '+str(stats['New Cases']),
             'New Deaths in last 24 hours :- '+str(stats['New Deaths']),
             'Total Deaths till today :- '+str(stats['Total Deaths']),
             'Total Tests till today :- '+str(stats['Total Tests']),
             'New Cases per Million :- '+str(stats['New Cases per million']),
             'New Deaths per Million :- '+str(stats['New Deaths per million']),
             'New Tests per Thousand :- '+str(stats['New Tests per thousand']),
            ]             
    text = '<br>'.join(lines)
    layout = go.Layout(height=800,title_text=country_name+' Covid-19 Statistics',annotations=[
        go.layout.Annotation(
                         bordercolor='black',  # Remove this to hide border
                         align='left',  # Align text to the left
                         yanchor='top',
                         text=text,
                         showarrow=False, # Hide arrow head
                         xref='paper',  # Place relative to figure, not axes
                         yref='paper',
                         font={'family': 'Courier','size':18},  # Use monospace font to keep nice indentation
                         x=0, # Place on left edge
                         y=0.2 # Place a little more than half way down
                         )])
    fig = make_subplots(rows=7, cols=1)
    fig.add_trace(go.Scatter(x = covid_country.date, y=np.array(covid_country.new_cases),name='New cases'),row=1, col=1)
    fig.add_trace(go.Scatter(x = covid_country.date, y=np.array(covid_country.new_deaths),name = 'New Deaths'),row=2, col=1)
    fig.add_trace(go.Scatter(x = covid_country.date, y=np.array(covid_country.new_tests),name='New Tests'),row=3, col=1)
    fig.add_trace(go.Scatter(x = covid_country.date, y=np.array(covid_country.total_cases),name='Total Cases'),row=4, col=1)
    fig.add_trace(go.Scatter(x = covid_country.date, y=np.array(covid_country.total_deaths),name='Total Deaths'),row=5, col=1)
    fig.update_traces(mode="markers+lines")
    fig.update_layout(layout)
    #fig.update_layout(title_text=country_name+' statistics '+str(stats))
    return fig.show()


#Choice of Stats
print("Enter the country name for Covid-19 statistics : ")
country = input()
country_data(country,data)

