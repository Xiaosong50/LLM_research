from flask import Flask, render_template, request, redirect, session, Response
from markdown import markdown
from db_config import get_connection
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.tables import TableExtension
import csv
import io
def render_markdown_safe(text):
    return markdown(text, extensions=[
        FencedCodeExtension(),
        CodeHiliteExtension(),
        TableExtension()
    ])
app = Flask(__name__, template_folder='templates')
app.secret_key = 'secret-key'

LEVEL_ORDER = {
    'Not familiar at all': 0,
    'Beginner': 1,
    'Moderate': 2,
    'Proficient': 3,
    'Very proficient': 4
}
@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM answers WHERE student_email = %s", (email,))
        user = cursor.fetchone()

        if user:
            student_id = user['id']
            cursor.execute("SELECT COUNT(openai_default_rank) as count FROM llm_feedback WHERE student_id = %s", (student_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()

            if result['count'] > 0:
                return redirect('/thankyou')
            else:
                session['student_id'] = student_id
                return redirect('/term')
        else:
            cursor.close()
            conn.close()
            return render_template("unregistered.html")

    return render_template('login.html')


# --- app.py (partial) ---

@app.route('/term', methods=['GET', 'POST'])
def term():
    student_id = session.get('student_id')
    if not student_id:
        return redirect('/login')

    selected_indices = get_selected_question_indices(student_id)
    return render_survey_route(questions_range=selected_indices, template='term.html')

@app.route('/coding', methods=['GET', 'POST'])
def coding():
    return render_survey_route(questions_range=[7], template='coding.html')

def get_selected_question_indices(student_id):
    conn = get_connection()  # 保留 conn 对象，防止被 GC 回收
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT java_programming, `SQL`, data_mining_and_machine_learning, IoT, HCI, blockchains
        FROM answers WHERE id = %s
    """, (student_id,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    skill_levels = {
        'java_programming': LEVEL_ORDER.get(row['java_programming'], -1),
        'SQL': LEVEL_ORDER.get(row['SQL'], -1),
        'data_mining_and_machine_learning': LEVEL_ORDER.get(row['data_mining_and_machine_learning'], -1),
        'IoT': LEVEL_ORDER.get(row['IoT'], -1),
        'HCI': LEVEL_ORDER.get(row['HCI'], -1),
        'blockchains': LEVEL_ORDER.get(row['blockchains'], -1),
    }

    sorted_skills = sorted(skill_levels.items(), key=lambda x: x[1])
    lowest = [name for name, _ in sorted_skills[:2]]
    highest = [name for name, _ in sorted_skills[-2:]]

    skill_to_index = {
        'java_programming': 1,
        'SQL': 2,
        'data_mining_and_machine_learning': 3,
        'IoT': 4,
        'HCI': 5,
        'blockchains': 6,
    }

    return [skill_to_index[skill] for skill in lowest + highest]

def render_survey_route(questions_range, template):
    if 'student_id' not in session:
        return redirect('/login')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    student_id = session['student_id']

    if request.method == 'POST':
        # for i in questions_range:
        for idx, qidx in enumerate(questions_range, start=1):
            qid = request.form.get(f'question_id_{idx}')
            # qid = request.form.get(f'question_id_{i}')
            ############了解程度
            # pre = request.form.get(f'pre_score_{idx}')
            # post = request.form.get(f'post_score_{idx}')
            ############
            ranks = [request.form.get(f'rank_{j}_{idx}') for j in range(1, 6)]

            cursor.execute("""
                INSERT INTO llm_feedback (
                    student_id, question_id, 
                    openai_default_rank,
                    openai_skills_rank,
                    openai_hobbies_rank,
                    openai_subjects_rank,
                    openai_all_rank
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    openai_default_rank = VALUES(openai_default_rank),
                    openai_skills_rank = VALUES(openai_skills_rank),
                    openai_hobbies_rank = VALUES(openai_hobbies_rank),
                    openai_subjects_rank = VALUES(openai_subjects_rank),
                    openai_all_rank = VALUES(openai_all_rank);
            """, (student_id, qid, *ranks))

        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/coding') if template == 'term.html' else redirect('/thankyou')

    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()

    # cursor.execute("SELECT * FROM deepseek_response_default")
    # deepseek_default_responses = {
    #     row['question_id']: render_markdown_safe(row['response'])
    #     for row in cursor.fetchall()
    # }

    # cursor.execute("SELECT * FROM deepseek_response_skills WHERE student_id = %s", (student_id,))
    # deepseek_skills = cursor.fetchone()

    # cursor.execute("SELECT * FROM deepseek_response_hobbies WHERE student_id = %s", (student_id,))
    # deepseek_hobbies = cursor.fetchone()

    # cursor.execute("SELECT * FROM deepseek_response_subjects WHERE student_id = %s", (student_id,))
    # deepseek_subjects = cursor.fetchone()

    # cursor.execute("SELECT * FROM deepseek_response_all WHERE student_id = %s", (student_id,))
    # deepseek_all = cursor.fetchone()


    cursor.execute("SELECT * FROM openai_response_default")
    openai_default_responses = {
        row['question_id']: render_markdown_safe(row['response'])
        for row in cursor.fetchall()
    }

    cursor.execute("SELECT * FROM openai_response_skills WHERE student_id = %s", (student_id,))
    openai_skills = cursor.fetchone()

    cursor.execute("SELECT * FROM openai_response_hobbies WHERE student_id = %s", (student_id,))
    openai_hobbies = cursor.fetchone()

    cursor.execute("SELECT * FROM openai_response_subjects WHERE student_id = %s", (student_id,))
    openai_subjects = cursor.fetchone()

    cursor.execute("SELECT * FROM openai_response_all WHERE student_id = %s", (student_id,))
    openai_all = cursor.fetchone()


    topic_fields = [
        'java_response', 'sql_response', 'data_mining_response', 'IOT_response',
        'HCI_response', 'blockchains_response', 'coding_response'
    ]

    all_responses = []
    for i in questions_range:
        q = questions[i - 1]
        qid = q['question_id']
        topic_field = topic_fields[i - 1]
        response = {
            'question': render_markdown_safe(q['question']),
            'question_id': qid,
            # 'deepseek_default': render_markdown_safe(deepseek_default_responses.get(qid, '')),
            # 'deepseek_skills': render_markdown_safe(deepseek_skills[topic_field]) if deepseek_skills else '',
            # 'deepseek_hobbies': render_markdown_safe(deepseek_hobbies[topic_field]) if deepseek_hobbies else '',
            # 'deepseek_subjects': render_markdown_safe(deepseek_subjects[topic_field]) if deepseek_subjects else '',
            # 'deepseek_all': render_markdown_safe(deepseek_all[topic_field]) if deepseek_all else ''

            'openai_default': render_markdown_safe(openai_default_responses.get(qid, '')),
            'openai_skills': render_markdown_safe(openai_skills[topic_field]) if openai_skills else '',
            'openai_hobbies': render_markdown_safe(openai_hobbies[topic_field]) if openai_hobbies else '',
            'openai_subjects': render_markdown_safe(openai_subjects[topic_field]) if openai_subjects else '',
            'openai_all': render_markdown_safe(openai_all[topic_field]) if openai_all else ''
        }

        all_responses.append(response)

    cursor.close()
    conn.close()
    return render_template(template, responses=all_responses)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/feedback')
def feedback():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT f.*, a.gender, a.level_of_study,
               CASE f.question_id
                   WHEN 1 THEN 'java_programming'
                   WHEN 2 THEN 'SQL'
                   WHEN 3 THEN 'data_mining_and_machine_learning'
                   WHEN 4 THEN 'IoT'
                   WHEN 5 THEN 'HCI'
                   WHEN 6 THEN 'blockchains'
                   ELSE NULL
               END AS skill_name,
               CASE f.question_id
                   WHEN 1 THEN a.java_programming
                   WHEN 2 THEN a.SQL
                   WHEN 3 THEN a.data_mining_and_machine_learning
                   WHEN 4 THEN a.IoT
                   WHEN 5 THEN a.HCI
                   WHEN 6 THEN a.blockchains
                   ELSE NULL
               END AS knowledge_level
        FROM llm_feedback f
        JOIN answers a ON f.student_id = a.id
        ORDER BY f.feedback_id, f.student_id
    """)
    feedbacks = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('feedback.html', feedbacks=feedbacks)


@app.route('/download_feedback')
def download_feedback():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # 跟 feedback 页面一样的查询，带上 Skill 和 Knowledge Level
    cursor.execute("""
        SELECT f.*, a.gender, a.level_of_study,
               CASE f.question_id
                   WHEN 1 THEN 'java_programming'
                   WHEN 2 THEN 'SQL'
                   WHEN 3 THEN 'data_mining_and_machine_learning'
                   WHEN 4 THEN 'IoT'
                   WHEN 5 THEN 'HCI'
                   WHEN 6 THEN 'blockchains'
                   ELSE NULL
               END AS skill_name,
               CASE f.question_id
                   WHEN 1 THEN a.java_programming
                   WHEN 2 THEN a.SQL
                   WHEN 3 THEN a.data_mining_and_machine_learning
                   WHEN 4 THEN a.IoT
                   WHEN 5 THEN a.HCI
                   WHEN 6 THEN a.blockchains
                   ELSE NULL
               END AS knowledge_level
        FROM llm_feedback f
        JOIN answers a ON f.student_id = a.id
        ORDER BY f.feedback_id, f.student_id
    """)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)

    # CSV列名
    header = [
        'Feedback ID', 'Student ID', 'Question ID',
        'Skill', 'Knowledge Level', 'Gender','Level of study',
        'Deepseek Default', 'Deepseek Skills', 'Deepseek Hobbies', 'Deepseek Subjects', 'Deepseek All', 
        'OpenAI Default','OpenAI Skills', 'OpenAI Hobbies', 'OpenAI Subjects', 'OpenAI All'
    ]
    writer.writerow(header)

    for row in rows:
        writer.writerow([
            row['feedback_id'],
            row['student_id'],
            row['question_id'],
            row['skill_name'] if row['question_id'] <= 6 else '-',
            row['knowledge_level'] if row['question_id'] <= 6 else '-',
            row['gender'],
            row['level_of_study'],
            row['deepseek_default_rank'],
            row['deepseek_skills_rank'],
            row['deepseek_hobbies_rank'],
            row['deepseek_subjects_rank'],
            row['deepseek_all_rank'],
            row['openai_default_rank'],
            row['openai_skills_rank'],
            row['openai_hobbies_rank'],
            row['openai_subjects_rank'],
            row['openai_all_rank'],
        ])

    output.seek(0)
    return Response(
        output,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=llm_feedback.csv'}
    )

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=8080)