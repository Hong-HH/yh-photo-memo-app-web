from flask import Flask, request, render_template, session,  redirect, url_for

# api 호출을 위한 requests 함수 
import requests


from config import Config
from utils import login_api, main_api


app = Flask(__name__)

app.secret_key = Config.SESSION_SECRET

# 환경변수 셋팅
app.config.from_object(Config)



# 페이지 경로 설정 

# 루트는 나중에 소개페이지로 바꿀것
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/login" , methods=['POST','GET'])
def login():

    if request.method =='POST':
        print("login post")
        email = request.form['email']
        password= request.form['password']

        login_result = login_api(email, password)
        if login_result['status'] == 200 :
            return redirect(url_for('main'))

        else :
            print(login_result['message'])
            return render_template('login.html', result=login_result['message'])

    # method 가 get 일때
    else :
        print("login get")
        return render_template('login.html')

@app.route("/register")
def register():
    
    return "<p>Hello, This is register Page!</p>"


@app.route("/main" )
def main():

    if 'access_token' in session:
        main_result, count_result = main_api()
        # API 호출 결과에 따른 페이지 이동 
        print('main api 호출 결과' + str(main_result['status']))

        if main_result['status'] == 200 :

            total_count = count_result['message'][0]['total']
            page_count = int(total_count/30) + 1

            print("총 메모의 갯수는 :  " + str(total_count))
            print("총 페이지의 갯수는 : " + str(page_count))
            
            

            memo_list = main_result['list']
            memo_count = main_result['count']
            print('메모 갯수는 ' + str(memo_count))

            return  render_template('memo_list.html', memo_list = memo_list, page_list = range(1, page_count +1))
        else :
            # API 호출에 문제가 생겼다면 로그인으로 
            # TODO 나중에 로그인 만료인지 , 이미 로그아웃한 (REVOKED) 토큰인지 체크하기
            if  main_result['status'] == 401 :
                print(main_result['message'])
            return redirect(url_for('login'))

    else : 
        #  엑세스 토큰이 없다면 로그인 페이지로
        return redirect(url_for('login'))


@app.route("/add" , methods=['POST','GET'])
def add():

    if request.method =='POST':
        title = request.form['title']
        date = request.form['date']
        myfile = request.form['myfile']
        # print(type(myfile)) --> str 임
        return render_template('add.html')

    else :
        return render_template('add.html')





if __name__ == "__main__" :
    # 개발 끝나면 디버그 모드 풀기
    # app.debug = True
    app.run()
    # app.run(host='127.0.0.1',port=5001)
    # app.run(debug=True)
    # Flask.run(debug=True)

    # 현재 api 를 5000으로 웹을 5001로 돌리고 있음
    # set FLASK_ENV=development
    # flask run --port 5001