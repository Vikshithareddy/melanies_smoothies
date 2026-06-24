# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw: {st.__version__}")
st.write(
  """Choose the fruits you what in your custom smoothie!"""
)
#option = st.selectbox("How would like you to be connected?",          ('Email', 'Home Phone', 'Mobile Phone'))
#st.write('You Selected:', option)
#option1 = st.selectbox("What is your favorite fruit?",            ('Banana', 'Strawberries', 'Apples'))
#st.write('You Selected:', option1)

name_on_order = st.text_input('Name on Smoothie:')

cnx = st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("Fruit_Name"))
Ingredients_list = st.multiselect('Choose up to 5 Ingredients', my_dataframe, max_selections=5)

#st.dataframe(data=my_dataframe, use_container_width=True)
if Ingredients_list:
    st.write(Ingredients_list)
    st.text(Ingredients_list)
    ingredients_string = ''
    for fruits in Ingredients_list:
        ingredients_string += fruits
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
                    values ('""" + ingredients_string + """', '""" + name_on_order+ """')"""

    #my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
     #               values ('""" + ingredients_string + """')"""
    #st.write(my_insert_stmt)
    time_to_start = st.button('Submit Order')
    if time_to_start:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

import requests  
smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
st.text(smoothiefroot_response.json())


