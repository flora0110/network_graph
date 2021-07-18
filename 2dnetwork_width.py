import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import networkx as nx

def make_edge(x, y, width):
    """
    Args:
        x: a tuple of the x from and to, in the form: tuple([x0, x1, None])
        y: a tuple of the y from and to, in the form: tuple([y0, y1, None])
        width: The width of the line

    Returns:
        a Scatter plot which represents a line between the two points given.
    """
    return  go.Scatter(
                x=x,
                y=y,
                line=dict(width=width,color='#888'),
                hoverinfo='none',
                mode='lines')

# Plotly figure
edges = [['K', 'B'], ['B', 'C'], ['B', 'D']]
G = nx.Graph()
G.add_edges_from(edges)
pos = nx.spring_layout(G) #布局指定节点排列形式

# edges trace
edge_x = []
edge_y = []
data_total = []
a=1

for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_y.append(y0)
    edge_y.append(y1)
    data_total.append(make_edge(edge_x, edge_y, a))
    a=a+1
    del edge_x[0]
    del edge_x[0]
    del edge_y[0]
    del edge_y[0]
"""
x0, y0 = pos[edges[0][0]]
x1, y1 = pos[edges[0][1]]
edge_x.append(x0)
edge_x.append(x1)
edge_x.append(None)
edge_y.append(y0)
edge_y.append(y1)
edge_y.append(None)
print(edge_x)
print(edge_y)
edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(color='black', width=3),
    hoverinfo='none',
    showlegend=False,
    mode='lines')
data_total.append(edge_trace)
"""
# nodes trace
node_x = []
node_y = []
text = []

for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    text.append(node)


node_trace = go.Scatter(
    x=node_x, y=node_y, text=text,
    mode='markers+text',
    showlegend=False,
    hoverinfo='none',
    marker=dict(
        color='pink',
        size=50,
        line=dict(color='black', width=1)))

data_total.append(node_trace)

# layout
layout = dict(plot_bgcolor='white',
                paper_bgcolor='white',
                margin=dict(t=10, b=10, l=10, r=10, pad=0),
                xaxis=dict(linecolor='black',
                             showgrid=False,
                             showticklabels=False,
                             mirror=True),
                yaxis=dict(linecolor='black',
                             showgrid=False,
                             showticklabels=False,
                             mirror=True))

# figure
fig = go.Figure(data=data_total, layout=layout)

# Dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Dash Networkx'

app.layout = html.Div([
        html.I('Write your EDGE_VAR'),
        #html.Br(),
        #dcc.Input(id='EGDE_VAR', type='text', value='K', debounce=True),
        dcc.Graph(id='my-graph',figure=fig),
    ]
)



if __name__ == '__main__':
    app.run_server(debug=True)
