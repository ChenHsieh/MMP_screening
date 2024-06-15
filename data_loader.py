import pandas as pd
from config import settings

def load_mentors():
    mentors_table = pd.read_csv(settings['mentors_csv_export_url'])
    mentors_table.set_index("verification_code", inplace=True)
    return mentors_table

def load_mentee_data(mentor_name):
    data = pd.read_csv(settings['mentee_response_csv_export_url'])
    data = data.loc[
        (data["希望配對的導師（第一志願）"] == mentor_name) |
        (data["希望配對的導師（第二志願）.1"] == mentor_name) |
        (data["希望配對的導師（第三志願）.1"] == mentor_name) |
        (data["希望配對的導師（第四志願）.1"] == mentor_name) |
        (data["希望配對的導師（第五志願）.1"] == mentor_name)
    ]
    return data
