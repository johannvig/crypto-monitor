import re
import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed
import warnings
warnings.filterwarnings('ignore')


name_crypto=input("What is the crypto you want to track? (bitcoin, ethereum, solana, terra,...)")
price_asking=input("What price must crypto reach for you to be warned?(in €)")

def price_checker():
    global a
    global price
    global warning
    global soup
    global price_fluctuation

    headers = {
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "DNT": "1",
        "referer": "http://www.google.com/",
        "origin": "http://www.google.com/",
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'Upgrade-Insecure-Requests': '1',
        'sec-ch-ua': '" Not A;Brand";v="99", '
                     '"Chromium";v="96", "Google '
                     'Chrome";v="96"',
        'connection': 'keep-alive'

    }

    r = requests.get("https://coinmarketcap.com/fr/currencies/"+name_crypto+"/", headers=headers)
    data = r.content  # Content of response
    soup = BeautifulSoup(data, "html.parser")
    a = soup.find_all('td')



    price = soup.find("div", {"class": "priceValue"}).get_text(strip=True)


    price = str(price.strip())
    price_clean = price.replace("€", "")
    price_clean = price_clean.replace(",", "")
    price_clean = price_clean.split('.')
    price_clean = price_clean[0]






    if int(price_asking)<= int(price_clean):
        warning="yes"

        price_fluctuation = soup.find("span", {"class": "sc-15yy2pl-0 gEePkg"}).get_text(strip=True)
        price_fluctuation=price_fluctuation.strip()
    else:
        warning="no"




def volume_echange():
    global volume_echange_clean

    volume_echange = re.search('</div></td>, <td><span>€(.+?)</span><div><span class="sc-15yy2pl-0 kAXKAX', str(a))

    volume_echange_clean = str(volume_echange)
    volume_echange_clean = volume_echange_clean.replace("</span><>", "")
    volume_echange_clean = volume_echange_clean.split('<span>')
    volume_echange_clean = volume_echange_clean[1]




def offre_en_circulation():

    global offre_en_circulation_clean

    offre_en_circulation = re.search('ETH</td>, <td>(.+?)ETH</td>, <td>Aucune Donnée</td>]', str(a))

    offre_en_circulation_clean = str(offre_en_circulation)
    offre_en_circulation_clean = offre_en_circulation_clean.replace("</td>, <td>Aucune Do>", "")
    offre_en_circulation_clean = offre_en_circulation_clean.split('<td>')
    offre_en_circulation_clean = offre_en_circulation_clean[1]





while True:
    price_checker()

    if warning == "yes":
        volume_echange()
        offre_en_circulation()


        webhook_success = ""

        webhook = DiscordWebhook(url=webhook_success)
        embed = DiscordEmbed(title="Monitor Crypto", color=3066993)

        embed.set_author(
            name="Monitor crypto",
        )
        embed.add_embed_field(name='crypto name', value=str(name_crypto), inline=False)
        embed.add_embed_field(name='price', value=str(price), inline=False)
        embed.add_embed_field(name='price fluctuation', value=str(price_fluctuation), inline=False)
        embed.add_embed_field(name='volume exchange', value=str(volume_echange_clean),
                              inline=False)
        embed.add_embed_field(name='offre en circulation', value=str(offre_en_circulation_clean), inline=False)

        webhook.add_embed(embed)

        embed.set_timestamp()
        response = webhook.execute(remove_embeds=True)


        break
