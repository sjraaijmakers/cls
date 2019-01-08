import plotly as py
import plotly.graph_objs as go

import pandas as pd 

df = pd.read_csv("cars.csv")

# Map discrete values to numbers
mapping = {'US': 1, 'Europe': 2, 'Japan': 3}

df = df.replace({'origin': mapping})

df['year'] = df['year']+1900

cols = ['cylinders', 'horsepower', 'weight', 'MPG', 'year',]


data = [
    go.Parcoords(
        showlegend = True,
        line = dict(color = df['origin'], colorscale = [[0,'red'],[0.5,'blue'],[1,'green']]),
        dimensions = list([
            dict(label = 'Cylinders', values = df['cylinders'], tickvals=[3,4,5,6,7,8]),
            dict(label = 'Horsepower', values = df['horsepower']),
            dict(label = 'Weight (kg)', values = df['weight'], tickformat="~s"),
            dict(label = 'Miles per gallon', values = df['MPG']),
            dict(label = 'Year', values = df['year'], tickformat="~s"),
        ]),
        # dimensions = [
        #     dict(range = [df[col].min(), df[col].max()], label=col, values=df[col], tickformat="~s")
        #     for col in cols
        # ],
        hoverinfo = "x"
    )
]

layout = go.Layout(
    paper_bgcolor = '#f0f0f0',
    title = 'US = red, Europe = blue, Japan = Green'
)

fig = go.Figure(data = data, layout = layout)
py.offline.plot(fig, filename = 'cars.html')