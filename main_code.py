import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import openpyxl


def get_title(soup):

    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id":'productTitle'})
        
        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

# Function to extract Product Price
def get_price(soup):

    try:
        price = soup.find("span", attrs={'class':'a-price-whole'}).string.strip()

    except AttributeError:

        try:
            # If there is some deal price
            price = soup.find("span", attrs={'class':'a-offscreen'}).string.strip()

        except:
            price = ""

    return price

# Function to extract Product Rating
def get_rating(soup):

    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
    
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""	

    return rating


def get_description(soup):

    try:
        # Outer Tag Object
        title = soup.find("div", attrs={"id":'productDescription'})
        
        # Inner NavigatableString Object
        title_value = title.text


        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        try:
            title = soup.find("div", attrs={"id":'feature-bullets'})
            
            # Inner NavigatableString Object
            title_value = title.text

            # Title as a string value
            title_string = title_value.strip()
        except:
            title_string = ""

    return title_string


def get_asin(soup):

    try:
        # Outer Tag Object
        title = soup.find("div", attrs={"id":'detailBullets_feature_div'})
        # Inner NavigatableString Object
        Ntitle =title.find_all('li')[3]
        # entering inside li tag and fatching 2nd span tag data
        Ftitle=Ntitle.find_all('span')[2]
        # print(Ftitle)
        title_value = Ftitle.text
        # Title as a string value
        title_string = title_value.strip()
        # print(title_string)
        
        if title == None:
          table = soup.find("table", attrs={"id":'productDetails_detailBullets_sections1'}) # Table id
          # Inner NavigatableString Object
          Ntitle =table.find_all('tr')[3]
          # entering inside tr tag and fatching 3nd td tag data
          Ftitle=Ntitle.find_all('td')[3]
          print(Ftitle)
          title_value = Ftitle.text
          # Title as a string value
          title_string = title_value.strip()
          # print(title_string)
          
    except:
        title_string = ""

    return title_string


def get_manufacturer(soup):
# td class="a-size-base prodDetAttrValue"
    try:
        # Outer Tag Object
        title = soup.find("div", attrs={"id":'detailBullets_feature_div'})
        # Inner NavigatableString Object
        Ntitle =title.find_all('li')[2]
        # entering inside li tag and fatching 2nd span tag data
        Ftitle=Ntitle.find_all('span')[2]
        title_value = Ftitle.text
        # Title as a string value
        title_string = title_value.strip()
        
        if title == None:
          
          table = soup.find("table", attrs={"id":'productDetails_detailBullets_sections1'}) # Table id
          # Inner NavigatableString Object
          Ntitle =table.find_all('tr')[2]
          # entering inside tr tag and fatching 2nd td tag data
          Ftitle=Ntitle.find_all('td')[2]
          
          title_value = Ftitle.text
          

          # Title as a string value
          title_string = title_value.strip()
          
          

    except:
        title_string = ""

    return title_string


# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""	

    return review_count



if __name__ == '__main__':

    # add your user agent 
    HEADERS = ({'User-Agent':'', 'Accept-Language': 'en-US, en;q=0.5'})

    # The webpage URL
    # URL = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

    # Store the links
    links_list = []

    # Creating 12 pages for getting 200+ products
    for pg in range(1, 13):
      new_url = f"https://www.amazon.in/s?k=bags&page={pg}&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{pg}"

      # HTTP Request
      webpage = requests.get(new_url, headers=HEADERS)

      # Soup Object containing all data
      soup = BeautifulSoup(webpage.content, "html.parser")

      # Fetch links as List of Tag Objects
      links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

      # Loop for extracting links from Tag Objects
      for link in links:
        links_list.append(link.get('href'))    
    
    d = {"Product URL":[],"Product Name":[], "Product Price":[], "Rating":[] , "Number of reviews":[], "Manufacturer":[],"Product Description":[],"ASIN":[]}
    
    # Loop for extracting product details from each link 

    for link in links_list:
        new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")
        d['Product URL'].append("https://www.amazon.in"+ link)
        d['Product Name'].append(get_title(new_soup))
        d['Product Price'].append(get_price(new_soup))
        d['Rating'].append(get_rating(new_soup))
        d['Number of reviews'].append(get_review_count(new_soup))
        
        d['ASIN'].append(get_asin(new_soup))
        d['Product Description'].append(get_description(new_soup))
        d['Manufacturer'].append(get_manufacturer(new_soup))

    
    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['Product Name'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['Product Name'])
    amazon_df.to_csv("amazon_data.csv", header=True, index=False)

print(amazon_df)