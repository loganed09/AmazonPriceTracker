import requests
import smtplib
import lxml
from bs4 import BeautifulSoup
from pprint import pprint
import os
from termcolor import colored
from wish_list import item_list

MY_EMAIL = os.environ.get("EMAIL")
EMAIL_PASSWORD = os.environ.get("EMAIL_PW")

amazon_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

message = ''

for _ in range(len(item_list)):
    response = requests.get(url=item_list[_]["url"], headers=amazon_headers)
    response_webpage = response.text
    soup = BeautifulSoup(response_webpage, "lxml")

    if "LEGO" in item_list[_]["title"]:
        price_soup = soup.select_one("#corePrice_feature_div .a-offscreen")
        price = float(price_soup.getText().strip().split('$')[1])
    else:
        price_soup = soup.select("#tmmSwatches .a-color-price")
        #print(price_soup)
        price = float(price_soup[1].getText().strip().split('$')[1])

    product_title = soup.select_one("#productTitle").getText().strip()

    if price < item_list[_]["price_wanted"]:
        # deal_list.append(item_list[_]["title"])
        message += f"{product_title}is now only ${price}\n\n"


print(message)


with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=EMAIL_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs='loganed092023@gmail.com',
            msg=f"Subject: New Products from Wish List are on Sale!\n\n{message}"
        )