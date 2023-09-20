import requests
import selectorlib
import os
import smtplib
import ssl
import time

PASSWORD = os.getenv("PASSWORD")

# from bs4 import BeautifulSoup

URL = "https://programmer100.pythonanywhere.com/tours/"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def scrape(url):
    # Get respose code
    response = requests.get(url=url)  # , headers=HEADERS)
    # Get html text from response code
    html = response.text
    # print(response)
    # print(source)
    return html


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    print('extracted_value:', value)

    # Split the string by "Next Tour:" and take the second part
    value = value.split('Next Tour:')[0].strip()
    print(value)

    if value != "No upcoming tours":
        # Split the string into words
        value = value.split()
        print("value_split:", value)
        # Exclude the last two words
        value = ' '.join(value[:-2])

        # print(next_tour_portion)
        print('value:', value)
    return value


# def send_email():
#     print("Email sent")

def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "shibbirahmedd@gmail.com"
    password = PASSWORD

    receiver = "shibbirahmedd@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        # Sending mail
        server.sendmail(username, receiver, message)

    print("Email sent")


def store(extracted):
    with open("data.txt", "a") as file:
        file.write(extracted + "\n")

def read():
    with open("data.txt", "r") as file:
        data = file.read()
        return data

if __name__ == "__main__":

    while True:
        html_text = scrape(URL)
        # print(html_text)

        extracted = extract(html_text)
        print('extracted:', extracted)

        data = read()

        if extracted != "no upcoming tours":
            # if extracted not in "data.txt":  # if not extracted  in "data.txt":   # this also works
            #     send_email()

            if extracted not in data:
                store(extracted)
                send_email(message="Hey, new event was found!")

        time.sleep(2)