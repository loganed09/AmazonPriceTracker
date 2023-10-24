import requests
import smtplib
import lxml
from bs4 import BeautifulSoup
from pprint import pprint
import os

MY_EMAIL = os.environ.get("EMAIL")
EMAIL_PASSWORD = os.environ.get("EMAIL_PW")

amazon_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}


invincible_2_response = requests.get(url=os.environ.get("INVINCIBLE_2"), headers=amazon_headers)
invincible_2_response_webpage = invincible_2_response.text

soup = BeautifulSoup(invincible_2_response_webpage, "lxml")

price_soup = soup.select("#tmmSwatches .a-color-price")
price = float(price_soup[1].getText().strip().split('$')[1])

product_title = soup.select_one("#productTitle").getText().strip()

print(product_title)

if price < 55:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=EMAIL_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs='loganed092023@gmail.com',
            msg=f"Subject: {product_title} is less than $55\n\n{product_title} is now only ${price}"
        )