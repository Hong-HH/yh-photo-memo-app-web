from flask import Flask, request, render_template

# api 호출을 위한 requests 함수 
import requests


from config import Config


app = Flask(__name__)

# 환경변수 셋팅
app.config.from_object(Config)



# 페이지 경로 설정 
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/login" , methods=['POST','GET'])
def login():

    if request.method =='POST':
        email = request.form['email']
        password= request.form['password']
        return "posted"

    
    # method 가 get 일때
    else :
        return render_template('login.html')

@app.route("/register")
def register():
    
    return "<p>Hello, This is register Page!</p>"



if __name__ == "__main__" :
    app.run()
    # 개발 끝나면 디버그 모드 풀기
    # app.run(debug=True)
    # Flask.run(debug=True)