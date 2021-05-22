import plotly.graph_objects as go
from plotly.subplots import make_subplots

tracksFile = open('tracks.csv')

yearIndicator = dict()

for line in tracksFile:
    meta = line.split(',')
    trackID = meta[3].replace('\n','')
    year = meta[0]
    yearIndicator[trackID] = year

featureFile = open('features.csv')
fields = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 
        'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']

year_bucket = dict()

for line in featureFile:
    meta = line.split(',')
    trackID = meta[11].replace('\n','')
    year = yearIndicator[trackID]
    block = dict()

    for i, d in enumerate(meta):
        if i != 11:
            block[fields[i]] = float(meta[i])
            if fields[i] == 'tempo':
                block[fields[i]] = (block[fields[i]] - 60) / 60

    if year not in year_bucket:
        year_bucket[year] = []
    year_bucket[year].append(block)


fig = make_subplots(rows=2, cols=3, subplot_titles=("1970", "1980", "1990", "2000", "2010", "2019"))
mat = dict()

for year in year_bucket:
    data = year_bucket[year]
    mat[year] = dict()
    for field in fields:
        mat[year][field] = []
    for d in data:
        for field in fields:
            mat[year][field].append(d[field])

maxF = dict()
minF = dict()

for year in mat:
    for field in mat[year]:
        maxV = max(mat[year][field])
        minV = min(mat[year][field])
        if field not in maxF or maxV > maxF[field]:
            maxF[field] = maxV
        if field not in minF or minV < minF[field]:
            minF[field] = minV

for year in mat:
    for field in mat[year]:
        maxV = maxF[field]
        minV = minF[field]
        for i in range(len(mat[year][field])):
            mat[year][field][i] = (mat[year][field][i] - minV) / (maxV - minV)

counter = 0

for year in ['1970', '1980', '1990', '2000', '2010', '2019']:
    for field in mat[year]:
        fig.add_trace(go.Box(
            y=mat[year][field],
            name=field,
            boxpoints='outliers', # only outliers
            marker_color='rgb(107,174,214)',
            line_color='rgb(107,174,214)'
        ),row=int(counter/3) + 1, col=counter%3 + 1)
    counter += 1

fig.update_layout(title_text="Music features at different era", showlegend=False, height=800, width=1500)
fig.show()