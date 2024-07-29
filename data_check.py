import streamlit as st
import pandas as pd

# Load URLs from secrets and prepare for CSV download
mentee_response_sheet_url = st.secrets["mentee_response_sheet_url"].replace('/edit?gid=', '/export?format=csv&gid=')
mentee_matching_sheet_url = st.secrets["mentee_matching_sheet_url"].replace('/edit?gid=', '/export?format=csv&gid=')
mentor_matching_result_sheet_url = st.secrets["mentor_matching_result_sheet_url"].replace('/edit?gid=', '/export?format=csv&gid=')

# Load data once and reuse
mentee_response_df = pd.read_csv(mentee_response_sheet_url).dropna(how='all')
mentee_matching_df = pd.read_csv(mentee_matching_sheet_url)
mentors_df = pd.read_csv(mentor_matching_result_sheet_url, index_col="verification_code")

# Clean and prepare data
mentee_response_df["中文姓名"] = mentee_response_df["中文姓名"].apply(lambda x: x.strip() if isinstance(x, str) else x)

def load_mentee_data(mentee_id_list, mentee_response_df, mentee_matching_df):
    # Create a mapping from mentee_id to name
    id_to_name = dict(zip(mentee_matching_df['mentee_id'], mentee_matching_df['name_mentee']))
    # Map mentee IDs to names
    mentee_names = [id_to_name.get(mentee_id, None) for mentee_id in mentee_id_list]
    # Filter responses by names
    mentee_response = mentee_response_df[mentee_response_df["中文姓名"].isin(mentee_names)]
    return mentee_response

def convert_df_to_csv(df):
    return df.to_csv().encode('utf-8-sig')

# Initialize counter for entries checked
entries_checked = 0

# Process mentor data
for verification_code, row in mentors_df.iterrows():
    mentor_name = row["combined_mentor_id"]
    mentee_ids = row[["mentee_MSc", "mentee_PhD"]].dropna().str.split().explode().tolist()
    
    mentee_response = load_mentee_data(mentee_ids, mentee_response_df, mentee_matching_df)
    submitted_count = mentee_response.shape[0]
    expected_count = len(mentee_ids)
    
    if submitted_count != expected_count:
        st.write(f"{mentor_name} has {expected_count} mentees, but only {submitted_count} have submitted the form.")
        st.write("Please check the mentee list and the form submission status.")
        st.write(f"Mentee IDs: {mentee_ids}")
        st.write(f"Submitted Mentees: {mentee_response['中文姓名'].tolist()}")
        st.stop()
    else:
        entries_checked += 1

# Report on the data check process
st.write(f"All {entries_checked} entries have been checked. No discrepancies found.")
