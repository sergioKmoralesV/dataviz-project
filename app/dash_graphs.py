import pandas as pd
import plotly.express as px
from dash import dash, dcc, html, Input, Output
import plotly.graph_objs as go


app = dash.Dash(__name__)

df_hulu = pd.read_csv('../data/hulu_titles.csv')
df_netf = pd.read_csv('../data/netflix_titles.csv')
df_3 = pd.read_csv('../data/MoviesOnStreamingPlatforms.csv')

# df_hulu['dataset'] = 'Hulu'
# df_netf['dataset'] = 'Netflix'

df_joined = pd.concat([df_hulu, df_netf])
g_by_release = df_joined.groupby(['release_year'])


############################################## Graph 1
@app.callback(
    Output('content-release-date', 'figure'),
    Input('start_y', 'value'),
    Input('end_y', 'value'))
def update_figure(start_year, end_year):
    filtered_df1 = df_hulu[(start_year <= df_hulu['release_year']) & (df_hulu['release_year'] <= end_year)]
    filtered_df2 = df_netf[(start_year <= df_netf['release_year']) & (df_netf['release_year'] <= end_year)]

    g_by_release1 = filtered_df1.groupby(['release_year'])
    g_by_release2 = filtered_df2.groupby(['release_year'])

    values_years1 = [count for count in g_by_release1.size()]
    values_years2 = [count for count in g_by_release2.size()]

    fig = go.Figure([
        go.Scatter(
            name='Hulu',
            x=list(g_by_release1.groups.keys()),
            y=values_years1,
            mode='markers+lines',
            marker=dict(color='blue', size=6)
        ),
        go.Scatter(
            name='Netflix',
            x=list(g_by_release2.groups.keys()),
            y=values_years2,
            mode='markers+lines',
            marker=dict(color='red', size=6)
        )])

    fig.update_layout(
        title_text='Hulu and Netflix releases of movies and tv shows by year',
        xaxis_title='Year',
        yaxis_title='Count',
        height=600,
        title_font_family='Lato',
        title_font_size = 18)

    fig.update_layout(transition_duration=500)

    return fig


############################################## Graph 2

df_3mod = df_3.dropna(subset=['Age'])
g_by_age = df_3mod.groupby(['Age']).size().reset_index(name='count').sort_values('count')
g_by_age.reset_index(drop=True, inplace=True)

fig2 = go.Figure()

fig2.add_trace(go.Scatter(x = g_by_age['count'], 
                          y = g_by_age['Age'],
                          mode = 'markers',
                          marker_color ='darkblue',
                          marker_size  = 10))

for i in range(0, len(g_by_age)):
    fig2.add_shape(type='line',
        x0 = 0, y0 = i,
        x1 = g_by_age['count'][i],
        y1 = i,
        line=dict(color='crimson', width = 3))

fig2.update_layout(title_text = 
                   'Number of movies and tv series in each age category',
                   title_font_size = 15)


################################################ Graph 3 - Boxplot

def figure3():

    hulu_mov = df_hulu[['duration', 'type']].dropna()
    hulu_mov = hulu_mov[hulu_mov['type'] == 'Movie']
    hulu_mov['duration'] = hulu_mov['duration'].str.replace(' min', '')
    hulu_mov = hulu_mov.astype({'duration': 'int32'})
    hulu_mov['dataset'] = 'Hulu'

    netf_mov = df_netf[['duration', 'type']].dropna()
    netf_mov = netf_mov[netf_mov['type'] == 'Movie']
    netf_mov['duration'] = netf_mov['duration'].str.replace(' min', '')
    netf_mov = netf_mov.astype({'duration': 'int32'})
    netf_mov['dataset'] = 'Netflix'

    alldata = pd.concat([hulu_mov, netf_mov])

    return px.box(alldata, x='dataset', y='duration', height=700, width=900)


fig3 = figure3()

################################################

app.layout = html.Div(style={'fontFamily': 'Lato', 'margin': '12px 36px'}, children=[
    html.H1(children='Hulu and Netflix Movies and TV Shows'),

    html.Div([
        html.Div([
            "Starting Year: ",
            dcc.Dropdown(list(g_by_release.groups.keys()), 1923, id='start_y')
        ],
            style={
                "width": "25%",
            },
        ),
        html.Div([
            "End Year: ",
            dcc.Dropdown(list(g_by_release.groups.keys()), 2021, id='end_y')
        ],
            style={
                "width": "25%"
            },
        )]
        , style={
            "display": "flex",
            "justifyContent": "space-around",
            "fontWeight": "600",
        }),
    dcc.Graph(
        id='content-release-date'
    ),

    dcc.Graph(
        id='age-distribution',
        figure=fig2
    ),

    dcc.Graph(
        id='box-plot1',
        figure=fig3
    )
    ])


if __name__ == '__main__':
    app.run_server(debug=True)


# [1] - number of movies + tv series per platform - [callback with date]    DONE
# [2] - Box plot of distribution of duration of movies - [callback with listed_in]
# [3] - Box plot of distribution of duration of tv series - [callback with listed_in] 
# [4] - Difference between de release date and date addeed 
# [5] - Movies/tv series counting [map]
# [6] - 
# [7] - 
# [8] -
# [9] - 
# [10] - Comparison of movies between many platforms