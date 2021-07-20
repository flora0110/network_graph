import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import igraph as ig
import json
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import plotly
from plotly.offline import *
import plotly.graph_objects as go
def make_edge(x, y, z, width):
    if(width>150) : width=150
    #if(width<8) : width=8
    return  go.Scatter3d(x=x,
                           y=y,
                           z=z,
                           mode='lines',
                           line=dict(color='rgba(76,76,76,0.006)', width=round(width/10,2)),
                           hoverinfo='none'
                           )

data = []
#req = urllib2.Request("https://raw.githubusercontent.com/plotly/datasets/master/miserables.json")
req = urllib2.Request("https://raw.githubusercontent.com/flora0110/network_graph/master/node_connect_2.json")
opener = urllib2.build_opener()
f = opener.open(req)
data = json.loads(f.read())



N=len(data['nodes'])
N=173
#for node in data['nodes']:
#    print(node['name'])

#Define the list of edges and the Graph object from Edges:
L=len(data['links'])
Edges=[(data['links'][k]['source'], data['links'][k]['target']) for k in range(L)]
edge_width = [(data['links'][k]['value']) for k in range(L)]


G=ig.Graph(Edges, directed=False)

labels=[]
group=[]
for node in data['nodes']:
    labels.append(node['name'])
    #group.append(node['group'])

#Get the node positions, set by the Kamada-Kawai('kk') layout for 3D graphs
#turn to random,circle
layt=G.layout('circle', dim=3)
#layt is a list of three elements lists (the coordinates of nodes):

#Set data for the Plotly plot of the graph:
#for k in range(N) :
#    print(k)
#    print(data['nodes'][k])
#    print(layt[k][0])
Xn=[layt[k][0] for k in range(N)]# x-coordinates of nodes
Yn=[layt[k][1] for k in range(N)]# y-coordinates
Zn=[layt[k][2] for k in range(N)]# z-coordinates
Xe=[]
Ye=[]
Ze=[]
a=0
data_total = []
for e in Edges:
    Xe=[layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
    Ye=[layt[e[0]][1],layt[e[1]][1], None]
    Ze=[layt[e[0]][2],layt[e[1]][2], None]
    data_total.append(make_edge(Xe, Ye, Ze, edge_width[a]))
    a=a+1

sizes = [0]*N
for i in range(len(Edges)) :
    sizes[Edges[i][0]] = sizes[Edges[i][0]]+1
    sizes[Edges[i][1]] = sizes[Edges[i][1]]+1
sizes[0] = 60
i=0
while(i<len(sizes)):
    if(sizes[i]==0) :
        del Xn[i]
        del Yn[i]
        del Zn[i]
        del labels[i]
        del sizes[i]
    else : i=i+1
color = ["rgba(255,255,255,0.2)"]*len(sizes)
for i in range(len(sizes)):
    if(sizes[i]>40) :
        color[i] = "rgba(38,16,238,0.8)"
    elif(sizes[i]>25) :
        color[i] = "rgba(16,42,238,0.6)"
    elif(sizes[i]>15) :
        color[i] = "rgba(18,70,241,0.45)"
    elif(sizes[i]>3) :
        color[i] = "rgba(18,152,241,0.3)"

node_trace = go.Scatter3d(x=Xn,
                   y=Yn,
                   z=Zn, text=labels,
    #mode='markers+text',
    mode='text',
    name='actors',
    showlegend=False,
    hoverinfo='none',
    #size = sizes,
    textfont=dict(
        family="sans serif",
        size=sizes,
        color=color
    ))
data_total.append(node_trace)
axis=dict(showbackground=False,
          showline=False,
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title=''
          )

layout = go.Layout(
        #paper_bgcolor='#181818',
        paper_bgcolor="#080808",
         title="倚天屠龍記人物關係圖",
         title_font_size=50,
         title_font_color='white',
         width=1300,
         height=900,
         showlegend=False,
         scene=dict(
             xaxis=dict(axis),
             yaxis=dict(axis),
             zaxis=dict(axis),
        ),
     margin=dict(
        t=100
    ),
    hovermode='closest',
    annotations=[
           dict(
           showarrow=False,
            text="Data source: <a href='https://raw.githubusercontent.com/flora0110/network_graph/master/node_connect_2.json'>[1] node_connect_2.json</a>",
            xref='paper',
            yref='paper',
            x=0,
            y=0.1,
            xanchor='left',
            yanchor='bottom',
            font=dict(
            size=14
            )
            )
        ],    )
#data=[trace1, trace2]
#fig=go.Figure(data=data, layout=layout)
fig=go.Figure(data=data_total, layout=layout)

plotly.offline.plot(fig, filename='Les-Miserables')

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
