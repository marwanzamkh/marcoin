import base64
import io
import pandas as pd
import streamlit as st
import altair as alt
from bs4 import BeautifulSoup
import requests,lxml


import re as re
st.title("                   Optimizer ")
st.write("""###             For Google Shopping""")
st.write("""###             Developed by Marwan Zamkah""")
st.write("""###             """)
st.write("""###             """)
st.write("1- Video Tutorial for Optimizer of google shopping ")
st.video('http://www.youtube.com/watch?v=ubpMP0Ab5Ys')

user_word = st.sidebar.text_input("Enter a keyword")
submit = st.sidebar.button('Search Google Shopping .... 🔎')






headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

cn="SA"
params = {"q": user_word, "hl": "en", 'gl': 'sa', 'tbm': 'shop'}
#"Sebium gel moussant oily acne skin cleaning - Bioderma"

response = requests.get("https://www.google.com/search",params=params,headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
#soup = BeautifulSoup(response.text, 'html.parser')
shopping_data = []
my_dict={
             'title': [],
            'link': [],
            'source': [],
            'price': [],
            'rating': [],
            'reviews': [],
            'delivery': []
}


def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = link.split('=')[1]
    return f'<a target="_blank" href="{link}">{text}</a>'
def find_number(text):
     num = re.findall(r'[0.00-9.00]+',text)
     return " ".join(num)


for shopping_result in soup.select('.sh-dgr__content'):
    title = shopping_result.select_one('.Lq5OHe.eaGTj h4').text
    product_link = f"https://www.google.com{shopping_result.select_one('.Lq5OHe.eaGTj')['href']}"
    source = shopping_result.select_one('.IuHnof').text
    price = shopping_result.select_one('span.kHxwFf span').text

    try:
      rating =shopping_result.select_one('.Rsc7Yb').text
    except:
      rating = None

    try:
       reviews = shopping_result.select_one('.Rsc7Yb').next_sibling.next_sibling
    except:
      reviews = None

    try:
        delivery = shopping_result.select_one('.vEjMR').text
    except:
       delivery = None
       my_dict['title'].append(title)
       my_dict['link'].append(product_link)
       my_dict['source'].append(source)
       my_dict['price'].append(price)
       my_dict['rating'].append(rating)
       my_dict['reviews'].append(reviews)
       my_dict['delivery'].append(delivery)

df = pd.DataFrame.from_dict(my_dict)

try:

   df['link'] = df['link'].apply(make_clickable)
   df = df.to_html(escape=False)
   st.header("Search Results for Price Compression From Google Shopping  ")
   st.write(df, unsafe_allow_html=True)
   df1=pd.DataFrame.from_dict(my_dict)
   df1.replace(',','', regex=True, inplace=True)
   df1['pricenumber']=df1['price'].apply(lambda x: find_number(x))


   df1['product_cost']=df1['pricenumber'].str.split().str[0]

   df1['delivery'] = df1['delivery'].replace(['Free delivery','','+Delivery'], '0.0a')
   df1['delivery'] = df1['delivery'].fillna('0.0a')
   df1['reviews'] = df1['reviews'].fillna(0)
   df1['rating'] = df1['rating'].fillna(0)
   df1['deliver_cost']=df1['delivery'].apply(lambda x: find_number(x))
   df1["product_cost"] = pd.to_numeric(df1["product_cost"], downcast="float")
   df1['product_cost'] = df1['product_cost'].fillna(0)
   df1["deliver_cost"] = pd.to_numeric(df1["deliver_cost"], downcast="float")
   df1["rating"] = pd.to_numeric(df1["rating"], downcast="float")
   df1['Total_Cost']=df1['deliver_cost']+df1['product_cost']
   df4=df1.drop(['price', 'rating','delivery','pricenumber','reviews','rating'], axis = 1)
   df4.sort_values(by=['Total_Cost'], inplace=True)
   df4['link'] = df4['link'].apply(make_clickable)
   df4 = df4.to_html(escape=False)
  

   st.header("Sort Product by Price including Delivery Cost ")
   st.write(df4, unsafe_allow_html=True)

   st.header("Visualize the data with source vs. total_cost")
   chart=alt.Chart(df1).mark_bar().encode(
                      x = "source:O",
                      y = "Total_Cost:Q"
                      ).properties(
                      width=600,
                      height=500
                      )
   st.altair_chart(chart, use_container_width=True)

   a=df1['Total_Cost'].min()
   st.header("The best price of  product report")
   st.write("Minimum  price  is :", a)
   for tr in df1['Total_Cost']:

       if tr==a:
          ae=df1.loc[df1['Total_Cost']==tr]

          n=ae['reviews'].iloc[0]
          k=ae['rating'].iloc[0]
          g=ae['source'].iloc[0]
          li=ae['link'].iloc[0]
          st.write("The source of best price products is:",g)
          st.write("The rating ***** is :",k)
          st.write("The reviews ***** is :", n)
          st.write ('The link of product please click')
          link1 = li
          st.markdown(link1, unsafe_allow_html=True)
except:
    st.write('No search exist for following keyword')




