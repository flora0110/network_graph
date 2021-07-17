import dash
import dash_html_components as html
app = dash.Dash()
app.layout = html.Div(children=[
               html.H1(children='Hellooo Dash'),
               html.Div(
                 children='''Dash: A web application framework for
                 Python.''')
             ])
if __name__ == '__main__':
  app.run_server(debug=True)
