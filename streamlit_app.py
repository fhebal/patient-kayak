import streamlit as st
import uuid
import plotly.graph_objects as go
import pandas as pd
from load_css import local_css
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


local_css("style.css") 


with open('logo90.txt', 'r') as f:
    logo_base64 = f.read()


#st.set_page_config(layout="wide")
INPUT_PATH = '/home/muody/data/patient_kayak/'
df = pd.read_csv(INPUT_PATH + "lookup_table.csv")


# temporary
from PIL import Image
def logo():
    st.markdown("<div><span class='adjust'>"
        + '<img src="data:image/png;base64, {}", alt="Red dot" /'.format(logo_base64)
        + "</span><div>",
        unsafe_allow_html=True)


def header():
    cols = st.beta_columns(1)
    st.title("Find the best quality service from hundreds of providers.")


def search_bar(df):
    options = list(df['Charge Code Description'].dropna().unique())
    #options = [str(x) for x in options]
    options.sort()
    options += ['Enter a service...']
    selection = st.selectbox('',options=options, index=len(options)-1)
    df['similarity'] = df['Charge Code Description'].apply(lambda x: similar(str(x), selection))
    df = df[df['similarity'] > .5]
    return df.drop(columns=['similarity'])


def price_map():
    """
    For now this is a temporary png from Kayak as a placeholder
    """

    image = Image.open(INPUT_PATH + 'kayak_map_demo.png')
    st.image(image)

def results_table():
    INPUT_PATH = '/home/muody/data/patient_kayak/'
    df = pd.read_csv(INPUT_PATH + "lookup_table.csv")

    fig = go.Figure(data=[go.Table(
	columnwidth = [1,2,1,1],
	header=dict(values=list(df.columns),
		    #fill_color='paleturquoise',
		    align='left'),
	cells=dict(values=[df[x] for x in df.columns],
		   #fill_color='lavender',
		   align='left'))
    ])
    st.write(fig)


def results_table(df):
    st.title("Let's create a table!")
    cols = st.beta_columns(4)
    for i in range(4):
        cols[i].write("### " + str(df.columns[i]))

    cols = st.beta_columns(1)

    cols = st.beta_columns(4)
    for i in range(1, 10):
        row = df.iloc[i]
        for i in range(len(df.columns)):

            cols[i].button(str(row[i]), key=uuid.uuid1())
        cols = st.beta_columns(1)
        cols = st.beta_columns(4)
        #cols[1].button(f'{i * i}', key=uuid.uuid1())
        #cols[2].button(f'{i * i * i}')
        #cols[3].button(str('x' * i))


def results_table(df):
    st.table(df)


def main(df):
    logo()
    header()
    df = search_bar(df)
    price_map()
    results_table(df)

if __name__ == "__main__":
    main(df)

