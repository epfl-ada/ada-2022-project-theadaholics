# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import pandas as pd
# import matplotlib.pyplot as plt
import plotly.express as px

app = Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
fig.write_html("file.html")

# 'backgroundColor': colors['background'],
app.layout = html.Div(style={ 'display': 'flex', 'flex-direction': 'row'}, children=[
    
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    

    # html.Div(children='Dash: A web application framework for your data.', style={
    #     'textAlign': 'center',
    #     'color': colors['text']
    # }),

    html.Div(children=[
        # html.Label('Dropdown'),
        dcc.Graph(
          id='example-graph-2'
            # figure=fig
        ),
        dcc.Dropdown(['New York City', 'Montreal', 'SF'],'Montreal',id='ddown')

        

    ], style={'padding': 10, 'flex': 1})  

   
])

@app.callback(
    Output(component_id='example-graph-2', component_property='figure'),
    Input(component_id='ddown', component_property='value')
)
def update_figure(selected_city):
    print(selected_city)
    filtered_df = df[df['City'] == selected_city]

    fig = px.bar(filtered_df, x="Fruit", y="Amount", color="City", barmode="group")

    fig.update_layout(transition_duration=500)
    
    print(filtered_df)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
    





