from flask import Flask
import energy
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import dateutil
import golf_reserve2

app = Flask(__name__)
@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/energy')
def check_update():
    energy.check_update()
    return 'Energy'

@app.route('/make_reserve')
def make_reserve():
    user_id = 'lima36'
    user_pw = 'peace@2020'
    user_phone = "010-7795-5647"

    target = datetime.datetime.today() + dateutil.relativedelta.relativedelta(days=21)
    targetDate1 = datetime.datetime.strftime(target, '%Y%m%d')
    print(targetDate1)
    target_date = targetDate1#'20220226'
    target_time = '0800:1255'

    golf_reserve2.make_reserve(user_id, user_pw, target_date, target_time, user_phone)
    return "make_reserve"


if __name__ == '__main__':
    #apscheduler 선언
    sched = BackgroundScheduler(daemon=True)

    # 1.반복적으로 실행

    # sched.add_job(scrawl,'interval', minutes=1)

    # 2. apscheduler실행설정, Cron방식으로, 1주-53주간실행, 월요일부터금요일까지실행, 8시에실행
    sched.add_job(make_reserve,'cron', week='1-53', day_of_week='0-6', hour='09', minute='00')
    # of June, July, August, November and December at 00:00, 01:00, 02:00 and 03:00
    # sched.add_job(job_function, 'cron', month='6-8,11-12', day='3rd fri', hour='0-3')
    # 출처: https://tomining.tistory.com/138 [마이너의 일상]

    #apscheduler실행
    sched.start()

    app.run(debug=True)