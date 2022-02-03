import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
from time import strftime

def get_front_page_links():
    """
    Function to acquire blog posts from the Codeup blog and return a list of urls.
    """
    response = requests.get('https://codeup.com/blog/', headers = {'user-agent': 'Codeup DS Hopper'})
    soup = BeautifulSoup(response.text)
    links = [link.attrs['href'] for link in soup.select('.more-link')]

    return links

def parse_codeup_blog_article(url):
    """
    Function to scrap information from a url and return a dictionary.
    """
    response = requests.get(url, headers = {'user-agent': 'Codeup DS Hopper'})
    soup = BeautifulSoup(response.text)
    return {
        'title': soup.select_one('.entry-title').text,
        'published': soup.select_one('.published').text,
        'content': soup.select_one('.entry-content').text.strip(),
            }

def get_blog_articles():
    """
    Function to return dataframe where each row represents a blog post.
    """
    links = get_front_page_links()
    df = pd.DataFrame([parse_codeup_blog_article(link) for link in links])
    
    return df

def parse_news_card(card):
    """
    Function that takes a news card object and returns a dictionary containing the article's
    title, author, content and date.
    """
    card_title = card.select_one('.news-card-title')
    output = {}
    output['title'] = card.find('span', itemprop = 'headline').text
    output['author'] = card.find('span', class_ = 'author').text
    output['content'] = card.find('div', itemprop = 'articleBody').text
    output['date'] = card.find('span', clas ='date').text
    
    return output

def parse_inshorts_page(url):
    """
    Function that takes in a url and returns a df in which each row is an article from the
    url.
    """
    category = url.split('/')[-1]
    response = requests.get(url, headers = {'user-agent': 'Codeup DS'})
    soup = BeautifulSoup(response.text)
    cards = soup.select('.news-card')
    df = pd.DataFrame([parse_news_card(card) for card in cards])
    df['category'] = category
    
    return df

def get_inshorts_articles():
    """
    This function returns a df of a news article from teh business, sports, technology and 
    entertainment section from the inshorts site.
    """
    url = 'https://inshorts.com/en/read/'
    categories = ['business', 'sports', 'technology', 'entertainment']
    df = pd.DataFrame()
    for cat in categories:
        df = pd.concat([df, pd.DataFrame(parse_inshorts_page(url + cat))])
    df = df.reset_index(drop = True)
    
    return df