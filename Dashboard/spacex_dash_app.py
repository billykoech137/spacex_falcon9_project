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

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                {'label': 'All Sites', 'value':'ALL'},
                                                {'label': 'Cape Canaveral AFS Launch Complex 40', 'value':'CCAFS LC-40'},
                                                {'label': 'Vandenberg AFB Space Launch Complex 4E', 'value':'VAFB SLC-4E'},
                                                {'label': 'Kennedy Space Complex Launch Complex 39A', 'value':'KSC LC-39A'},
                                                {'label': 'Cape Canaveral AFS Space Launch Complex 40', 'value':'CCAFS SLC-40'}
                                             ],
                                            value = 'ALL',
                                            placeholder='All Sites',
                                            searchable=True
                                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=100,
                                                marks={0:'0',2500:'2,500',5000:'5,000',7500:'7,500', 10000:'10,000'},
                                                value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ]
                    )

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(launch_site):
    if launch_site == 'ALL':
        data = spacex_df.groupby(['Launch Site'])['class'].apply(lambda x: (x==1).sum()).reset_index(name='sucess')
        fig = px.pie(data_frame=data, values='sucess', names='Launch Site', title='Total Success Launches By Site')
        return fig
    else:
        df_site = spacex_df.groupby('Launch Site')['class'].get_group(launch_site).value_counts().to_frame().reset_index().rename(columns={'index':'class','class':'count'})
        fig = px.pie(data_frame=df_site, values='count', names='class', title=f'Total Success Launches for {launch_site}')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])

def get_scatter_chart(site, payload):
    
    if site == "ALL":
        fig = px.scatter(data_frame=spacex_df, x='Payload Mass (kg)', y='class', color='Booster Version', title='Correlation Between Payload and Success For All Sites')
        return fig
    else:
        df_2 = spacex_df.groupby('Launch Site').get_group(site)
        data = df_2[(df_2['Payload Mass (kg)']>=payload[0]) & (df_2['Payload Mass (kg)']<=payload[1])]
        fig = px.scatter(data_frame=data, x='Payload Mass (kg)', y='class', color='Booster Version', title=f'Correlation Between Payload and Success For {site} Site')
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
