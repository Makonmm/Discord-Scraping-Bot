import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)


def fetch_html():
    url = 'https://economia.uol.com.br/cotacoes/'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Erro: {e}")
        return None


def find_currency_value(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    cotation = soup.find_all('table', class_='data-table tableMoedas')
    prices = []
    for i in cotation:
        price_tds = i.find_all('td')
        for td in price_tds:
            price_tag = td.find('a')
            if price_tag:
                currency_price = price_tag.get_text(strip=True)
                prices.append(currency_price)
    return prices


def find_commodities(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table', class_='data-table')
    commodities = []
    for table in tables:
        cells = table.find_all('td')
        for cell in cells:
            commodities_text = cell.get_text(strip=True)
            commodities.append(commodities_text)
    return commodities


@app.route('/currency', methods=['GET'])
def currency():
    html_content = fetch_html()
    if html_content:
        prices = find_currency_value(html_content)
        return jsonify(prices)
    else:
        return jsonify({'error'}), 500


@app.route('/commodities', methods=['GET'])
def commodities():
    html_content = fetch_html()
    if html_content:
        commodities_list = find_commodities(html_content)
        return jsonify(commodities_list)
    else:
        return jsonify({'error'}), 500


if __name__ == '__main__':
    app.run(debug=True)
