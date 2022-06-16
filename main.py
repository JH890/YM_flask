from flask import Flask, render_template, request, make_response, Response
import pymysql
import datetime
import time
import json
from time import time, sleep
from random import random

app = Flask(__name__)

candleData = [
      ['Mon', 20, 28, 38, 45],
      ['Tue', 31, 38, 55, 66],
      ['Wed', 50, 55, 77, 80],
      ['Thu', 77, 77, 66, 50],
      ['Fri', 68, 66, 22, 15]]


@app.route('/Detect')
def test_data():
    def test_raw_data():
        test_img_file = "test_image1"
        test_model_name = "test_model1"
        test_len_str = 100
        test_len_end = 200
        test_thick_len = [100, 120, 140, 160, 180, 200]
        test_thick = [0.3, 0.3, 0.4, 0.7, 0.6, 0.3]
        while True:

            # 이미지 파일 테스트 용
            if test_img_file == "test_image1":
                test_img_file = "test_image2"
            elif test_img_file == "test_image2":
                test_img_file = "test_image1"

            # 모델명 테스트 용
            if test_model_name == "test_model1":
                test_model_name = "test_model2"
            elif test_model_name == "test_model2":
                test_model_name = "test_model1"

            # 길이 시작 지점, 종료 지점 테스트 용
            if test_len_str == 100:
                test_len_str = 200
                test_len_end = 300
            elif test_len_str == 200:
                test_len_str = 100
                test_len_end = 200

            # 두께 그래프 테스트 용
            if test_thick_len[0] == 100:
                test_thick_len = [200, 220, 240, 260, 280, 300]
                test_thick = [0.4, 0.3, 0.3, 0.2, 0.3, 0.5]
            elif test_thick_len[0] == 200:
                test_thick_len = [100, 120, 140, 160, 180, 200]
                test_thick = [0.3, 0.3, 0.4, 0.7, 0.6, 0.3]

            json_data = json.dumps({
                'test_img': test_img_file,
                'test_model': test_model_name,
                'test_len_str': test_len_str,
                'test_len_end': test_len_end,
                'test_graph': {'test_thick_len': test_thick_len,
                               'test_thick': test_thick}})

            print("test_img_num : " + str(test_img_file))
            sleep(3)
            yield f"data:{json_data}\n\n"

    return Response(test_raw_data(), mimetype='text/event-stream')


# 검사 항목 관리 CLASS (SELECT, INSERT, DELETE) --
class Data:
    def __init__(self):
        pass

    def checkData(self):
        db = pymysql.connect(host='localhost', user='root', db='metal_result', password='admin0808', charset='utf8')
        curs = db.cursor()

        sql = '''SELECT IFNULL(MAX(number),0) FROM test_table WHERE date = %s'''
        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d')
        curs.execute(sql, date)
        rows = curs.fetchall()

        number_latest = rows[0][0]

        db.commit()
        db.close()

        return number_latest

    # 조회
    def selectData(self):
        db = pymysql.connect(host='localhost', user='root', db='metal_result', password='admin0808', charset='utf8')
        curs = db.cursor()

        sql = '''SELECT number, model_name FROM test_table WHERE date = %s'''
        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d')
        curs.execute(sql, date)
        rows = curs.fetchall()
        ret = []

        for e in rows:
            temp = {'number': e[0], 'model': e[1]}
            ret.append(temp)

        db.commit()
        db.close()
        return ret

    # 초기화
    def deleteItem(self):
        db = pymysql.connect(host='localhost', user='root', db='metal_result', password='admin0808', charset='utf8')
        curs = db.cursor()

        # sql = "DELETE FROM test_table"
        sql = '''DELETE FROM test_table WHERE date = %s'''
        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d')
        curs.execute(sql, date)
        db.commit()
        db.close()

    # 추가
    def insertItem(self, num, model):
        db = pymysql.connect(host='localhost', user='root', db='metal_result', password='admin0808', charset='utf8')
        curs = db.cursor()

        sql = '''INSERT INTO test_table (number, model_name, date) VALUES (%s, %s, %s)'''
        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d')
        curs.execute(sql, (int(num), model, date))
        db.commit()
        db.close()


# 메인 페이지
@app.route('/dashboard')
@app.route('/')
def test():
    test_img = "image/test.png"
    last_Data = Data().checkData()
    now = datetime.datetime.now()
    date = now.strftime('%Y-%m-%d')
    if last_Data == 0:
        message = "[" + date + "] 설정된 검사항목이 존재하지 않습니다."
    else:
        message = "[" + date + "]"

    return render_template("main.html", img_name=test_img,  message=message)


# 항목 추가 페이지
@app.route('/insert')
def insert():
    last_Data = Data().checkData() + 1
    select_Data = Data().selectData()
    now = datetime.datetime.now()
    date = now.strftime('%Y-%m-%d')
    return render_template("insert.html", date=date, last_Data=last_Data, select_Data=select_Data)


# 항목 추가 페이지 추가Btn
@app.route('/insert_insert', methods=['POST'])
def insert_insert():
    number = request.form['value_number']
    model = request.form['value_model']
    Data().insertItem(number, model)
    last_Data = Data().checkData() + 1
    select_Data = Data().selectData()
    now = datetime.datetime.now()
    date = now.strftime('%Y-%m-%d')
    return render_template("insert.html", date=date, last_Data=last_Data, select_Data=select_Data)


# 항목 추가 페이지 초기화Btn
@app.route('/insert_delete')
def insert_delete():
    Data().deleteItem()
    last_Data = Data().checkData() + 1
    select_Data = Data().selectData()
    now = datetime.datetime.now()
    date = now.strftime('%Y-%m-%d')
    return render_template("insert.html", date=date, last_Data=last_Data, select_Data=select_Data)


@app.route('/live-data')
def live_data():
    data = [time() * 1000, random() * 100]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)