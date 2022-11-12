"""
Comment
"""

import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

def get_fv_data(fv_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fv_choice)
  #streamlit.text(fruityvice_response.json()) #Just displays data in JSON 
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json()) # Takes JSON output and normaizes the same 
  return(fruityvice_normalized)

def get_sf_FRUIT_LOAD_LIST():
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_cur = my_cnx.cursor()
  #my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
  #my_data_row = my_cur.fetchone()
  my_cur.execute("SELECT * FROM PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
  return(my_cur.fetchall())  


streamlit.title("My Mom's New Healthy Diner")
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries']) 
# Display the table on the page
#streamlit.dataframe(my_fruit_list) 

fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)


streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get the information")
  else:
    fv_res = get_fv_data(fruit_choice)
    #streamlit.write('The user entered ', fruit_choice)    
    streamlit.dataframe(fv_res) # displays the data in tabular format
except URLError as e:
  streamlit.error()
  


streamlit.header("The fruit load list contains :")
if streamlit.button('Get Fruit Load List'):
  fv_list = get_sf_FRUIT_LOAD_LIST()
  streamlit.dataframe(fv_list)

streamlit.stop()
add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thaks for adding ', add_my_fruit)
my_cur.execute("INSERT INTO PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST VALUES ('From STREAM LIT')")
