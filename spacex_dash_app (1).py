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
                                dcc.Dropdown(id='site-dropdown',  options=[{'label': 'All Sites', 'value': 'ALL'},
                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                               { 'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                ],
                                value='ALL'
                               
                                )
                                ,
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                marks={0: '0', 1000: '1000', 2000: '2000', 3000: '3000', 4000: '4000', 5000: '5000', 6000: '6000', 7000: '7000', 8000: '8000', 9000: '9000', 10000: '10000'},
                                value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Callback function for `success-pie-chart`
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(selected_site):
    # Filter the DataFrame based on the selected site
    if selected_site == 'ALL':
        site_success_counts = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
        site_success_counts = site_success_counts.rename(columns={'class': 'Success Count'})
        title_text = 'Total Success Launches by Launch Site'
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        success_count = filtered_df[filtered_df['class'] == 1].shape[0]
        failure_count = filtered_df[filtered_df['class'] == 0].shape[0]
        pie_chart = px.pie(
            names=['Success', 'Failure'],
            values=[success_count, failure_count],
            title=f'Success vs. Failure Launches for {selected_site}',
            hole=0.3,  # Set to 0 for a complete circle
            color_discrete_sequence=['red', 'green'],  # Customize colors
        )

        return pie_chart
    pie_chart_all_sites = px.pie(
        site_success_counts,
        names='Launch Site',
        values='Success Count',
        title=title_text,
        hole=0.3,  # Set to 0 for a complete circle
        color_discrete_sequence=px.colors.qualitative.Set1,  # Customize colors
    )
    return pie_chart_all_sites
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'), Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, selected_payload_range):
   
    if selected_site == 'ALL':
        filtered_df = spacex_df
        title_text = 'Payload vs. Launch Outcome for All Sites'
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        title_text = f'Payload vs. Launch Outcome for {selected_site}'
    filtered_df = filtered_df[
        (filtered_df['Payload Mass (kg)'] >= selected_payload_range[0]) &
        (filtered_df['Payload Mass (kg)'] <= selected_payload_range[1])
    ]
    scatter_chart = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title=title_text,
        labels={'class': 'Launch Outcome'},
        color_discrete_sequence=px.colors.qualitative.Set1,  # Customize colors
    )

    return scatter_chart

# Run the app
if __name__ == '__main__':
    app.run_server()
