import streamlit as st
import pandas as pd
import numpy as np

st.title('MMP Screening App Prototype')

sheet_url = st.secrets["sheet_url"]
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

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

mentor_name = st.text_input('Please input your "mentor ID" from the email', 'C10 謝明修') #TODO: modify the default value
data_load_state = st.text('Loading data...')
data = load_data(mentor_name) # example mentor: "C10 謝明修", "B39 張櫂杬"
data_load_state.text("Mentee data retrieved!")
st.text(f'You got these candidate mentees: {data["中文姓名"].values}')

"You can click the checkbox below to see all the raw data of the candidate mentees."
if st.checkbox('Show raw data of candidate mentees'):
    st.subheader('Raw data')
    st.write(data)
    csv = convert_df(data)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f'{mentor_name}_candidate_mentee.csv',
        mime='text/csv',
    )

st.subheader('Understand your mentees better!')

st.radio(
    "Choose your mentee data display mode",
    ["Single Mentee Info", "Multiple Mentee Info"],
    key="viewing_mode",
    horizontal=True,
)

display_columns = [
    "電子郵件地址",
    "中文姓名",
    "其餘聯絡方式 (非必填)",
    "最高學歷",
    "學士就讀/畢業學校",
    "學士就讀/畢業系所",
    "碩士就讀/畢業學校",
    "碩士就讀/畢業系所",
    "申請年份",
    "廣義研究領域",
    "專業領域",
    "主要申請系所所在國家",
    "欲申請學位",
    "欲申請系所/program",
    "欲申請學校",
    "欲尋求之協助/建議(至多三個)",
    "請問您目前準備進度為何？是否已經完成選校？",
    "提供簡歷與相關資料",
    "是否已經參加留學國的語文程度測驗？",
    "目前申請文件的準備進度？",
    "相關的選擇學校、系所的理由",
    "任何公開資訊 （選填）",
    "任何想對未來導師說的話",
    "是否為家族中第一代高等教育子女（選填）",
    "國際活動經驗（選填）",
    "學術領域外相關特殊專長、經驗或成就（選填）",
    "家人、伴侶等狀態（選填）",
    "目前的生涯規劃，或主要申請目的與動機（選填）",
    "您認為可能會影響申請過程或結果的身份、背景、經歷，而您希望導師知道的（選填）",
    "任何想補充給導師知道的（選填）",
    "目前是否已開始聯繫請求推薦信。",
    "是否已經參加標準化入學考試？",
]

if st.session_state.viewing_mode == "Single Mentee Info":
    st.subheader("Single Mentee Info")
    mentee_name = st.selectbox(
        'You can select one mentee to see his/her profile.',
        data["中文姓名"].values)

    st.dataframe(
        data.loc[
            data["中文姓名"] == mentee_name,display_columns
                ].set_index("中文姓名").transpose(),
        use_container_width=True
        )
elif st.session_state.viewing_mode == "Multiple Mentee Info":
    st.subheader("Multiple Mentee Info")
    options = st.multiselect(
        'You can select up to 3 mentees to see compare their profiles.',
        data["中文姓名"].values,
        max_selections=3)

    st.dataframe(
        data.loc[
            data["中文姓名"].isin(options),display_columns].set_index("中文姓名").transpose(),
        use_container_width=True
        )

st.subheader("Please use the following Google form to let us know your decision on the mentees you want to mentor.")

"google form link (WIP)" #TODO: add the link to the google form