import os
import validators.url
from dotenv import load_dotenv
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def get_from_env(key):
    dotenv = Path(__file__).parent.absolute() / ".env"
    load_dotenv(dotenv)
    return os.environ.get(key)


def is_valid_url(str_url):
    return validators.url(str_url) and len(str_url) <= 255


def to_normal(str_url):
    url = urlparse(str_url)
    return f"{url.scheme}://{url.netloc}"


def get_seo_data(response):
    soup = BeautifulSoup(response, "lxml")
    t = soup.find("title")
    title = t.text.strip() if t else None
    h = soup.find("h1")
    h1 = h.text.strip() if h else None
    desc = soup.find("meta", {"name": "description"})
    description = desc.get("content") if desc else None

    return h1, title, description
