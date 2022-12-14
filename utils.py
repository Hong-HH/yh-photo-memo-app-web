from unittest import result
import requests
from config import Config
from flask import session
# 실행시간 체크를 위한 구문
from time import time



def login_api(email, password):
    url = Config.END_POINT + "v1/user/login"
    print(url)
    login_req = { "email": email,  "password" :password  }

    # api 실행시간 체크를 위한 구문
    begin = time()

    login_result  = requests.post(url, json = login_req )

    # api 실행시간 체크를 위한 구문
    end = time()
    print('실행 시간: {0:.3f}초'.format(end - begin))


    login_result = login_result.json()

    if login_result['status'] == 200 :
        # 로그인이 성공했다면
        # 1. 엑세스 토큰을 쿠키에 저장하기
        session['access_token'] = login_result['message']

        return login_result

    else :
        return login_result


def main_api():
    # 세션에서 access_token 가져오기
    access_token = session['access_token']
    # 메모 리스트 가져오는 api url 
    url = Config.END_POINT +  'v1/memo'
    print(url)
    # 헤더에 엑세스 토큰 정보 담기
    headers={'Authorization':'Bearer '+access_token}
    params =  {"offset": 0, "limit": 30 }

    # api 실행시간 체크를 위한 구문
    begin = time()

    # api 호출 (.json 으로 Response 객체 json으로 받기)
    main_result = requests.get(url,headers=headers, params=params).json()

    # api 실행시간 체크를 위한 구문
    end = time()
    print('실행 시간: {0:.3f}초'.format(end - begin))




    ################ 2번째 api 호출 ################################################
    # 메모 갯수 가져오는 api url 
    url = Config.END_POINT +  'v1/memo/count'
    print(url)
    # 헤더에 엑세스 토큰 정보 담기
    headers={'Authorization':'Bearer '+access_token}

    # api 실행시간 체크를 위한 구문
    begin = time()

    # api 호출 (.json 으로 Response 객체 json으로 받기)
    count_result = requests.get(url,headers=headers).json()

    # api 실행시간 체크를 위한 구문
    end = time()
    print('실행 시간: {0:.3f}초'.format(end - begin))


    
    return main_result, count_result




def memo_add_api(title_1, date_1, file_1, content_1) :
    title =title_1 
    date = date_1 
    file = file_1
    content = content_1
    if content is None :
        content = ""
    

    print(type(content))
    print("" + str(type(date)) + str(date))

    # 세션에서 access_token 가져오기
    access_token = session['access_token']

    # 메모를 추가하는 api
    url = Config.END_POINT +  'v1/memo'
    print(url)

    # 헤더에 엑세스 토큰 정보 담기
    headers={'Authorization':'Bearer '+access_token}

    # api 실행시간 체크를 위한 구문
    begin = time()

    # api 호출 (.json 으로 Response 객체 json으로 받기) files 의 photo 의 두번째 파라미터인 파일은 file, file.read() 둘다 된다.
    add_result = requests.post(url,headers=headers,files={'photo' : (file.filename, file, file.content_type )}, data= {'title' : title, 'date' : date, 'content' : content}).json()

    # api 실행시간 체크를 위한 구문
    end = time()
    print('실행 시간: {0:.3f}초'.format(end - begin))

    print(add_result)


    
    return add_result
