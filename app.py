import streamlit as st
import pandas as pd
import numpy as np

st.title('testing the idea')

sheet_url = "https://docs.google.com/spreadsheets/d/1vAKMOOkGNaBTQQGyQreIDag767hX94ddxuTae7A6djE/edit#gid=1994387913"
csv_export_url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')

@st.cache_data
def load_data(mentor_name):
    data = pd.read_csv(csv_export_url)
    # lowercase = lambda x: str(x).lower()
    # data.rename(lowercase, axis='columns', inplace=True)
    # data["時間戳記"] = pd.to_datetime(data["時間戳記"])
    data = data.loc[
        (data["希望配對的導師（第一志願）"] == mentor_name) |
        (data["希望配對的導師（第二志願）.1"] == mentor_name) |
        (data["希望配對的導師（第三志願）.1"] == mentor_name) |
        (data["希望配對的導師（第四志願）.1"] == mentor_name) |
        (data["希望配對的導師（第五志願）.1"] == mentor_name) 
        #TODO: reduce the columns to be shown
    ]
    return data

mentor_name = st.text_input('Please input your "mentor ID" from the email', 'C10 謝明修') #TODO: modify the default value
data_load_state = st.text('Loading data...')
data = load_data(mentor_name) # example mentor: "C10 謝明修", "B39 張櫂杬"
data_load_state.text("Mentee data retrieved!")
st.text(f'You got these candidate mentees: {data["中文姓名"].values}')

"You can click the checkbox below to see the raw data of the candidate mentees."
if st.checkbox('Show raw data of candidate mentees'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Understand your mentees better!')
options = st.multiselect(
    'What are your favorite colors',
    data["中文姓名"].values,
    max_selections=3)

st.dataframe(
    data.loc[
        data["中文姓名"].isin(options),
            ["中文姓名",
            "最高學歷",
     "學士就讀/畢業學校"]].set_index("中文姓名").transpose(),
     use_container_width=True
     )

st.subheader("Please use the following Google form to let us know your decision on the mentees you want to mentor.")

"google form link (WIP)" #TODO: add the link to the google form