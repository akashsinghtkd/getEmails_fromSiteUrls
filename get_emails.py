import urllib
import os
import requests
import re
# from urllib.parse import urljoin
from urllib.parse import urlparse

url = 'https://www.google.com/'
protocol = (urllib.parse.urlsplit(url)).scheme
base_url = urlparse(url).netloc
regEx_url = protocol+"?:\/\/(.+?\.)?" + base_url + "(\/[A-Za-z0-9\-\._~:\/\?#\[\]@!$&'\(\)\*\+,;\=]*)?"
regEx_email = '[\w.+-]+@[\w-]+\.[\w.-]+'
allUrls = []
allEmails = []
count = 0


def is_url_valid(URL):
    split_tup = os.path.splitext(URL)
    extensions = [".css", ".js", ".png", ".jpg", ".gif"]
    if not (split_tup[1] in extensions):
        return 'true'


def get_the_url_text(URL):
    global count
    if is_url_valid(URL) == 'true':
        try:
            count += 1
            print('[%d] Processing %s' % (count, URL))
            text = requests.get(URL).text
            get_emails(text)
            return text
        except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            return ''


def find_uls(text):
    global base_url, protocol, allUrls, regEx_url
    urls = re.findall(regEx_url, text)
    url_array = []
    for Url_path in urls:
        full_url = protocol + '://' + base_url + Url_path[1]
        if not (full_url in allUrls):
            allUrls.append(full_url)
            url_array.append(full_url)
    return url_array


def get_emails(text):
    global allEmails, regEx_email
    emails = re.findall(regEx_email, text)
    emails = list(dict.fromkeys(emails))
    allEmails = list(dict.fromkeys(emails + allEmails))


def urlLoop(text):
    urls = list(dict.fromkeys(find_uls(text)))
    if len(urls) > 0:
        for Url in urls:
            new_string = get_the_url_text(Url)
            if new_string:
                urlLoop(new_string)


string = get_the_url_text(url)
urlLoop(string)
print(allEmails)
