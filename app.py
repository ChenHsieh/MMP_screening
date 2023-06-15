import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components

st.set_page_config(
    page_title="MMP Screening App",
    page_icon="⛵️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': """
# Find more about TYRA
https://linktr.ee/projecttyra
"""
    }
)
st.title('MMP Screening App')
st.sidebar.markdown('''
# Sections
- [Know your mentee better](#know-your-mentee-better)
- [Finalize your decision](#finalize-your-decision)
''', unsafe_allow_html=True)

sheet_url = st.secrets["sheet_url"]
csv_export_url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')

mentors_sheet_url = st.secrets["mentors_sheet_url"]
mentors_csv_export_url = mentors_sheet_url.replace(
    '/edit#gid=', '/export?format=csv&gid=')
mentors = pd.read_csv(mentors_csv_export_url)


@st.cache_data
def load_mentee_data(mentor_name):
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
    ]
    return data


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


display_columns = [
    "中文姓名",
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
    "電子郵件地址",
    "其餘聯絡方式 (非必填)",
    "志願序",
]

# TODO: modify the default value and change to the verification code system
mentor_name = st.text_input(
    'Please input your "verification code" from the email', 'C10 謝明修')
# example mentor: "C10 謝明修", "B39 張櫂杬"
mentee_response = load_mentee_data(mentor_name)
# data_load_state.text("Mentee's response retrieved!")
candidate_mentee_number = mentee_response.shape[0]
if candidate_mentee_number == 0:
    st.warning(
        f"Oops! No mentee is interested in you! Please check your name again.")
    st.stop()
elif candidate_mentee_number == 1:

    st.success(
        f"Great! {mentee_response['中文姓名'].values[0]} is interested in you!")
else:

    st.success(
        f'You are popular! Here are the mentees who are interested in you: {"、".join(mentee_response["中文姓名"].values)}')

# extract the ranking of the mentor from the mentee response
mentee_response.loc[mentee_response["希望配對的導師（第五志願）.1"]
                    == mentor_name, "志願序"] = "5"
mentee_response.loc[mentee_response["希望配對的導師（第四志願）.1"]
                    == mentor_name, "志願序"] = "4"
mentee_response.loc[mentee_response["希望配對的導師（第三志願）.1"]
                    == mentor_name, "志願序"] = "3"
mentee_response.loc[mentee_response["希望配對的導師（第二志願）.1"]
                    == mentor_name, "志願序"] = "2"
mentee_response.loc[mentee_response["希望配對的導師（第一志願）"]
                    == mentor_name, "志願序"] = "1"

# filter the columns to be shown
mentee_response = mentee_response[display_columns].sort_values(by="志願序")

if st.checkbox('Show and download raw mentee response'):
    st.write(mentee_response.set_index("中文姓名"))
    csv = convert_df(mentee_response.set_index("中文姓名"))
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f'{mentor_name}_candidate_mentee.csv',
        mime='text/csv',
    )

st.header('Know your mentee better!')

if candidate_mentee_number == 1:
    viewing_mode = "Single Mentee Info"
elif candidate_mentee_number > 1:
    viewing_mode = st.radio(
        "Choose your mentee data display mode",
        ["Single Mentee Info", "Multiple Mentee Info"],
        # key="viewing_mode",
        horizontal=True,
    )


if viewing_mode == "Single Mentee Info":
    if candidate_mentee_number == 1:
        mentee_name = mentee_response["中文姓名"].values[0]
    if candidate_mentee_number > 1:
        mentee_name = st.selectbox(
            'You can select one of the candidate mentees to see their profile.',
            mentee_response["中文姓名"].values)

    for column in display_columns:
        if (pd.isna(mentee_response.loc[mentee_response["中文姓名"]
                                        == mentee_name, column]).any()):
            continue
        st.subheader(column)
        st.write(mentee_response.loc[mentee_response["中文姓名"]
                                     == mentee_name, column].values[0])
elif viewing_mode == "Multiple Mentee Info":
    st.subheader("Multiple Mentee Info")
    options = st.multiselect(
        'You can select up to 3 mentees to see compare their profiles.',
        mentee_response["中文姓名"].values,
        max_selections=3)

    st.dataframe(
        mentee_response.loc[
            mentee_response["中文姓名"].isin(options), display_columns].set_index("中文姓名").transpose(),
        height=500,
        use_container_width=True
    )
st.divider()
st.markdown("[go back to top](#know-your-mentee-better)")
st.header("Finalize your decision")

f"""Please use the following Google form to let us know your decision on the mentees you want to mentor. We will let you know the final result after the matching process is done. 

If the following part is not shown, please use this link: https://forms.gle/KbvU9C6TPZZ3h3wV6"""
components.iframe("https://forms.gle/KbvU9C6TPZZ3h3wV6",
                  width=None, height=1069, scrolling=True)
