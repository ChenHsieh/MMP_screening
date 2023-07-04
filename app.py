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
        "About": """Find more about TYRA
https://linktr.ee/projecttyra

If you find this project useful, please consider giving us a star on GitHub:
https://github.com/ChenHsieh/MMP_screening

"""
    },
)
st.title("project Tyra - Mentor Dashboard")

mentee_response_sheet_url = st.secrets["mentee_response_sheet_url"]
mentee_sheet_url = st.secrets["mentee_sheet_url"]
mentor_sheet_url = st.secrets["mentor_sheet_url"]

mentee_response_sheet_url = mentee_response_sheet_url.replace(
    "/edit#gid=", "/export?format=csv&gid="
)
mentee_sheet_url = mentee_sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")
mentor_sheet_url = mentor_sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")
mentee_table = pd.read_csv(mentee_sheet_url)
mentor_table = pd.read_csv(mentor_sheet_url)
# mentor_table = pd.read_csv("mentors_processed.csv")
mentor_table.set_index("verification_code2", inplace=True)


@st.cache_data
def load_mentee_data(mentee_name_list):
    data = pd.read_csv(mentee_response_sheet_url)
    data = data.loc[data["中文姓名"].isin(mentee_name_list)]
    return data


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


display_columns = [
    "志願序",
    "中文姓名",
    "申請年份",
    "欲申請學位",
    "最高學歷",
    "學士就讀/畢業學校",
    "學士就讀/畢業系所",
    "碩士就讀/畢業學校",
    "碩士就讀/畢業系所",
    "廣義研究領域",
    "專業領域",
    "主要申請系所所在國家",
    "欲申請學校",
    "欲申請系所/program",
    "相關的選擇學校、系所的理由",
    "欲尋求之協助/建議(至多三個)",
    "請問您目前準備進度為何？是否已經完成選校？",
    "提供簡歷與相關資料",
    "是否已經參加留學國的語文程度測驗？",
    "目前申請文件的準備進度？",
    "目前是否已開始聯繫請求推薦信。",
    "是否已經參加標準化入學考試？",
    "任何想對未來導師說的話",
    "任何公開資訊 （選填）",
    "是否為家族中第一代高等教育子女（選填）",
    "國際活動經驗（選填）",
    "學術領域外相關特殊專長、經驗或成就（選填）",
    "家人、伴侶等狀態（選填）",
    "目前的生涯規劃，或主要申請目的與動機（選填）",
    "您認為可能會影響申請過程或結果的身份、背景、經歷，而您希望導師知道的（選填）",
    "任何想補充給導師知道的（選填）",
    "電子郵件地址",
    "其餘聯絡方式 (非必填)",
]

mentor_verification_code = st.text_input(
    'Please input your latest "verification code" from the email. Please note that the "verification code" is case-sensitive.',
    "",
)

if mentor_verification_code == "":
    st.warning(f"The input is empty!")
    st.stop()
elif (
    (mentor_verification_code in mentor_table["name"].values)
    | (mentor_verification_code in mentor_table["mentor_id"].values)
    | (mentor_verification_code in mentor_table["combined_mentor_id"].values)
    | (mentor_verification_code in mentor_table["email"].values)
):
    st.warning(
        f"Please input the verification code instead of personal information. Please check your verification code from the email we sent to you."
    )
    st.stop()
elif mentor_verification_code in mentor_table.index:
    st.success(
        f"Hola {mentor_table.loc[mentor_verification_code]['name']}! Welcome to the mentor dashboard!"
    )
    mentor_table["mentee_MSc"].fillna("", inplace=True)
    mentor_table["mentee_PhD"].fillna("", inplace=True)
    # f"You have been matched with {len(mentor_table.loc[mentor_verification_code]['mentee_MSc'].split(' '))} mentees for master program."
    # f"You have been matched with {len(mentor_table.loc[mentor_verification_code]['mentee_PhD'].split(' '))} mentees for PhD program."

else:
    st.warning(
        f"Oops! We cannot find any results for the current input. Please check your verification code."
    )
    st.stop()

mentee_id_list = mentor_table.loc[mentor_verification_code]["mentee_MSc"].split(
    " "
) + mentor_table.loc[mentor_verification_code]["mentee_PhD"].split(" ")
if "" in mentee_id_list:
    mentee_id_list.remove("")

mentee_table.set_index("mentee_id", inplace=True)
mentee_name_list = mentee_table.loc[mentee_id_list, "name"]

mentor_name = mentor_table.loc[mentor_verification_code, "combined_mentor_id"]
mentee_response = load_mentee_data(mentee_name_list)
candidate_mentee_number = mentee_response.shape[0]
if candidate_mentee_number == 0:
    st.warning(
        f"Oops! We cannot find any results for the current input. Please check your verification code."
    )
    st.stop()
elif candidate_mentee_number == 1:
    st.success(f'Great! {"、".join(mentee_response["中文姓名"].values)} matched with you!')
else:
    st.success(f'Great! {"、".join(mentee_response["中文姓名"].values)} matched with you!')

# extract the ranking of the mentor from the mentee response
mentee_response.loc[mentee_response["希望配對的導師（第五志願）.1"] == mentor_name, "志願序"] = "5"
mentee_response.loc[mentee_response["希望配對的導師（第四志願）.1"] == mentor_name, "志願序"] = "4"
mentee_response.loc[mentee_response["希望配對的導師（第三志願）.1"] == mentor_name, "志願序"] = "3"
mentee_response.loc[mentee_response["希望配對的導師（第二志願）.1"] == mentor_name, "志願序"] = "2"
mentee_response.loc[mentee_response["希望配對的導師（第一志願）"] == mentor_name, "志願序"] = "1"

# filter the columns to be shown
mentee_response = mentee_response[display_columns].sort_values(by="志願序")

if st.checkbox("Show and download raw mentee response"):
    st.write(mentee_response.set_index("中文姓名"))
    csv = convert_df(mentee_response.set_index("中文姓名"))
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f"{mentor_name}_candidate_mentee.csv",
        mime="text/csv",
    )


st.divider()
st.header("Know your mentee better!")

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
            "You can select one of the candidate mentees to see their profile.",
            mentee_response["中文姓名"].values,
        )
    current_mentee = mentee_response.loc[mentee_response["中文姓名"] == mentee_name]

    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            f"選擇您為第 {current_mentee['志願序'].values[0]} 志願",
            current_mentee["中文姓名"].values[0],
        )
        st.write(
            f"申請 {current_mentee['申請年份'].values[0]} {current_mentee['欲申請學位'].values[0]}"
        )
        st.subheader("學歷資料")
        for degree in ["學士", "碩士"]:
            if pd.isna(current_mentee[f"{degree}就讀/畢業學校"].values[0]):
                continue
            st.write(
                f"{current_mentee[f'{degree}就讀/畢業學校'].values[0]} {current_mentee[f'{degree}就讀/畢業系所'].values[0]} {degree}"
            )

        st.subheader("申請目標")
        goal_columns = [
            "主要申請系所所在國家",
            "欲申請學校",
            "欲申請系所/program",
            "相關的選擇學校、系所的理由",
        ]
        for column in goal_columns:
            if pd.isna(current_mentee[column]).any():
                continue
            st.caption(column)
            st.write(current_mentee[column].values[0])

        st.subheader("任何想對未來導師說的話")
        current_mentee["任何想對未來導師說的話"].values[0]

    with col2:
        st.subheader("基本資料")
        st.caption(f"廣義研究領域")
        current_mentee["廣義研究領域"].values[0]
        st.caption(f"專業領域")
        current_mentee["專業領域"].values[0]

        st.subheader("目前申請準備進度")
        progress_columns = [
            "欲尋求之協助/建議(至多三個)",
            "請問您目前準備進度為何？是否已經完成選校？",
            "提供簡歷與相關資料",
            "是否已經參加留學國的語文程度測驗？",
            "目前申請文件的準備進度？",
            "目前是否已開始聯繫請求推薦信。",
            "是否已經參加標準化入學考試？",
        ]
        for column in progress_columns:
            if pd.isna(current_mentee[column]).any():
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
        "任何公開資訊 （選填）",
    ]
    for column in background_columns:
        if pd.isna(current_mentee[column]).any():
            continue
        st.caption(column)
        st.write(current_mentee[column].values[0])

    st.subheader("聯絡方式")
    contact_columns = [
        "電子郵件地址",
        "其餘聯絡方式 (非必填)",
    ]
    for column in contact_columns:
        if pd.isna(current_mentee[column]).any():
            continue
        st.caption(column)
        st.write(current_mentee[column].values[0])

elif viewing_mode == "Multiple Mentee Info":
    st.subheader("Multiple Mentee Info")
    options = st.multiselect(
        "You can select multiple mentees to compare their profiles.",
        mentee_response["中文姓名"].values,
    )

    st.dataframe(
        mentee_response.loc[mentee_response["中文姓名"].isin(options), display_columns]
        .set_index("中文姓名")
        .transpose(),
        height=696,
        use_container_width=True,
    )
