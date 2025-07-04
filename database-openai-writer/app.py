from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'admin',
    'password': 'Lxs,123321',
    'database': 'survey',
    'charset': 'utf8mb4'
}
# DB_CONFIG = {
#     'host': '192.168.172.74',
#     'port': 5000,
#     'user': 'admin',
#     'password': 'admin123321',
#     'database': 'survey',
#     'charset': 'utf8mb4'
# }


@app.route('/skills', methods=['POST'])
def save_skills_response():
    data = request.json

    student_id = data.get("student_id")
    java_response = data.get("java_response")
    sql_response = data.get("sql_response")
    data_mining_response = data.get("data_mining_response")
    IOT_response = data.get("IOT_response")
    HCI_response = data.get("HCI_response")
    blockchains_response = data.get("blockchains_response")
    coding_response = data.get("coding_response")

    # 必填校验（仅学生ID，其他字段允许为空）
    if not all([student_id, java_response, sql_response, data_mining_response, IOT_response, HCI_response, blockchains_response, coding_response]):
        return jsonify({'status': 'error', 'message': 'Missing data'}), 400

    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO openai_response_skills (
                    student_id,
                    java_response,
                    sql_response,
                    data_mining_response,
                    IOT_response,
                    HCI_response,
                    blockchains_response,
                    coding_response
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            # sql = """
            #     UPDATE llm_response_skills
            #     SET 
            #         java_response = %s,
            #         sql_response = %s,
            #         data_mining_response = %s,
            #         IOT_response = %s,
            #         HCI_response = %s,
            #         blockchains_response = %s,
            #         coding_response = %s
            #     WHERE student_id = %s;
            # """
            cursor.execute(sql, (
                student_id,
                java_response,
                sql_response,
                data_mining_response,
                IOT_response,
                HCI_response,
                blockchains_response,
                coding_response
            ))
        conn.commit()
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500



# hobbies

@app.route('/hobbies', methods=['POST'])
def save_hobbies_response():
    data = request.json

    student_id = data.get("student_id")
    java_response = data.get("java_response")
    sql_response = data.get("sql_response")
    data_mining_response = data.get("data_mining_response")
    IOT_response = data.get("IOT_response")
    HCI_response = data.get("HCI_response")
    blockchains_response = data.get("blockchains_response")
    coding_response = data.get("coding_response")

    # 必填校验（仅学生ID，其他字段允许为空）
    if not all([student_id, java_response, sql_response, data_mining_response, IOT_response, HCI_response, blockchains_response, coding_response]):
        return jsonify({'status': 'error', 'message': 'Missing data'}), 400

    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO openai_response_hobbies (
                    student_id,
                    java_response,
                    sql_response,
                    data_mining_response,
                    IOT_response,
                    HCI_response,
                    blockchains_response,
                    coding_response
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                student_id,
                java_response,
                sql_response,
                data_mining_response,
                IOT_response,
                HCI_response,
                blockchains_response,
                coding_response
            ))
        conn.commit()
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# subjects

@app.route('/subjects', methods=['POST'])
def save_subjects_response():
    data = request.json

    student_id = data.get("student_id")
    java_response = data.get("java_response")
    sql_response = data.get("sql_response")
    data_mining_response = data.get("data_mining_response")
    IOT_response = data.get("IOT_response")
    HCI_response = data.get("HCI_response")
    blockchains_response = data.get("blockchains_response")
    coding_response = data.get("coding_response")


    # 必填校验（仅学生ID，其他字段允许为空）
    if not all([student_id, java_response, sql_response, data_mining_response, IOT_response, HCI_response, blockchains_response, coding_response]):
        return jsonify({'status': 'error', 'message': 'Missing data'}), 400

    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO openai_response_subjects (
                    student_id,
                    java_response,
                    sql_response,
                    data_mining_response,
                    IOT_response,
                    HCI_response,
                    blockchains_response,
                    coding_response
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                student_id,
                java_response,
                sql_response,
                data_mining_response,
                IOT_response,
                HCI_response,
                blockchains_response,
                coding_response
            ))
        conn.commit()
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# all

@app.route('/all', methods=['POST'])
def save_all_response():
    data = request.json

    student_id = data.get("student_id")
    java_response = data.get("java_response")
    sql_response = data.get("sql_response")
    data_mining_response = data.get("data_mining_response")
    IOT_response = data.get("IOT_response")
    HCI_response = data.get("HCI_response")
    blockchains_response = data.get("blockchains_response")
    coding_response = data.get("coding_response")

    # 必填校验（仅学生ID，其他字段允许为空）
    if not all([student_id, java_response, sql_response, data_mining_response, IOT_response, HCI_response, blockchains_response, coding_response]):
        return jsonify({'status': 'error', 'message': 'Missing data'}), 400

    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO openai_response_all (
                    student_id,
                    java_response,
                    sql_response,
                    data_mining_response,
                    IOT_response,
                    HCI_response,
                    blockchains_response,
                    coding_response
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                student_id,
                java_response,
                sql_response,
                data_mining_response,
                IOT_response,
                HCI_response,
                blockchains_response,
                coding_response
            ))
        conn.commit()
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# default
@app.route('/default', methods=['POST'])
def save_default_response():
    data = request.json

    question_id = data.get("question_id")
    response = data.get("response")
    

    # 必填校验（仅学生ID，其他字段允许为空）
    if not all([question_id, response]):
        return jsonify({'status': 'error', 'message': 'Missing data'}), 400

    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO openai_response_default (
                    question_id,
                    response
                ) VALUES (%s, %s)
            """
            cursor.execute(sql, (
                question_id,
                response
            ))
        conn.commit()
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# --------------------------------------------------------------------------

# # coding-subjects
# @app.route('/codingsubjects', methods=['POST'])
# def save_codingsubjects_response():
#     data = request.json

#     student_id = data.get("student_id")
#     response = data.get("response")
    

#     # 必填校验（仅学生ID，其他字段允许为空）
#     if not all([student_id, response]):
#         return jsonify({'status': 'error', 'message': 'Missing data'}), 400

#     try:
#         conn = pymysql.connect(**DB_CONFIG)
#         with conn.cursor() as cursor:
#             sql = """
#                 UPDATE llm_response_subjects
#                 SET coding_response = %s
#                 WHERE student_id = %s;
#             """
#             cursor.execute(sql, (
#                 response,
#                 student_id
#             ))
#         conn.commit()
#         return jsonify({'status': 'success'}), 200
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500


# # coding-all
# @app.route('/codingall', methods=['POST'])
# def save_codingall_response():
#     data = request.json

#     student_id = data.get("student_id")
#     response = data.get("response")
    

#     # 必填校验（仅学生ID，其他字段允许为空）
#     if not all([student_id, response]):
#         return jsonify({'status': 'error', 'message': 'Missing data'}), 400

#     try:
#         conn = pymysql.connect(**DB_CONFIG)
#         with conn.cursor() as cursor:
#             sql = """
#                 UPDATE llm_response_all
#                 SET coding_response = %s
#                 WHERE student_id = %s;
#             """
#             cursor.execute(sql, (
#                 response,
#                 student_id
#             ))
#         conn.commit()
#         return jsonify({'status': 'success'}), 200
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)