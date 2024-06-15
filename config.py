settings = {
    'page_title': "MMP Screening App",
    'page_icon': "⛵️",
    'layout': "wide",
    'initial_sidebar_state': "expanded",
    'menu_items': {
        'About': """Find more about TYRA
https://linktr.ee/projecttyra

If you find this project useful, please consider giving us a star on GitHub:
https://github.com/ChenHsieh/MMP_screening
"""
    }
}

import os

# Determine environment (local or online)
if os.getenv("LOCAL_TESTING"):
    settings['mentee_response_csv_export_url'] = "data/mentee_responses_mock.csv"
    settings['mentors_csv_export_url'] = "data/mentors_mock.csv"
else:
    settings['mentee_response_csv_export_url'] = os.getenv("MENTEE_SHEET_URL").replace('/edit#gid=', '/export?format=csv&gid=')
    settings['mentors_csv_export_url'] = os.getenv("MENTORS_SHEET_URL").replace('/edit#gid=', '/export?format=csv&gid=')
