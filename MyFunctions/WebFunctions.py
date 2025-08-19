# WebFunctions:
"""
Funções relacionadas a capacidade que o modelo tem de interagir 
com a internet. LLMs são modelos de linguagem, eles não leem
links nem entram em páginas. Então, a ideia aqui é capacitar o modelo
a lidar com links e páginas.
"""

# Dependencias:
import requests
import re
import unicodedata
from html_to_markdown import convert_to_markdown
import html2text
from selenium import webdriver


def search_content_in_complex_site_logic(url:str) -> str:
    """
    Função que extrair o texto de um site usando cloudflare.
    Usar o selenium resolve o problema da necessidade de um
    navegador que rode javascript.
    """

    # Aquisitando HTML
    driver = webdriver.Chrome()
    driver.get(url)
    html = driver.page_source
    driver.quit()

    # Transformando em markdown
    markdown = html2text.html2text(html)
    return markdown



def search_site_content_logic(url: str) -> str:
    """
    Tool purpose:
    -------------
    This function serves as an agent tool within an LLM pipeline.
    Its role is:
      - Accept a URL provided by a user prompt,
      - Fetch the page via the `requests` library,
      - Decode the content appropriately,
      - Convert HTML to Markdown,
      - Clean up encoding artifacts using regex,
      - Return a clean Markdown string for agent consumption.
    """

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5"
    }

    resp = requests.get(url, headers=headers, timeout=20.0)
    resp.raise_for_status()  # Raise HTTPError on bad 4xx/5xx responses

    # Step 1: Determine encoding
    # requests uses Content-Type charset if present; otherwise
    # it may guess using chardet or charset_normalizer via resp.apparent_encoding
    encoding = resp.encoding or resp.apparent_encoding
    resp.encoding = encoding  # override to ensure correct decoding
    html = resp.text

    # Step 2: Convert HTML to Markdown using your converter
    md = convert_to_markdown(html)

    # Step 3: Normalize Unicode (e.g. combine accents properly)
    md = unicodedata.normalize('NFC', md)

    # Step 4: Cleanup control characters and placeholders
    md = md.replace('\r', ' ').replace('\xa0', ' ')
    md = re.sub(r'�+', ' ', md)               # remove garbled replacement characters
    md = re.sub(r'<!--.*?-->', '', md, flags=re.DOTALL)  # strip HTML comments
    md = re.sub(r'\n{3,}', '\n\n', md)        # collapse multiple blank lines
    md = re.sub(r'[ \t]{2,}', ' ', md)        # collapse multiple spaces/tabs

    return md