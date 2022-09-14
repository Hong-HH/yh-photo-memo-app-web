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
            return render_template('login.html', result=login_result['message'])

    # method 가 get 일때
    else :
        print("login get")
        return render_template('login.html')

@app.route("/register")
def register():
    
    return "<p>Hello, This is register Page!</p>"


@app.route("/main")
def main():
    if 'access_token' in session:
        main_result = main_api()
        # API 호출 결과에 따른 페이지 이동 
        print('main api 호출 결과' + str(main_result['status']))

        if main_result['status'] == 200 :
            memo_list = main_result['list']
            memo_count = main_result['count']
            print('메모 갯수는 ' + str(memo_count))

        return  render_template('main.html', memo_list = memo_list)
    else : 
        return redirect(url_for('login'))



if __name__ == "__main__" :
    # 개발 끝나면 디버그 모드 풀기
    # app.debug = True
    app.run()
    # app.run(host='127.0.0.1',port=5001)
    # app.run(debug=True)
    # Flask.run(debug=True)

    # 현재 api 를 5000으로 웹을 5001로 돌리고 있음
    # flask run --port 5001