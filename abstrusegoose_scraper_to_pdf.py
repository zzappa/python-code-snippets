"""Script that fetches all AbstruseGoose comicses and creates a pdf."""

import html
import logging
import re
from io import BytesIO

from lxml import html as lxml_html
import requests
from PIL import Image
from bs4 import BeautifulSoup
from fpdf import FPDF

link = 'https://abstrusegoose.com/'


def add_image(img, text, size):
    pdf.add_page(format=size)
    pdf.image(img)
    pdf.ln(5)
    text = text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(ln=1, w=0, h=26, align='L', txt=text)


def fetch_image(link):
    try:
        img = requests.get(link)
        logging.warning(img.url)
        i = Image.open(BytesIO(img.content))
    except Exception:
        i = None
    return i


def get_comic(link):
    r = requests.get(link)

    try:
        urls_strips = re.findall('https?://abstrusegoose.com/strips/.*png', r.text)
        url = urls_strips[0]
        i = fetch_image(url)
    except Exception:
        i = None
    src = r.url
    try:
        soup = BeautifulSoup(r.text, 'html5lib')
        txt = soup.find("div", {"id": "blog_text"})
        txt = html.unescape(str(txt).lstrip('<div id="blog_text"><p>\n<p>').rstrip('</p></div></p>\n'))
        txt = str(lxml_html.fromstring(txt).text_content())
        for item in ('r/>', 'align="center">', 'a href="', '" target="_blank"', 're>', 'm>', 'strong>', '/p>'):
            txt = txt.replace(item, ' ')
        txt = txt.replace('r/>', '') + "\n" + src
    except Exception:
        txt = src
    try:
        title = soup.find("h1", {"class": "storytitle"})
        title = title.text
    except Exception:
        title = ''
    text = title + '\n' + txt
    return i, text


pdf = FPDF(unit = 'pt')
pdf.set_font("Times", size=20)
img1 = fetch_image('https://abstrusegoose.com/strips/conv_sub_panel_small.png')
add_image(img1, 'Convergent Subsequence' + '\n' + link + '1', size=(img1.width + 50, img1.height + 200))
for i in range(2, 615):
    url = link + str(i)
    img, txt = get_comic(url)
    if img:
        add_image(img, txt, size=(img.width + 50, img.height + 550))
pdf.output("abstrusegoose.pdf")
