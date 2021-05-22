from plotly.subplots import make_subplots
import plotly.graph_objects as go
import json

fig = make_subplots(rows=2, cols=3, 
    specs=[[{"type":"polar"}, {"type":"polar"}, {"type":"polar"}], [{"type":"polar"}, {"type":"polar"}, {"type":"polar"}]])

years = ['1970', '1980', '1990', '2000', '2010', '2019']
stats = []

for index, year in enumerate(years):
    text = open('data/' + year + '.json').read()
    stats.append(json.loads(text))

data = []

for i in range(len(stats)):
    data.append(dict())
    for field in stats[i]:
        if field not in ['count', 'tempo']:
            data[i][field] = stats[i][field] / stats[i]['count']
        if field == 'tempo':
            data[i][field] = ((stats[i][field] - 60) / 60) / stats[i]['count']

categories = list(data[i].keys())

for i in range(len(data)):
    d = data[i]

    print(d.values())

    fig.add_trace(go.Scatterpolar(
        r=list(d.values()),
        theta=categories,
        fill='toself',
        name='Product A'
    ),row=int(i/3) + 1, col=i%3 + 1)
    

fig.update_layout(height=800, width=1600, title_text='Radar Plot of All Clusters (Fig.4)')

fig.show()


#boxplot