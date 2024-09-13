import discord
import logging
import requests
from bs4 import BeautifulSoup

TOKEN = ''

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

client = discord.Client(intents=intents)


def fetch_html_economy():
    url = 'https://economia.uol.com.br/cotacoes/'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None


def fetch_html_news():
    url = 'https://g1.globo.com/'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error", {e})
        return None


def find_currency_value(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    cotation = soup.find_all('table', class_='data-table tableMoedas')
    prices = []
    for table in cotation:
        price_tds = table.find_all('td')
        for td in price_tds:
            price_tag = td.find('a')
            if price_tag:
                currency_price = price_tag.get_text(strip=True)
                prices.append(currency_price)

    grouped_prices = [prices[i:i + 3] for i in range(0, len(prices), 3)]

    formatted_prices = '\n'.join([' | '.join(group)
                                 for group in grouped_prices])

    return formatted_prices


def find_commodities(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table', class_='data-table')
    commodities = []
    for table in tables:
        cells = table.find_all('td')
        for cell in cells:
            commodities_text = cell.get_text(strip=True)
            if "Fonte" not in commodities_text:
                commodities.append(commodities_text)

    grouped_commodities = [commodities[i:i + 2]
                           for i in range(0, len(commodities), 2)]
    formatted_commodities = '\n'.join(
        [' | '.join(commoditie) for commoditie in grouped_commodities])
    return formatted_commodities


def find_news(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    news = soup.find_all(class_='feed-post bstn-item-shape type-materia')

    titles = []
    links = []
    dates = []

    for new in news[:10]:
        title = new.find('p')
        if title:
            title_text = title.get_text(strip=True)
            titles.append(title_text)

        link = new.find('a')
        if link:
            href = link.get('href')
            links.append(href)

        date = new.find(class_='feed-post-datetime')
        if date:
            span_text = date.get_text(strip=True)
            dates.append(span_text)

    formatted_entries = [f"{title}\n{link}\n{
        date}\n" for title, link, date in zip(titles, links, dates)]

    return formatted_entries


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!currency'):
        html_content = fetch_html_economy()
        if html_content:
            prices = find_currency_value(html_content)
            await message.channel.send('Valores atualizados das seguintes moedas (BRL):\n\n' + prices)
        else:
            await message.channel.send('Não foi possível obter os dados.')

    elif message.content.startswith('!commodities'):
        html_content = fetch_html_economy()
        if html_content:
            commodities_list = find_commodities(html_content)
            await message.channel.send('Valores econômicos atualizados:\n\n' + commodities_list)
        else:
            await message.channel.send('Não foi possível obter os dados.')

    elif message.content.startswith('!news'):
        html_content = fetch_html_news()
        if html_content:
            news_list = find_news(html_content)
            await message.channel.send('Principais notícias do dia:\n\n' + '\n'.join(news_list))

        else:
            await message.channel.send('Não foi possível obter os dados.')

client.run(TOKEN)
