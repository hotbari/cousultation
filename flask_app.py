# flask_app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import re

# 기본 설정
app = Flask(__name__)

# 폴더 구조 변경
# app = Flask(__name__, template_folder="../templates")
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# 데이터 정리

CONSULTATION_TIMES = {

    "930626": { "name" : "학생1",
                "consultation_time":"1월 16일 15시"
                },
    "950102": { "name" : "학생2",
                "consultation_time":"1월 16일 16시"
                },
    "930318": { "name" : "학생3",
                "consultation_time":"1월 16일 14시"
                },

    # -------------------------------------- 완료 -----------------------------------------
    "000208": { "name" : "학생4",
                "consultation_time": "1차 헬스체크 완료!"
                },
}

# @app.route("/")
# def home():
#     return render_template("base.html")

"""
문자열 검증
"""
def validate_date(date_str):
    """6자리 문자열로 받을 경우"""
    try:
        if not len(date_str) == 6 :
            return False
        return True
    except ValueError:
        return False


"""
생년월일 입력
"""
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        birthdate = request.form.get('birthdate')

        if not validate_date(birthdate):
            flash('입력값이 잘못되었습니다.')
            return redirect(url_for('login'))

        if birthdate not in CONSULTATION_TIMES:
            flash('상담 시간이 존재하지 않습니다. 연수 조교에게 문의하세요!')
            return redirect(url_for('login'))

        session['birthdate'] = birthdate
        return redirect(url_for('schedule'))

    return render_template('base.html')


"""
헬스체크 시간 출력
"""

@app.route('/schedule')
def schedule():
    birthdate = session.get('birthdate')
    if not birthdate:
        return redirect(url_for('login'))
    student_data = CONSULTATION_TIMES.get(birthdate)
    consultation_time = student_data['consultation_time']
    if consultation_time == "일 시":
        consultation_time = "아직 헬스체크 일정이 배정되지 않았습니다."

    print(birthdate[2:4]) # 01
    print(datetime.now().month) # 1
    birth_msg =  '이번 달 생일을 축하드립니다 :)'
    if birthdate[2:4] :
        if len(str(datetime.now().month)) == 1 :
            today_month = '0' + str(datetime.now().month)
        if birthdate[2:4] == today_month:
            return render_template('schedule.html',
                                   name=student_data['name'],
                                   consultation_time=consultation_time,
                                   # consultation_time=student_data['consultation_time'],
                                   info='헬스체크 시에는 카메라와 마이크 사용이 필요합니다!',
                                   msg='장비 사용에 문제가 없는지 미리 확인해주세요.',
                                   birth_msg = birth_msg)

    return render_template('schedule.html',
                           name = student_data['name'],
                           consultation_time = consultation_time,
                           # consultation_time=student_data['consultation_time'],
                           info='헬스체크 시에는 카메라와 마이크 사용이 필요합니다!',
                           msg='장비 사용에 문제가 없는지 미리 확인해주세요 :)')


if __name__ == '__main__':
    app.run(debug=False,port=5001)