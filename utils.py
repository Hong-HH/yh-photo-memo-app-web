import requests
from config import Config
from flask import session

def login_api(email, password):
    url = Config.END_POINT + "v1/user/login"
    print(url)
    login_req = { "email": email,  "password" :password  }

    login_result  = requests.post(url, json = login_req )
    login_result = login_result.json()

    if login_result['status'] == 200 :
        # 로그인이 성공했다면
        # 1. 엑세스 토큰을 쿠키에 저장하기
        session['access_token'] = login_result['message']

        return login_result

    else :
        return login_result

