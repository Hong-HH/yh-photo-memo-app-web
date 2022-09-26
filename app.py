from flask import Flask, request, render_template, session,  redirect, url_for

# api 호출을 위한 requests 함수 
import requests

# 파일 업로드를 위한 임포트
from PIL import Image



from config import Config
from utils import login_api, main_api, memo_add_api



ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


app = Flask(__name__)

app.secret_key = Config.SESSION_SECRET

# 환경변수 셋팅
app.config.from_object(Config)
# 업로드 하는 파일의 최대 크기를 16 메가로 제한
# 그 이상의 파일을 업로드 한다면 RequestEntityTooLarge 예외 발생 (https://flask-docs-kr.readthedocs.io/ko/latest/patterns/fileuploads.html) 참고
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


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
        # memo_content = request.form['memo_content']
        memo_content = ""
        memo_content = str(memo_content)
        # form 태그에 enctype=multipart/form-data 속성이 없었을때는
        # myfile = request.form['myfile']
        # print(type(myfile)) --> str 임
        file = request.files['file']
        print(type(file)) # 결과 : <class 'werkzeug.datastructures.FileStorage'>
        


        if file and allowed_file(file.filename):
            # file = file.read()
            # print(type(file)) # 결과 : <class 'bytes'>
            img = Image.open(file)
            print(type(img))
            
            if title is None or len(title) < 1 :
                print("point 1")
                result = "제목은 필수로 기재해야하는 항목입니다! 제목을 채워주세요."
            else :
                print("point 2")
                if date is None or len(date) < 1 :
                    print("point 3")
                    result = "날짜를 선택해주세요!"
                else : 
                    print("point 4")
                    print(date)
                    print(type(date))
                    add_result = memo_add_api(title, date, file, memo_content)

                    if add_result['status'] == 200 :
                        result = "업로드 완료!"
                    else : 
                        result = "업로드 실패ㅜㅜ"

        else :
            # 허용되지 않은 파일이나, 파일이름이다.
            result = "허용되지 않은 파일 형식이나 파일이름입니다."

        return render_template('add.html', result = result)

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