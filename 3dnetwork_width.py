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
    return  go.Scatter3d(x=x,
                           y=y,
                           z=z,
                           mode='lines',
                           line=dict(color='rgb(125,125,125)', width=width),
                           hoverinfo='none'
                           )

data = []
req = urllib2.Request("https://raw.githubusercontent.com/plotly/datasets/master/miserables.json")
opener = urllib2.build_opener()
f = opener.open(req)
data = json.loads(f.read())

print (data.keys())

N=len(data['nodes'])
print(N)

#Define the list of edges and the Graph object from Edges:
L=len(data['links'])
Edges=[(data['links'][k]['source'], data['links'][k]['target']) for k in range(L)]

G=ig.Graph(Edges, directed=False)
print(data['nodes'][0])

labels=[]
group=[]
for node in data['nodes']:
    labels.append(node['name'])
    group.append(node['group'])

#Get the node positions, set by the Kamada-Kawai layout for 3D graphs
layt=G.layout('kk', dim=3)
#layt is a list of three elements lists (the coordinates of nodes):
print(layt[5])
#Set data for the Plotly plot of the graph:
Xn=[layt[k][0] for k in range(N)]# x-coordinates of nodes
Yn=[layt[k][1] for k in range(N)]# y-coordinates
Zn=[layt[k][2] for k in range(N)]# z-coordinates
Xe=[]
Ye=[]
Ze=[]
a=1
data_total = []
for e in Edges:
    Xe=[layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
    Ye=[layt[e[0]][1],layt[e[1]][1], None]
    Ze=[layt[e[0]][2],layt[e[1]][2], None]
    data_total.append(make_edge(Xe, Ye, Ze, a))

#線條
"""
trace1=go.Scatter3d(x=Xe,
               y=Ye,
               z=Ze,
               mode='lines',
               line=dict(color='rgb(125,125,125)', width=1),
               hoverinfo='none'
               )
"""
trace2=go.Scatter3d(x=Xn,
               y=Yn,
               z=Zn,
               mode='markers',
               name='actors',
               marker=dict(symbol='circle',
                             size=6,
                             color=group,
                             colorscale='Viridis', # choose a colorscale
                             line=dict(color='rgb(50,50,50)', width=0.5)
                             ),
               text=labels,
               hoverinfo='text'
               )
data_total.append(trace2)
axis=dict(showbackground=False,
          showline=False,
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title=''
          )

layout = go.Layout(
         title="Network of coappearances of characters in Victor Hugo's novel<br> Les Miserables (3D visualization)",
         width=1000,
         height=1000,
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
            text="Data source: <a href='http://bost.ocks.org/mike/miserables/miserables.json'>[1] miserables.json</a>",
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
