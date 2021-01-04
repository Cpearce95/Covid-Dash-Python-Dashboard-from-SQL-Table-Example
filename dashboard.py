import pandas as pd,numpy as np,sqlalchemy as sa, os, time, datetime, smtplib, sys, plotly, plotly.express as px,yaml,json,gc
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from sqlalchemy import create_engine
from datetime import *



##Stylesheets/Bootstrap
external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css']
BS = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"

##Initialise app
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)


##Colors dict
colors = {
    'background': '#111111',
    'text': '#7FDBFF',
    'fontcolor':'#a99a86',
    'headercolor':'#bc987e'
}

###*****************************************************************************Getting Data
server,db = 'SERVER_NAME','covid_19_db'
engine = sa.create_engine(f'mssql+pyodbc://{server}/{db}?Trusted_Connection=yes&Driver=ODBC Driver 17 for SQL Server')
con = engine.connect()
q = r'select * from tbl_covid_worldometer'
df = pd.read_sql(q,con=con)


###*****************************************************************************Groupbys of data 
#g1 - Mean Total_Deaths by Location[:25]
g1 = df.groupby('Location')['Total_Cases'].mean().sort_values(ascending=False)[2:27]
g1cols,g1vals = [],[]
for c,v in g1.items():
    g1cols.append(c)
    g1vals.append(v)
#g2 - Mean New_Deaths by population[2:27]
g2 = df.groupby('Location')['New_Deaths'].mean().sort_values(ascending=False)[2:27]
g2cols,g2vals = [],[]
for c,v in g2.items():
    g2cols.append(c)
    g2vals.append(v)
#g3 - Total_Recovered by Location[:25]
g3 = df.groupby('Location')['Total_Recovered'].mean().sort_values(ascending=False)[2:27]
g3cols,g3vals = [],[]
for c,v in g3.items():
    g3cols.append(c)
    g3vals.append(v)
#g4 - New_Cases by Location[:25]
g4 = df.groupby('Location')['New_Cases'].mean().sort_values(ascending=False)[3:27]
g4cols,g4vals = [],[]
for c,v in g4.items():
    g4cols.append(c)
    g4vals.append(v)
###**********************************************************Figures of data     
##Figure 1 - Bar with orientation = h
fig1 = px.bar(df, x=g1vals,y=g1cols,orientation='h',color=g1cols,labels=dict(x="Total_Cases (Millions)", y="Country"))
fig1.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
##Figure 2 - Bar
fig2 = px.bar(df,x=g2vals,y=g2cols,color=g2cols,labels=dict(x='New Deaths (Last24Hrs)',y='Country'))
fig2.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
##Figure 3 - Funnel
fig3 = px.funnel(df, x=g3vals ,y=g3cols,labels=dict(x='Total Recovered',y='Country'))
fig3.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

##Figre 4 - Pie
fig4 = px.pie(df,values=g4vals ,names=g4cols)
fig4.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
###*****************************************************App layout
app.layout = html.Div(style={'backgroundColor': colors['background']},children =[
        html.Div([
                html.Div([
                        html.H2('Covid SQL table analysis', style = {'text-align':'center','color':colors['headercolor']}),
                    ],className = 'col-md-12'),
                ],className = 'row'),
                html.Div([
                    html.Div([
                        html.H3('Total_Cases by Country', style = {'text-align':'center','color':colors['fontcolor']}),
                        dcc.Graph(id='first', figure=fig1),
                    ], className = 'col-md-6'),
                    html.Div([
                        html.H3('New_Deaths by Country', style = {'text-align':'center','color':colors['fontcolor']}),
                        dcc.Graph(id='second', figure=fig2),
                    ], className = 'col-md-6'),
                ],className = 'row'),
                html.Div([
                    html.Div([
                        html.H3('Total_Recovered by Country', style = {'text-align':'center','color':colors['fontcolor']}),
                        dcc.Graph(id='third', figure=fig3),
                    ], className = 'col-md-6'),
                    html.Div([
                        html.H3('New_Cases by Location', style = {'text-align':'center','color':colors['fontcolor']}),
                        dcc.Graph(id='fourth', figure=fig4),
                    ], className = 'col-md-6'),
                ],className = 'row'),
        ],className = 'container-fluid')


##Run app 
if __name__ == '__main__':
    app.run_server(debug=True)
