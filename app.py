from requests_html import HTMLSession
from tqdm import tqdm
import pandas as pd

s = HTMLSession()
r = s.get("https://www.coingecko.com/en")
print(r.status_code)

## NAME
name = r.html.find(
    'a[class="tw-hidden lg:tw-flex font-bold tw-items-center tw-justify-between"]'
)
name_list = []
coin_url_list = []
for x in name:
    name_list.append(x.text)
    coin_url_list.append(f"https://www.coingecko.com{x.attrs['href']}")

## PRICE
price = r.html.find('td[class="td-price price text-right"]')
price_list = []
for x in price:
    price_list.append(x.text)

## VOLUME
volume = r.html.find('td[class="td-liquidity_score lit text-right %> col-market"]')
volume_list = []
for x in volume:
    volume_list.append(x.text)

## MARKET CAP
marketcap = r.html.find('td[class="td-market_cap cap col-market cap-price text-right"]')
marketcap_list = []
for x in marketcap:
    marketcap_list.append(x.text)

print(len(name_list))
print(len(price_list))
print(len(volume_list))
print(len(marketcap_list))
print(len(coin_url_list))

## PAGINATION
next_page_btn = r.html.find('a[aria-label="next"]', first=True)

for i in range(4):
    if next_page_btn:
        try:
            url_part = next_page_btn.attrs["href"].replace("2", "")
            url = f"https://www.coingecko.com{url_part + str(i+2)}"
            r = s.get(url)
            print(url)
            print(r.status_code)

            ## NAME
            name = r.html.find(
                'a[class="tw-hidden lg:tw-flex font-bold tw-items-center tw-justify-between"]'
            )
            for x in name:
                name_list.append(x.text)
                coin_url_list.append(f"https://www.coingecko.com{x.attrs['href']}")

            ## PRICE
            price = r.html.find('td[class="td-price price text-right"]')
            for x in price:
                price_list.append(x.text)

            ## VOLUME
            volume = r.html.find(
                'td[class="td-liquidity_score lit text-right %> col-market"]'
            )
            for x in volume:
                volume_list.append(x.text)

            ## MARKET CAP
            marketcap = r.html.find(
                'td[class="td-market_cap cap col-market cap-price text-right"]'
            )
            for x in marketcap:
                marketcap_list.append(x.text)

            print(len(name_list))
            print(len(price_list))
            print(len(volume_list))
            print(len(marketcap_list))
            print(len(coin_url_list))

        except:
            print("...")

## CIRCULATION
circulation_list = []
for x in  coin_url_list:
    r = s.get(x)
    cir = r.html.find('span[class="tw-text-gray-900 dark:tw-text-white tw-float-right tw-font-medium tw-mr-1"]', first=True)
    circulation_list.append(cir.text.strip())
    print(cir.text.strip())
    
print(len(circulation_list))

## DISPLAYING
try:
    df = pd.DataFrame(
        {
            "Name": name_list,
            "Price": price_list,
            "Volume": volume_list,
            "Market Cap": marketcap_list,
            "Circulation": circulation_list
        }
    )
    df.to_csv("Rakshith.csv")
except:
    print(len(name_list))
    print(len(price_list))
    print(len(volume_list))
    print(len(marketcap_list))
    print(len(coin_url_list))
    print(len(circulation_list))