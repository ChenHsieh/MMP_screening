
### this is simply a mock app, it does not reflect the actual logic of the real app

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Mentor Dashboard",
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
st.title('Project TYRA - Mentor Dashboard 2024 Matching Confirmation (Stage 2)')

st.markdown("""
Thank you for participating as a mentor in the TYRA MMP 2024 program. This dashboard allows you to review the profiles of mentees who have matched with you during both the first and second stages of the matching process.
""")

st.markdown("""
### How to Use This Dashboard
1. **Enter your verification code**: You received this code via email. Please note that it is case-sensitive.
2. **Review Mentee Profiles**: After entering your code, you will be able to see the profiles of the mentees matched with you in both the first and second stages, allowing you to review detailed information.
3. **Contact Your Mentees**: Once you have reviewed the profiles, please reach out to the mentees directly and begin the mentoring process according to the commitments you made during the program sign-up.
""")

mentee_response_sheet_url = "mock_mentee_data_stage1.csv"
mentee_response_stage2_sheet_url = "mock_mentee_data_stage2.csv"
mentee_matching_sheet_url = "mock_mentee_data_stage1.csv"
mentor_matching_result_sheet_url = "mock_mentee_data_stage1.csv"
mentor_matching_result_both_stage_sheet_url = "mock_mentee_data_stage2.csv"
mentee_matching_stage2_sheet_url = "mock_mentee_data_stage2.csv"


mentees_table = pd.read_csv(mentee_matching_sheet_url)
mentors_table = pd.read_csv(
    mentor_matching_result_sheet_url, index_col="verification_code")

def load_mentee_data_stage1(mentee_id_list):
    mentee_response_df = pd.read_csv(mentee_response_sheet_url)
    mentee_response_df = mentee_response_df.dropna(how='all')
    mentee_response_df["中文姓名"] = mentee_response_df["中文姓名"].apply(lambda x: x.strip() if isinstance(x, str) else x)

    mentee_matching_df = pd.read_csv(mentee_matching_sheet_url)

    id_to_name = dict(zip(mentee_matching_df['mentee_id'], mentee_matching_df['name_mentee']))

    # Convert the list of mentee IDs to mentee names
    mentee_names = list(map(id_to_name.get, mentee_id_list))
    
    mentee_response = mentee_response_df.loc[mentee_response_df["中文姓名"].isin(mentee_names)]
    
    return mentee_response


def load_mentee_data_stage2(mentee_id_list):
    mentee_response_df = pd.read_csv(mentee_response_stage2_sheet_url)
    mentee_response_df = mentee_response_df.dropna(how='all')
    mentee_response_df["中文姓名"] = mentee_response_df["中文姓名"].apply(lambda x: x.strip() if isinstance(x, str) else x)

    mentee_matching_df = pd.read_csv(mentee_matching_stage2_sheet_url)

    id_to_name = dict(zip(mentee_matching_df['mentee_id'], mentee_matching_df['name_mentee']))

    # Convert the list of mentee IDs to mentee names
    mentee_names = list(map(id_to_name.get, mentee_id_list))
    
    mentee_response = mentee_response_df.loc[mentee_response_df["中文姓名"].isin(mentee_names)]
    
    return mentee_response

def convert_df(df):
    return df.to_csv().encode('utf-8-sig')


verification_code_placeholder = 'test'

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


    "欲尋求之協助/建議(至多三個)",
    "請問您目前準備進度為何？是否已經完成選校？",
    "提供簡歷與相關資料",
    "是否已經參加留學國的語文程度測驗？",
    "目前是否已開始聯繫請求推薦信。",

    "請詳述申請留學之動機以及參加 MMP之動機",

    "任何公開資訊 （選填）",
    "是否為家族中第一代高等教育子女（選填）",
    "國際活動經驗（選填）",
    "學術領域外相關特殊專長、經驗或成就（選填）",
    "家人、伴侶等狀態（選填）",
    "目前的生涯規劃，或主要申請目的與動機（選填）",
    "您認為可能會影響申請過程或結果的身份、背景、經歷，而您希望導師知道的（選填）",

    "Email Address",
    "其餘聯絡方式 (非必填)",
]

mentor_verification_code = st.text_input(
    'Please input your "verification code" from the email. Please note that the "verification code" is case-sensitive.', verification_code_placeholder)

if (mentor_verification_code == ""):
    st.warning(
        f"The input is empty!")
    st.stop()

elif (mentor_verification_code in mentors_table.index):
    st.success(
        f"Hola {mentors_table.loc[mentor_verification_code]['name']}! Welcome to the mentor dashboard!"
    )
else:
    st.warning(
        f"Oops! We cannot find any results for the current input. Please check your verification code.")
    st.stop()

mentor_name = mentors_table.loc[mentor_verification_code]

mentee_id_list_stage1 = mentors_table

mentee_response = mentors_table
mentee_names_stage1 = mentee_response["中文姓名"].values



candidate_mentee_number = mentee_response.shape[0]

if candidate_mentee_number == 0:
    st.warning(
        "Thank you for volunteering to become a mentor. Unfortunately, during the initial matching process, all available mentees interested in you were assigned to other mentors. Please stay tuned for the second phase of matching, where we hope to connect you with a mentee. Your willingness to support others is greatly appreciated."
    )
    st.stop()
else:
    stage1_text = f'In the first stage, you were matched with: {"、".join(mentee_names_stage1)}.' if len(mentee_names_stage1) > 0 else ''
    

    st.success(f'Great! {stage1_text}')



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
        # Ensure the '志願序' value is converted to an integer
        preference_order = int(current_mentee['志願序'].values[0])

        # Display the metric with the integer value
        st.metric(f"選擇您為第 {preference_order} 志願", current_mentee["中文姓名"].values[0])

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
        ]
        for column in goal_columns:
            if (pd.isna(current_mentee[column]).any()):
                continue
            st.caption(column)
            st.write(current_mentee[column].values[0])

        st.subheader("申請留學之動機以及參加 MMP之動機")
        current_mentee["請詳述申請留學之動機以及參加 MMP之動機"].values[0]

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
                            "目前是否已開始聯繫請求推薦信。",
                            ]
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
        "任何公開資訊 （選填）", ]
    for column in background_columns:
        if (pd.isna(current_mentee[column]).any()):
            continue
        st.caption(column)
        st.write(current_mentee[column].values[0])

    st.subheader("聯絡方式")
    contact_columns = [
        "Email Address",
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
        'You can select multiple mentees to compare their profiles.',
        mentee_response["中文姓名"].values
    )

    st.dataframe(
        mentee_response.loc[
            mentee_response["中文姓名"].isin(options), display_columns].set_index("中文姓名").transpose(),
        height=696,
        use_container_width=True
    )

st.markdown("[go back to top](#know-your-mentee-better)")
st.divider()

st.write("""
Find more about TYRA
https://linktr.ee/projecttyra

If you find this project useful, please consider giving us a star on GitHub:
https://github.com/ChenHsieh/MMP_screening
""")
