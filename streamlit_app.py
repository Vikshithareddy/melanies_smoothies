# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests 
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
my_dataframe = session.table("smoothies.public.fruit_options").select(col("Fruit_Name"), col('SEARCH_ON'))
#st.dataframe(data = my_dataframe, use_container_width=True)
#st.stop()
pd_df = my_dataframe.to_pandas()
Ingredients_list = st.multiselect('Choose up to 5 Ingredients', my_dataframe, max_selections=5)

#st.dataframe(data=my_dataframe, use_container_width=True)
if Ingredients_list:
    st.write(Ingredients_list)
    st.text(Ingredients_list)
    ingredients_string = ''
    for fruits in Ingredients_list:
        ingredients_string += fruits +' '
        search_on  = pd_df.loc[pd_df['FRUIT_NAME'] == fruits, 'SEARCH_ON'].iloc[0]
        st.subheader(fruits +'Nutrition Infromation')
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")  
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)
    

