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
        'About': """Find more about TYRA
https://linktr.ee/projecttyra

If you find this project useful, please consider giving us a star on GitHub:
https://github.com/ChenHsieh/MMP_screening

"""
    }
)
st.title('project Tyra - Mentor Dashboard')

mentee_response_sheet_url = st.secrets["sheet_url"]
mentors_sheet_url = st.secrets["mentors_sheet_url"]


mentee_response_csv_export_url = mentee_response_sheet_url.replace(
    '/edit#gid=', '/export?format=csv&gid=')


mentors_csv_export_url = mentors_sheet_url.replace(
    '/edit#gid=', '/export?format=csv&gid=')
mentors_table = pd.read_csv(mentors_csv_export_url)
# mentors_table = pd.read_csv("mentors_processed.csv")
mentors_table.set_index("verification_code", inplace=True)


@st.cache_data
def load_mentee_data(mentor_name):
    data = pd.read_csv(mentee_response_csv_export_url)
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

mentor_verification_code = st.text_input(
    'Please input your "verification code" from the email', '')

if (mentor_verification_code == ""):
    st.warning(
        f"The input is empty!")
    st.stop()
elif ((mentor_verification_code in mentors_table["name"].values) | (mentor_verification_code in mentors_table["mentor_id"].values) |
      (mentor_verification_code in mentors_table["combined_mentor_id"].values) | (mentor_verification_code in mentors_table["email"].values)):
    st.warning(
        f"Please input the verification code instead of personal information. Please check your verification code from the email we sent to you.")
    st.stop()
elif (mentor_verification_code in mentors_table.index):
    st.success(
        f"Hola {mentors_table.loc[mentor_verification_code]['name']}! Welcome to the mentor dashboard!")
    f"From your record, we know that you plan to accept {mentors_table.loc[mentor_verification_code]['capacity_PhD']} mentees for PhD program and {mentors_table.loc[mentor_verification_code]['capacity_MSc']} mentees for master program. You chose to {(lambda: '' if mentors_table.loc[mentor_verification_code]['review_info'] else 'not ')()} review the mentee response before making your desicion."
    f"For now, there are {mentors_table.loc[mentor_verification_code]['assigned_PhD']} mentees for PhD program and {mentors_table.loc[mentor_verification_code]['assigned_MSc']} mentees for master program interested in meeting you."
    f"Please check the following mentee information and let us know your decision."
else:
    st.warning(
        f"Oops! We cannot find any results for the current input. Please check your verification code from the email.")
    st.stop()

mentor_name = mentors_table.loc[mentor_verification_code, "combined_mentor_id"]
mentee_response = load_mentee_data(mentor_name)
candidate_mentee_number = mentee_response.shape[0]
if candidate_mentee_number == 0:
    st.warning(
        f"Oops! We cannot find any results for the current input. Please check your verification code.")
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
st.divider()
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
    current_mentee = mentee_response.loc[mentee_response["中文姓名"]
                                         == mentee_name]

    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            f"選擇您為第 {current_mentee['志願序'].values[0]} 志願", current_mentee["中文姓名"].values[0])
        st.write(
            f"申請 {current_mentee['申請年份'].values[0]} {current_mentee['欲申請學位'].values[0]}")
        st.subheader("學歷資料")
        for degree in ["學士", "碩士"]:
            if (pd.isna(current_mentee[f'{degree}就讀/畢業學校'].values[0])):
                continue
            st.write(
                f"{current_mentee[f'{degree}就讀/畢業學校'].values[0]} {current_mentee[f'{degree}就讀/畢業系所'].values[0]} {degree}")

        st.subheader("申請目標")
        goal_columns = [
            "主要申請系所所在國家",
            "欲申請學校",
            "欲申請系所/program",
            "相關的選擇學校、系所的理由",
        ]
        for column in goal_columns:
            if (pd.isna(current_mentee[column]).any()):
                continue
            st.caption(column)
            st.write(current_mentee[column].values[0])

        st.subheader("任何想對未來導師說的話")
        current_mentee["任何想對未來導師說的話"].values[0]

    with col2:
        st.subheader("基本資料")
        st.caption(f"廣義研究領域")
        current_mentee['廣義研究領域'].values[0]
        st.caption(f"專業領域")
        current_mentee['專業領域'].values[0]

        st.subheader("目前申請準備進度")
        progress_columns = ["欲尋求之協助/建議(至多三個)",
                            "請問您目前準備進度為何？是否已經完成選校？",
                            "提供簡歷與相關資料",
                            "是否已經參加留學國的語文程度測驗？",
                            "目前申請文件的準備進度？",
                            "目前是否已開始聯繫請求推薦信。",
                            "是否已經參加標準化入學考試？", ]
        for column in progress_columns:
            if (pd.isna(current_mentee[column]).any()):
                continue
            st.caption(column)
            st.write(current_mentee[column].values[0])

    st.subheader("選填背景資訊")
    background_columns = [
        "是否為家族中第一代高等教育子女（選填）",
        "國際活動經驗（選填）",
        "學術領域外相關特殊專長、經驗或成就（選填）",
        "家人、伴侶等狀態（選填）",
        "目前的生涯規劃，或主要申請目的與動機（選填）",
        "您認為可能會影響申請過程或結果的身份、背景、經歷，而您希望導師知道的（選填）",
        "任何想補充給導師知道的（選填）",
        "任何公開資訊 （選填）", ]
    for column in background_columns:
        if (pd.isna(current_mentee[column]).any()):
            continue
        st.caption(column)
        st.write(current_mentee[column].values[0])

    st.subheader("聯絡方式")
    contact_columns = [
        "電子郵件地址",
        "其餘聯絡方式 (非必填)",
    ]
    for column in contact_columns:
        if (pd.isna(current_mentee[column]).any()):
            continue
        st.caption(column)
        st.write(current_mentee[column].values[0])

elif viewing_mode == "Multiple Mentee Info":
    st.subheader("Multiple Mentee Info")
    options = st.multiselect(
        'You can select up to 3 mentees to see compare their profiles.',
        mentee_response["中文姓名"].values,
        max_selections=3)

    st.dataframe(
        mentee_response.loc[
            mentee_response["中文姓名"].isin(options), display_columns].set_index("中文姓名").transpose(),
        height=696,
        use_container_width=True
    )
st.divider()
st.markdown("[go back to top](#know-your-mentee-better)")
st.header("Finalize your decision")

f"""Please use the following Google form to let us know your decision on the mentees you want to mentor. We will let you know the final result after the matching process is done. 

If the following part is not shown, please use this link: https://forms.gle/KbvU9C6TPZZ3h3wV6"""
components.iframe("https://forms.gle/KbvU9C6TPZZ3h3wV6",
                  width=None, height=1069, scrolling=True)
