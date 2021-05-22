from urllib.request import urlopen as uRequest
from bs4 import BeautifulSoup as soup

url = 'https://www.billboard.com/charts/hot-100'

# Opening up connection, grabbing the page
uClient = uRequest(url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")

containers = page_soup.select('article[class*=chart]') # *= means contains

filename = 'billboard_hot_100.csv'
f = open(filename, 'w') 

headers = 'Song, Artist, Last Week, Peak Position, Weeks on Chart\n'

f.write(headers)

chart_position = 1

for container in containers:

    song_container = container.find('div', {'class': 'chart-row__title'})

    song = song_container.h2.text
    
    try:
        artist = song_container.a.text.strip()
    except AttributeError:
        artist = song_container.span.text.strip()

    last_week_container = container.find('div', {'class': 'chart-row__last-week'})
    last_week = last_week_container.find('span', {'class': 'chart-row__value'}).text

    peak_position_container = container.find('div', {'class': 'chart-row__top-spot'})
    peak_position = peak_position_container.find('span', {'class': 'chart-row__value'}).text

    weeks_on_chart_container = container.find('div', {'class': 'chart-row__weeks-on-chart'})
    weeks_on_chart = weeks_on_chart_container.find('span', {'class': 'chart-row__value'}).text

    if print_data:
        print('\nPosition: #{}'.format(chart_position))
        print('Song: {}'.format(song))
        print('Artist: {}'.format(artist))
        print('Last Week: {}'.format(last_week))
        print('Peak Position: {}'.format(peak_position))
        print('Weeks on Chart: {}'.format(weeks_on_chart))

    chart_position += 1

    f.write('\"' + song + '\",\"' + artist.replace('Featuring', 'Feat.') + '\",' + last_week + ',' + peak_position + ',' + weeks_on_chart + '\n')

f.close()