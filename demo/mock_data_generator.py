import pandas as pd
from faker import Faker
import random

fake = Faker()

# Generate mock mentee data
def generate_mock_mentee_data(num_mentees):
    mentee_data = []
    for _ in range(num_mentees):
        mentee_data.append({
            "志願序": random.randint(1, 5),
            "中文姓名": fake.name(),
            "申請年份": random.choice(["2024", "2025"]),
            "欲申請學位": random.choice(["MSc", "PhD"]),
            "最高學歷": random.choice(["Bachelor's", "Master's"]),
            "學士就讀/畢業學校": fake.company(),
            "學士就讀/畢業系所": fake.job(),
            "碩士就讀/畢業學校": fake.company(),
            "碩士就讀/畢業系所": fake.job(),
            "廣義研究領域": random.choice(["Biology", "Physics", "Chemistry", "Engineering"]),
            "專業領域": fake.job(),
            "主要申請系所所在國家": fake.country(),
            "欲申請學校": fake.company(),
            "欲申請系所/program": fake.bs(),
            "欲尋求之協助/建議(至多三個)": fake.sentence(),
            "請問您目前準備進度為何？是否已經完成選校？": fake.sentence(),
            "提供簡歷與相關資料": fake.sentence(),
            "是否已經參加留學國的語文程度測驗？": random.choice(["Yes", "No"]),
            "目前是否已開始聯繫請求推薦信。": random.choice(["Yes", "No"]),
            "請詳述申請留學之動機以及參加 MMP之動機": fake.paragraph(),
            "任何公開資訊 （選填）": fake.sentence(),
            "是否為家族中第一代高等教育子女（選填）": random.choice(["Yes", "No"]),
            "國際活動經驗（選填）": fake.sentence(),
            "學術領域外相關特殊專長、經驗或成就（選填）": fake.sentence(),
            "家人、伴侶等狀態（選填）": fake.sentence(),
            "目前的生涯規劃，或主要申請目的與動機（選填）": fake.paragraph(),
            "您認為可能會影響申請過程或結果的身份、背景、經歷，而您希望導師知道的（選填）": fake.sentence(),
            "Email Address": fake.email(),
            "其餘聯絡方式 (非必填)": fake.phone_number(),
        })
    return pd.DataFrame(mentee_data)

# Save mock data
mock_data_stage1 = generate_mock_mentee_data(10)
mock_data_stage2 = generate_mock_mentee_data(10)

mock_data_stage1.to_csv("mock_mentee_data_stage1.csv", index=False, encoding='utf-8-sig')
mock_data_stage2.to_csv("mock_mentee_data_stage2.csv", index=False, encoding='utf-8-sig')