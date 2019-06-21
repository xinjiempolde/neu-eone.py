from flask import Flask
from flask import request
import neu,json

app = Flask(__name__)

# 学期转化字典
transformer = {
    '11': {'schoolYear': '2018-2019', 'semester': '1'},
    '30': {'schoolYear': '2018-2019', 'semester': '2'},
    '49': {'schoolYear': '2018-2019', 'semester': '3'},
    '12': {'schoolYear': '2019-2020', 'semester': '1'},
    '31': {'schoolYear': '2019-2020', 'semester': '2'},
    '54': {'schoolYear': '2019-2020', 'semester': '3'}
}

# 课程查询入口
@app.route('/mini/api/getNewTermCourse', methods=['POST'])
def getNewTermCourse():
    data = json.loads(request.data)
    stu = neu.NeuStu(data['stuID'],data['stuPass'])
    response = {"message": "教务处可以正常访问，获取即时数据", "code": 200}
    if stu.success:
        try:
            # 尝试获取课程
            courses =  stu.get_course( transformer[data['term']]['schoolYear'], transformer[data['term']]['semester'] )
        except:
            response['message']="访问教务处错误"
            response['code']=500
            courses = []
    else:
        response['message'] = "登录错误"
        response['code'] = 400
        courses=[]
    response['data']=courses
    return json.dumps(response,ensure_ascii=False)


app.run()
