import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from dash import dash_table

# Load the dataset
df = pd.read_csv('ProcessedTweets.csv')

# Create the Dash app
app = dash.Dash(__name__)
server = app.server
# Define the layout
app.layout = html.Div([
    html.H1("Twitter Data Dashboard", style={'text-align': 'center'}),
    
    html.Div([
        html.Label("Select Month:"),
        dcc.Dropdown(
            id='month-dropdown',
            options=[{'label': month, 'value': month} for month in df['Month'].unique()],
            value=df['Month'].unique()[0]
        )
    ], style={'display': 'inline-block', 'margin-bottom': '20px', 'width': '30%', 'margin-right': '10px'}),
    
    html.Div([
        html.Label("Sentiment Range:"),
        dcc.RangeSlider(
            id='sentiment-slider',
            min=df['Sentiment'].min(),
            max=df['Sentiment'].max(),
            step=0.1,
            marks={i: str(i) for i in range(-1, 2)},
            value=[df['Sentiment'].min(), df['Sentiment'].max()]
        )
    ], style={'display': 'inline-block', 'margin-bottom': '20px', 'width': '30%', 'margin-right': '10px'}),
    
    html.Div([
        html.Label("Subjectivity Range:"),
        dcc.RangeSlider(
            id='subjectivity-slider',
            min=df['Subjectivity'].min(),
            max=df['Subjectivity'].max(),
            step=0.1,
            marks={i: str(i) for i in range(0, 2)},
            value=[df['Subjectivity'].min(), df['Subjectivity'].max()]
        )
    ], style={'display': 'inline-block', 'margin-bottom': '20px', 'width': '30%'}),
    
    dcc.Graph(id='scatter-plot', config={'modeBarButtonsToAdd': ['lasso2d']}),
    
    html.Div([
        html.H2("Tweets", style={'text-align': 'center'})
    ]),
    
    html.Div([
        dash_table.DataTable(id='tweet-table',
                             columns=[{"name": " ", "id": "tweet"}],
                             style_table={'overflowX': 'auto'},
                             page_size=10,
                             style_cell={'textAlign': 'center', 'whiteSpace': 'normal', 'height': 'auto'},
                             style_header={'textAlign': 'center', 'whiteSpace': 'normal', 'height': 'auto'}
        )
    ], style={'width': '80%', 'margin': 'auto'})
])

# Define callback to update scatter plot
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('month-dropdown', 'value'),
     Input('sentiment-slider', 'value'),
     Input('subjectivity-slider', 'value')]
)
def update_scatter_plot(selected_month, sentiment_range, subjectivity_range):
    filtered_df = df[(df['Month'] == selected_month) &
                     (df['Sentiment'] >= sentiment_range[0]) & (df['Sentiment'] <= sentiment_range[1]) &
                     (df['Subjectivity'] >= subjectivity_range[0]) & (df['Subjectivity'] <= subjectivity_range[1])]
    
    fig = px.scatter(filtered_df, x='Dimension 1', y='Dimension 2', custom_data=[filtered_df.index])
    fig.update_traces(marker=dict(color='blue', size=10), hoverinfo='text')
    fig.update_layout(title='',
                      xaxis_title='',
                      yaxis_title='',
                      modebar={'orientation': 'v'})
    fig.update_layout(hoverlabel=dict(bgcolor="white", font_size=12, font_family="Rockwell"))
    fig.update_traces(hovertemplate='%{text}')
    return fig

# Define callback to update tweet display table
@app.callback(
    Output('tweet-table', 'data'),
    [Input('scatter-plot', 'selectedData')]
)
def display_selected_tweet(selectedData):
    if selectedData:
        indices = [point['customdata'][0] for point in selectedData['points']]
        tweets = [{'tweet': df.iloc[index]['RawTweet']} for index in indices]
        return tweets
    else:
        return []

if __name__ == '__main__':
    app.run_server(debug=True)
