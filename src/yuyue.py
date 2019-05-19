import requests, json, hashlib

# 其实写这个的目的不是用做爬虫，而是让那些不方便登录预约系统的开发者了解预约系统的数据格式
# 目前正在探索各个错误码的意义
# 目前可知的是 若错误码为0则正常，为负则为异常

# 下面是各个功能的请求URL

__query_url = 'https://mathe.neu.edu.cn:8080/api/v2/reserve/query'  # 这个URL毕竟特殊，不需要登录就能查询，可能并不打算开放的
__choose_exam_url = 'https://mathe.neu.edu.cn:8080/api/v2/reserve/try'
__login_url = 'https://mathe.neu.edu.cn:8080/api/auth/login'   # 登录URL与其他格式不同
__cancel_url = 'https://mathe.neu.edu.cn:8080/api/v2/reserve/cancel'
__papers_url = 'https://mathe.neu.edu.cn:8080/api/v2/reserve/papers'
__dates_url = 'https://mathe.neu.edu.cn:8080/api/v2/reserve/dates'
__rooms_url = 'https://mathe.neu.edu.cn:8080/api/v2/reserve/rooms'
__rounds_url = 'https://mathe.neu.edu.cn:8080/api/v2/reserve/rounds'
__seats_url = 'https://mathe.neu.edu.cn:8080/api/v2/reserve/seats'


# 通过查询页面得到的已选考试 keyword可以是姓名也可以是学号
def get_choose_exams(keyword):
    return requests.post(__query_url, data='{"keyword":"%s"}'%keyword).json()

# 登录请求，如果返回code为0，则data中包含token用于以后的请求
def login(username, password):
    pwd_md5 = hashlib.md5(password.encode()).hexdigest()
    data = '{"username":"%s","password":"%s"}'%(username, pwd_md5)
    return requests.post(__login_url, data=data).json()


def choose_exam(date_id, paper_id, room_id, round_id, token):
    data = {
        'date_id': date_id,
        'paper_id': paper_id,
        'room_id': room_id,
        'round_id': round_id,
        'token': token
    }
    return requests.post(__choose_exam_url, data=json.dumps(data)).json()


def cancel_exam(exam_id, token):
    data = {
        'id': exam_id,
        'token': token
    }
    return requests.post(__cancel_url, data=json.dumps(data)).json()


def get_exams(token):
    return requests.post(__papers_url, json.dumps({'token': token})).json()


def get_exam_date(token, exam_id):
    return requests.post(__dates_url, data=json.dumps({'paper_id': exam_id,'token': token}))


def get_exam_room(token, date_id):
    return requests.post(__rooms_url, data=json.dumps({'date_id': date_id,'token': token}))


def get_exam_round(token, date_id, paper_id, room_id):
    data = {
        'date_id': date_id,
        'paper_id': paper_id,
        'room_id': room_id,
        'token': token
    }
    return requests.post(__rounds_url, data=json.dumps(data)).json()


def get_seat_num(date_id, room_id, round_id, token):
    data = {
        'date_id': date_id,
        'room_id': room_id,
        'round_id': round_id,
        'token': token
    }
    return requests.post(__seats_url, data=json.dumps(data)).json()