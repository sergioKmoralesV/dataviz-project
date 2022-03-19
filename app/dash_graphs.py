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
        title='Hulu and Netflix releases of movies and tv shows by year',
        xaxis_title='Year',
        yaxis_title='Count',
        height=600,
        title_font_family='Lato')

    fig.update_layout(transition_duration=500)

    return fig



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
    )
    ])






if __name__ == '__main__':
    app.run_server(debug=True)


# [1] - number of movies + tv series per platform - [callback with date]
# [2] - Box plot of distribution of duration of movies - [callback with listed_in]
# [3] - Box plot of distribution of duration of tv series - [callback with listed_in] 
# [4] - Difference between de release date and date addeed 
# [5] - Movies/tv series counting [map]
# [6] - 
# [7] - 
# [8] -
# [9] - 
# [10] - Comparison of movies between many platforms