
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from discord_webhook import DiscordWebhook, DiscordEmbed

name_crypto=input("What is the crypto you want to track? (bitcoin, ethereum, solana, terra,...)")
price_asking=input("What price must crypto reach for you to be warned?(in €)")


url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
  'slug': name_crypto,
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': ''#Put your api key,
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)['data']['1']['quote']['USD']
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)


def price_checker():
    global warning

    price_clean = json.loads(response.text)['data']['1']['quote']['USD']['price']

    if int(price_asking) <= int(price_clean):
        warning = "yes"

    else:
        warning = "no"


while True:
    price_checker()

    if warning == "yes":
        webhook_success = ""

        webhook = DiscordWebhook(url=webhook_success)
        embed = DiscordEmbed(title="Monitor Crypto", color=3066993)

        embed.set_author(
            name="Monitor crypto",
        )
        embed.add_embed_field(name='crypto name', value=str(name_crypto), inline=False)
        embed.add_embed_field(name='price', value=str(json.loads(response.text)['data']['1']['quote']['USD']['price']),
                              inline=False)
        embed.add_embed_field(name='price fluctuation', value=str(json.loads(response.text)['data']['1']['quote']['USD']['percent_change_24h']), inline=False)
        embed.add_embed_field(name='volume exchange', value=str(json.loads(response.text)['data']['1']['quote']['USD']['volume_change_24h']),
                              inline=False)
        embed.add_embed_field(name='market cap dominance', value=str(json.loads(response.text)['data']['1']['quote']['USD']['market_cap_dominance']+'%'), inline=False)

        webhook.add_embed(embed)

        embed.set_timestamp()
        response = webhook.execute(remove_embeds=True)

        break
