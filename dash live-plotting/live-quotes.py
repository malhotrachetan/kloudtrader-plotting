import dash
import dash_core_components as dcc
import dash_html_components as html
import time
from kloudtrader.equities.data import *
from collections import deque
import plotly.plotly as py
import plotly.graph_objs as go
import random

app = dash.Dash('vehicle-data')

max_length = 50
times = deque(maxlen=max_length)
ASK = deque(maxlen=max_length)
BID = deque(maxlen=max_length)
VOLUME=deque(maxlen=max_length)



data_dict = {"ASK":ASK,
"BID": BID,
"Volume":VOLUME
}


def update_obd_values(ASK,BID):

    times.append(time.time())
    if len(times) == 1:
        quotes=live_quotes('AAPL',create_session())
        print(quotes)
        ASK.append(quotes['ask'])
        BID.append(quotes['bid'])
        VOLUME.append(1)
        
    else:
        for data_of_interest in [ASK,BID,VOLUME]:
            data_of_interest.append(data_of_interest[-1]+data_of_interest[-1]*random.uniform(-0.0001,0.0001))

    return ASK, BID, VOLUME

ASK,BID,VOLUME = update_obd_values(ASK,BID)

app.layout = html.Div([
    html.Div([
        html.H2('Live Quotes',
                style={'float': 'left',
                       }),
        ]),
        
    dcc.Dropdown(id='live-quotes',
                 options=[{'label': s, 'value': s}
                          for s in data_dict.keys()],
                 value=['ASK'],
                 multi=True
                 ),
    html.Div(children=html.Div(id='graphs'), className='row'),
    dcc.Interval(
        id='graph-update',
        interval=100),
    ], className="container",style={'width':'98%','margin-left':10,'margin-right':10,'max-width':50000})


@app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('live-quotes', 'value')],
    events=[dash.dependencies.Event('graph-update', 'interval')]
    )
def update_graph(data_names):
    graphs = []
    update_obd_values(ASK,BID,VOLUME)
    if len(data_names)>2:
        class_choice = 'col s12 m6 l4'
    elif len(data_names) == 2:
        class_choice = 'col s12 m6 l6'
    else:
        class_choice = 'col s12'


    for data_name in data_names:

        data = go.Scatter(
            x=list(times),
            y=list(data_dict[data_name]),
            name='Scatter',
            fill="tozeroy",
            fillcolor="#6897bb"
            )

        graphs.append(html.Div(dcc.Graph(
            id=data_name,
            animate=True,
            figure={'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(times),max(times)]),
                                                        yaxis=dict(range=[min(data_dict[data_name]),max(data_dict[data_name])]),
                                                        margin={'l':50,'r':1,'t':45,'b':1},
                                                        title='{}'.format(data_name))}
            ), className=class_choice))

    return graphs



external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_css:
    app.scripts.append_script({'external_url': js})


if __name__ == '__main__':
    app.run_server(debug=True)