from flask import Flask, request



from config import Config


app = Flask(__name__)

# 환경변수 셋팅
app.config.from_object(Config)



# 페이지 경로 설정 
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/login")
def login():
    
    return "<p>Hello, This is Login Page!</p>"


if __name__ == "__main__" :
    app.run()