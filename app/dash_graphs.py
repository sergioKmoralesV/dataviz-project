from collections import defaultdict
from email.policy import default
import pandas as pd
import plotly.express as px
from dash import dash, dcc, html, Input, Output
import plotly.graph_objs as go
import pycountry

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
            marker=dict(color='#1ce783', size=6)
        ),
        go.Scatter(
            name='Netflix',
            x=list(g_by_release2.groups.keys()),
            y=values_years2,
            mode='markers+lines',
            marker=dict(color='red', size=6)
        )])

    fig.update_layout(
        title_text='Hulu vs Netflix releases of movies and tv shows by year',
        xaxis_title='Year released',
        yaxis_title='Total count of releases',
        height=600,
        title_font_size=18)
    fig.update_layout(title_font_family='Lato')
    fig.update_layout(transition_duration=500)

    return fig


############################################## Graph 2

df_3mod = df_3.dropna(subset=['Age'])
g_by_age = df_3mod.groupby(['Age']).size().reset_index(name='count').sort_values('count')
g_by_age.reset_index(drop=True, inplace=True)

fig2 = go.Figure()

fig2.add_trace(go.Scatter(x=g_by_age['count'],
                          y=g_by_age['Age'],
                          mode='markers',
                          marker_color='darkblue',
                          marker_size=10))

for i in range(0, len(g_by_age)):
    fig2.add_shape(type='line',
                   x0=0, y0=i,
                   x1=g_by_age['count'][i],
                   y1=i,
                   line=dict(color='purple', width=3))

fig2.update_layout(title_font_family='Lato')
fig2.update_layout(title_text=
                   'Number of movies and tv series in each age category',
                   xaxis_title='Count per category',
                   yaxis_title='Age category',
                   height=500,
                   )


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
    netf_mov = netf_mov[netf_mov['duration'] < 300]
    netf_mov['dataset'] = 'Netflix'

    # alldata = pd.concat([hulu_mov, netf_mov])

    fig = go.Figure()
    fig.add_trace(go.Box(y=netf_mov['duration'], name='Netflix',
                         marker_color='indianred'))
    fig.add_trace(go.Box(y=hulu_mov['duration'], name='Hulu',
                         marker_color='#1ce783'))

    fig.update_layout(
        height=700,
        title_text='Hulu and Netflix movie lenght',
        yaxis_title='Duration in Minutes',
        title_font_size=18)
    fig.update_layout(title_font_family='Lato')

    return fig


def figure3_series():
    hulu_mov = df_hulu[['duration', 'type']].dropna()
    hulu_mov = hulu_mov[hulu_mov['type'] == 'TV Show']
    hulu_mov['duration'] = hulu_mov['duration'].str.replace(' Seasons', '')
    hulu_mov['duration'] = hulu_mov['duration'].str.replace(' Season', '')
    hulu_mov = hulu_mov.astype({'duration': 'int32'})
    hulu_mov['dataset'] = 'Hulu'

    netf_mov = df_netf[['duration', 'type']].dropna()
    netf_mov = netf_mov[netf_mov['type'] == 'TV Show']
    netf_mov['duration'] = netf_mov['duration'].str.replace(' Seasons', '')
    netf_mov['duration'] = netf_mov['duration'].str.replace(' Season', '')
    netf_mov = netf_mov.astype({'duration': 'int32'})
    netf_mov = netf_mov[netf_mov['duration'] < 300]
    netf_mov['dataset'] = 'Netflix'

    fig = go.Figure()
    fig.add_trace(go.Box(y=netf_mov['duration'], name='Netflix',
                         marker_color='indianred'))
    fig.add_trace(go.Box(y=hulu_mov['duration'], name='Hulu',
                         marker_color='#1ce783'))

    fig.update_layout(
        height=700,
        title_text='Hulu and Netflix tv shows lenght',
        yaxis_title='Duration in # Seasons',
        title_font_size=18)
    fig.update_layout(title_font_family='Lato')

    return fig


fig3 = figure3()
fig3_series = figure3_series()

################################################ Graph 5 not finished, callback to add

@app.callback(
    Output('rotten-tomatoes', 'figure'),
    Input('checklist', 'value'))
def figure5(checklist):
    df_3rot = df_3.dropna(subset=['Rotten Tomatoes'])

    df_3rot['sum'] = 0
    for column in checklist:
        df_3rot['sum'] += df_3rot[column]

    df_3rot = df_3rot[df_3rot['sum'] > 0]

    df_3rot['Rotten Tomatoes'] = df_3rot['Rotten Tomatoes'].str.replace('/100', '')

    df_3rot = df_3rot.astype({'Rotten Tomatoes': 'int32'}).sort_values('Rotten Tomatoes')
    df_3rot = df_3rot.astype({'Rotten Tomatoes': 'str'})

    fig5 = px.histogram(df_3rot, x='Rotten Tomatoes', labels={
        'Rotten Tomatoes': 'Score of Rotten Tomatoes',
    }, title='Rotten Tomatoes score distribution of Movies on Streaming Platforms', height=500)
    fig5.update_layout(title_font_family='Lato', yaxis_title='Total count per score')
    fig5.update_traces(hovertemplate='# Movies with score %{x} <br> Count: %{y}<extra></extra>')
    return fig5


################################################ Graph 6
def fuzzySearch(country):
    try:
        result = pycountry.countries.search_fuzzy(country)
    except Exception:
        return None
    else:
        return result[0].alpha_3


def figure6():
    df = df_netf['country'].dropna()

    countries = {}

    for x in df:
        if ',' in x:
            to_add = x.split(', ')
            for country in to_add:
                if country in countries:
                    countries[country] += 1
                else:
                    countries[country] = 1
        elif x in countries:
            countries[x] += 1
        else:
            countries[x] = 1

    df_countries = pd.DataFrame.from_dict(countries, orient='index')
    df_countries['iso'] = [fuzzySearch(country) for country in df_countries.index]
    df_countries_filtered = df_countries.dropna(subset=['iso'])

    df_countries_filtered.reset_index(inplace=True)
    df_countries_filtered = df_countries_filtered.rename({0: 'total_count'}, axis=1)
    fig6 = px.choropleth(df_countries_filtered, locations="iso", hover_name='index', color='total_count',
                         color_continuous_scale=px.colors.sequential.Oryel, title='Netflix - Country filmed')
    fig6.update_layout(title_font_family='Lato')
    return fig6


f6 = figure6()


def figure6_hulu():
    df = df_hulu['country'].dropna()

    countries = {}

    for x in df:
        if ',' in x:
            to_add = x.split(', ')
            for country in to_add:
                if country in countries:
                    countries[country] += 1
                else:
                    countries[country] = 1
        elif x in countries:
            countries[x] += 1
        else:
            countries[x] = 1

    df_countries = pd.DataFrame.from_dict(countries, orient='index')
    df_countries['iso'] = [fuzzySearch(country) for country in df_countries.index]
    df_countries_filtered = df_countries.dropna(subset=['iso'])

    df_countries_filtered.reset_index(inplace=True)
    df_countries_filtered = df_countries_filtered.rename({0: 'total_count'}, axis=1)
    fig6 = px.choropleth(df_countries_filtered, locations="iso", hover_name='index', color='total_count',
                         color_continuous_scale=px.colors.sequential.Tealgrn, title='Hulu - Country filmed')
    fig6.update_layout(title_font_family='Lato')
    return fig6


f6_hulu = figure6_hulu()

################################################ Graph 7 - Rating distribution


def figure7():
    net_filtered_ratings = df_netf[~df_netf["rating"].str.contains('min', na=False)]
    net_filtered_ratings = net_filtered_ratings[~net_filtered_ratings['rating'].str.contains('Season', na=False)]

    hulu_filtered_ratings = df_hulu[~df_hulu["rating"].str.contains('min', na=False)]
    hulu_filtered_ratings = hulu_filtered_ratings[~hulu_filtered_ratings['rating'].str.contains('Season', na=False)]

    netflix_ratings = net_filtered_ratings.dropna(subset=['rating']).groupby(['rating']).size().reset_index(
        name='count')
    hulu_ratings = hulu_filtered_ratings.dropna(subset=['rating']).groupby(['rating']).size().reset_index(name='count')

    fig7_net = px.treemap(netflix_ratings, path=['rating'], values='count', title='Netflix - Rating distribution',
                          height=700)
    fig7_net.update_layout(title_font_family='Lato')
    fig7_net.update_traces(hovertemplate='Rating: %{label}<br>Count: %{value}<extra></extra>')
    fig7_net.data[0].textinfo = 'label'

    fig7_hulu = px.treemap(hulu_ratings, path=['rating'], values='count', title='Hulu - Rating distribution',
                           height=700)
    fig7_hulu.update_layout(title_font_family='Lato')
    fig7_hulu.update_traces(hovertemplate='Rating: %{label}<br>Count: %{value}<extra></extra>')
    fig7_hulu.data[0].textinfo = 'label'

    return fig7_net, fig7_hulu


f7_netflix, f7_hulu = figure7()

################################################
app.layout = html.Div(style={'fontFamily': 'Lato', 'margin': '36px'}, children=[
    html.H1(children='Streaming Movies and TV Shows', style={'textAlign': 'center'}),
    html.Div([
        html.Div([
            html.Div([
                html.H4(children='Select the platforms to filter', style={'textAlign': 'center'}),
                html.Div([
                    dcc.Checklist(
                        ['Netflix', 'Hulu', 'Prime Video', 'Disney+'],
                        ['Netflix', 'Hulu'],
                        id='checklist', style={'width': '100%', 'display': 'flex', 'justifyContent': 'space-around'}),
                ], style={'width': '50%', 'margin': '0 25% 0 25%'}),
                dcc.Graph(
                    id='rotten-tomatoes',
                ),
            ], style={'margin': '0 0 20px 0', 'width': '50%', 'alignItems': 'center'}),
            dcc.Graph(
                id='age-distribution',
                figure=fig2,
                style={'width': '50%'}
            ),
        ], style={'display': 'flex', 'flexDirection': 'row'}),
        html.H2(children='Now, we will evaluate Hulu vs Netflix', style={'textAlign': 'center'}),
        html.Div([
            html.Div([
                "Starting Year: ",
                dcc.Dropdown(list(g_by_release.groups.keys()), 1923, id='start_y', style={'marginTop': 10})
            ],
                style={
                    "width": "25%",
                },
            ),
            html.Div([
                "End Year: ",
                dcc.Dropdown(list(g_by_release.groups.keys()), 2021, id='end_y', style={'marginTop': 10})
            ],
                style={
                    "width": "25%"
                },
            ),
        ], style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-around',
                  'width': '50%', 'margin': '0 25% 0 25%'}),
        dcc.Graph(
            id='content-release-date'
        ),
        html.Div([
            dcc.Graph(
                id='map_distribution',
                figure=f6,
                style={'width': '50%'}
            ),
            dcc.Graph(
                id='map_distribution_hulu',
                figure=f6_hulu,
                style={'width': '50%'}
            ),
        ], style={'display': 'flex', 'flexDirection': 'row'}),
        html.Div([
            dcc.Graph(
                id='box-plot1',
                figure=fig3,
                style={'width': '50%'}
            ),
            dcc.Graph(
                id='box-plot2',
                figure=fig3_series,
                style={'width': '50%'}
            ),
        ], style={'display': 'flex', 'flexDirection': 'row'}),
        html.Div([
            dcc.Graph(
                id='rating_netflix',
                figure=f7_netflix,
                style={'width': '50%'}
            ),
            dcc.Graph(
                id='rating_hulu',
                figure=f7_hulu,
                style={'width': '50%'}
            ),
        ], style={'display': 'flex', 'flexDirection': 'row'}),
    ]
        , style={
            "display": "flex",
            "justifyContent": "space-around",
            "fontWeight": "600",
            "flexDirection": 'column',
        }),
])

if __name__ == '__main__':
    app.run_server(debug=True)