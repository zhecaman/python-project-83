import os
import validators.url
from dotenv import load_dotenv
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests

def get_from_env(key):
    dotenv = Path(__file__).parent.absolute() / '.env'
    load_dotenv(dotenv)
    return os.environ.get(key)


def is_valid_url(str_url):
    return validators.url(str_url) and len(str_url) <= 255

def to_normal(str_url):
    url = urlparse(str_url)
    return f'{url.scheme}://{url.netloc}'


def get_seo_data(soup):
    