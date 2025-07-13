import pandas as pd
import pymysql

# 1. 读取 CSV 文件
df = pd.read_csv('/Users/xiaosonglu/Desktop/LLM-answers/llm_feedback.csv')

# 2. 只保留数据库中需要的列，并重命名为数据库中的字段名
df_clean = df.rename(columns={
    'Feedback ID': 'feedback_id',
    'Student ID': 'student_id',
    'Question ID': 'question_id',
    'Default Rank': 'deepseek_default_rank',
    'Skills Rank': 'deepseek_skills_rank',
    'Hobbies Rank': 'deepseek_hobbies_rank',
    'Subjects Rank': 'deepseek_subjects_rank',
    'All Rank': 'deepseek_all_rank'
})[
    ['feedback_id', 'student_id', 'question_id',
     'deepseek_default_rank', 'deepseek_skills_rank', 'deepseek_hobbies_rank', 'deepseek_subjects_rank', 'deepseek_all_rank']
]

# 3. 设置数据库连接
conn = pymysql.connect(
    host='localhost',
    user='admin',
    password='Lxs,123321',
    database='survey'
)
cursor = conn.cursor()

# 4. 插入数据
for _, row in df_clean.iterrows():
    sql = """
    INSERT INTO llm_feedback (
        feedback_id, student_id, question_id,
        deepseek_default_rank, deepseek_skills_rank, deepseek_hobbies_rank, deepseek_subjects_rank, deepseek_all_rank
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, tuple(row))

conn.commit()
cursor.close()
conn.close()
print("✅ 数据已成功插入 llm_feedback 表！")