# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

SITES = spacex_df['Launch Site'].unique()

x = spacex_df.groupby('Launch Site')['class'].value_counts()
column_names = ["CCAFS LC-40", "CCAFS SLC-40", "KSC LC-39A", "VAFB SLC-4E", "OUTCOME"]
df = pd.DataFrame(columns = column_names, index = ['Fail','Success'])
df.loc['Fail'] = [x[0],x[2],x[4],x[6],'FAIL']
df.loc['Success'] = [x[1],x[3],x[5],x[7],'SUCCESS']


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown', options=[
                                        {'label': 'ALL SITES', 'value': SITES},
                                        {'label': 'CCAFS LC-40', 'value': SITES[0]},
                                        {'label': 'VAFB SLC-4E', 'value': SITES[1]},
                                        {'label': 'KSC LC-39A', 'value': SITES[2]},
                                        {'label': 'CCAFS SLC-40', 'value': SITES[3]},],
                                    value='ALL', placeholder="SELECT THE LAUNCH SITE HERE", searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                                    marks={0: '0', 100: '10000'}, value=[min_payload, max_payload]),
                                html.Br(),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                html.Br(),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'), Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Success Outcome for All Sites')
        return fig
    elif entered_site == 'CCAFS LC-40':
        fig = px.pie(df, values='CCAFS LC-40', names='OUTCOME', title='Success Rate of CCAFS LC-40')
        return fig
    elif entered_site == 'VAFB SLC-4E':
        fig = px.pie(df, values='VAFB SLC-4E', names='OUTCOME', title='Success Rate of VAFB SLC-4E')
        return fig
    elif entered_site == 'KSC LC-39A':
        fig = px.pie(df, values='KSC LC-39A', names='OUTCOME', title='Success Rate of KSC LC-39A')
        return fig
    elif entered_site == 'CCAFS SLC-40':
        fig = px.pie(df, values='CCAFS SLC-40', names='OUTCOME', title='Success Rate of CCAFS SLC-40')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    #Input(component_id='payload-slider', component_property='value')
    )

def get_scatter_chart(entered_site):
    if entered_site == 'ALL':
        fig2 = px.scatter(spacex_df, x='Payload Mass (kg)', y='Launch Site', color='Booster Version Category', title='PayLoad vs Launch Site')
        return fig2
    elif entered_site == 'CCAFS LC-40':
        s_1 = spacex_df['Launch Site'] == 'CCAFS LC-40'
        df_1 = spacex_df[s_1]
        fig2 = px.scatter(df_1, x='Payload Mass (kg)', y='Launch Site', color='Booster Version Category', title='PayLoad vs Launch Site')
        return fig2
    elif entered_site == 'VAFB SLC-4E':
        s_1 = spacex_df['Launch Site'] == 'VAFB SLC-4E'
        df_1 = spacex_df[s_1]
        fig2 = px.scatter(df_1, x='Payload Mass (kg)', y='Launch Site', color='Booster Version Category', title='PayLoad vs Launch Site')
        return fig2
    elif entered_site == 'KSC LC-39A':
        s_1 = spacex_df['Launch Site'] == 'KSC LC-39A'
        df_1 = spacex_df[s_1]
        fig2 = px.scatter(df_1, x='Payload Mass (kg)', y='Launch Site', color='Booster Version Category', title='PayLoad vs Launch Site')
        return fig2
    elif entered_site == 'CCAFS SLC-40':
        s_1 = spacex_df['Launch Site'] == 'CCAFS SLC-40'
        df_1 = spacex_df[s_1]
        fig2 = px.scatter(df_1, x='Payload Mass (kg)', y='Launch Site', color='Booster Version Category', title='PayLoad vs Launch Site')
        return fig2
    


# Run the app
if __name__ == '__main__':
    app.run_server()

