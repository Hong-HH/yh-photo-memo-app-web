from flask import Flask, request, render_template, session,  redirect, url_for

# api 호출을 위한 requests 함수 
import requests


from config import Config
from utils import login_api


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
    return "<p>Hello,  This is  main pahge</p>"



if __name__ == "__main__" :
    # 개발 끝나면 디버그 모드 풀기
    # app.debug = True
    app.run()
    # app.run(host='127.0.0.1',port=5001)
    # app.run(debug=True)
    # Flask.run(debug=True)

    # 현재 api 를 5000으로 웹을 5001로 돌리고 있음
    # flask run --port 5001