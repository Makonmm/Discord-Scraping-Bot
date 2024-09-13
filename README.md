# Discord Bot for Economic and News Scraping

### Features:

- Command: !currency
The bot scrapes data from the UOL Economia website to retrieve the current exchange rates of various currencies against the Brazilian Real (BRL).
Output: The bot sends a list of currency prices in a tabular format, grouped by currency pairs.
Commodities Information:

- Command: !commodities
The bot also scrapes the UOL Economia website to collect information about economic commodities.
Output: The bot presents a list of commodity values, formatted for easy reading.
News Information:

- Command: !news
The bot scrapes the G1 Globo website to fetch the top news stories of the day.
Output: The bot sends the top 10 news stories, including titles, links, and publication dates.

### Technologies used:

- Python
- discord.py
- requests
- BeautifulSoup


### Installation:

1. Clone this repository:
    ```shell
    git clone https://github.com/Makonmm/Discord-Scraping-Bot

    ```
2. Install dependecies:
    ```shell
    pip install discord requests beautifulsoup4
    ```

### Notes:
- Ensure that your bot has the appropriate permissions to read and send messages in the Discord server.
- The HTML structure of the websites may change, which might require adjustments to the scraping code.
- The bot uses an authentication token (TOKEN) that needs to be configured to authenticate with the Discord API.