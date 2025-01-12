# index.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import re

# 기본 설정
# app = Flask(__name__)

# 폴더 구조 변경
app = Flask(__name__, template_folder="../templates")
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# 데이터 정리
"""
15시 = 1, 16시 = 2, 17시 = 3
"""
# 1차
# 새싹반 8인 먼저
mday_1 = "1월 13일 15시" # 장현영
mday_2 = "1월 13일 16시" # 임성욱
mday_3 = "1월 13일 17시" # 김지안

tday_1 = "1월 14일 15시" # 김나미
tday_2 = "1월 14일 16시" # 김지수(부산)
tday_3 = "1월 14일 17시" # 김한서

wday_1 = "1월 15일 15시" # 이삭
wday_2 = "1월 15일 16시" # 홍승우

wday_3 = "1월 15일 17시" # 송희태

# 조수민
# 이준호
# 정영하
# 명보경
# 배현우
# 김지수(서울)
# 노지민

# 고근우
# 권도현
# 권지원
# 김나경
# 김우중
# 김태진
# 박유진
# 이영득
# 이현경
# 장태문
# 정근영
# 정한율

CONSULTATION_TIMES = {
    # 새싹반 먼저
    "980314": { "name" : "고근우",
                "consultation_time":"일 시"
                },
    "001221": { "name" : "권도현",
                "consultation_time":"일 시"
                },
    "030709": { "name" : "권지원",
                "consultation_time":"일 시"
                },
    "010330": { "name" : "김나경",
                "consultation_time":"일 시"
                },
    "870126": { "name" : "김나미", # 새싹반
                "consultation_time": tday_1
                },
    "950422": { "name" : "김우중",
                "consultation_time":"일 시"
                },
    "940826": { "name" : "김지수(서울)",
                "consultation_time":"일 시"
                },
    "980323": { "name" : "김지수(부산)", # 새싹반
                "consultation_time": tday_2
                },
    "000407": { "name" : "김지안", # 새싹반
                "consultation_time": mday_3
                },
    "920131": { "name" : "김태진",
                "consultation_time":"일 시"
                },
    "020912": { "name" : "김한서", # 새싹반
                "consultation_time": tday_3
                },
    "000121": { "name" : "노지민",
                "consultation_time":"일 시"
                },
    "000208": { "name" : "명보경",
                "consultation_time":"일 시"
                },
    "920821": { "name" : "박유진",
                "consultation_time":"일 시"
                },
    "930318": { "name" : "배현우",
                "consultation_time":"일 시"
                },
    "950914": { "name" : "송희태",
                "consultation_time": wday_3
                },
    "990318": { "name" : "이삭",
                "consultation_time": wday_1
                },
    "901112": { "name" : "이영득",
                "consultation_time":"일 시"
                },
    "950102": { "name" : "이준호",
                "consultation_time":"일 시"
                },
    "991217": { "name" : "이현경",
                "consultation_time":"일 시"
                },
    "860307": { "name" : "임성욱", # 새싹반
                "consultation_time": mday_2
                },
    "930806": { "name" : "장태문",
                "consultation_time":"일 시"
                },
    "970128": { "name" : "장현영", # 새싹반
                "consultation_time": mday_1
                },
    "970612": { "name" : "정근영",
                "consultation_time":"일 시"
                },
    "980706": { "name" : "정영하",
                "consultation_time":"일 시"
                },
    "980204": { "name" : "정한율",
                "consultation_time":"일 시"
                },
    "930626": { "name" : "조수민",
                "consultation_time":"일 시"
                },
    "970813": { "name" : "홍승우", # 새싹반
                "consultation_time": wday_2
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
    app.run(debug=False)