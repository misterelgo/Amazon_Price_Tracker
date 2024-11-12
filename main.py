import ssl
import requests
from bs4 import BeautifulSoup
import os
from email.message import EmailMessage
import smtplib
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


Amazon_link = "https://appbrewery.github.io/instant_pot/"
r = requests.get(Amazon_link)
print(r.status_code)
soup = BeautifulSoup(r.text, 'html.parser')
product_price_whole = soup.find('span',"a-price-whole")
product_price_floating_number = soup.find('span',"a-price-fraction")
product_price = float(product_price_whole.text + product_price_floating_number.text)
product_title = soup.find(id="productTitle").get_text().strip()

print(product_title)
print(product_price)

preset_value = 100

#sending email notification
email_receiver = os.environ.get("EMAIL_ADDRESS")
email_password = os.environ.get("EMAIL_PASSWORD")
email_sender = os.environ.get("EMAIL_ADDRESS")
print("email_sender", email_sender)
#Mail content
subject = "Price Drop Alert from Amazon"
body = f"{product_title} is now at {preset_value}."

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

# send the mail
context = ssl.create_default_context()
if product_price <= preset_value:
    with smtplib.SMTP_SSL(os.environ.get("SMTP_ADDRESS"), 465, context=context) as connection:
        connection.login(email_sender, email_password)
        connection.sendmail(email_sender, email_receiver, em.as_string())