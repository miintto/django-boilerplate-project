# Boilerplate Project
확장 가능성 및 높은 코드 품질을 위한 초기 설정이 완료된 boilerplate 프로젝트 제작

# 1. Quick Start
## 1.1 Clone
~~~
$> git clone https://github.com/miintto/django-boilerplate-project.git
~~~

## 1.2 Install Libraries
~~~
$> pip install -r requirements.txt
~~~

## 1.3 Set Private Data
~~~
$> cd django-boilerplate-project
$> vi config/env/secrets.json

{
    "SECRET_KEY": "w3p_*mm=&uz3n3%i!&9$8oah^w09fy1i)fv8h1res4rfkflcd5",

    "DEFAULT_DATABASE": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "DBNAME",
        "USER": "USER",
        "PASSWORD": "PASSWORD",
        "HOST": "HOST",
        "PORT": "3306"
    }
}
~~~

## 1.4 Migration
~~~
$> python manage.py migrate
~~~

## 1.5 Run Server
~~~
$> python manage.py runserver
~~~

# 2. Details
## 2.1 구조
~~~
.
├─ config            # Config app
│   ├─ env             # 환경 변수 관리
│   ├─ modules         # 공통으로 사용하는 모듈
│   └─ settings        # 환경 설정 관리
├─ app_test          # 테스트용 sample app
│   ├─ migrations
│   └─ serializers
├─ logs              # 로그 저장
└─ manage.py
~~~

## 2.2 env 

Django 세팅과 관련되 환경 변수들을 관리하기 위해 사용.

- secret.json : Secret key 와 DB connection 정보와 같이 보안이 필요한 변수 관리.
  - .gitignore 파일에 추가하여 배포되지 않도록 주의가 필요함.
- config.py : secret.json 값을 읽어와서 dict 형식으로 바꾸는 모듈

## 2.3 modules
여러 app으로 확장시 공통적으로 사용하는 기능들을 한 번에 모아 관리.

### 2.3.1 exceptions.py
설계된 로직으로는 처리하기 힘들거나 작업 도중 예측하지 못한 에러가 발생하였을 때 상황별 적절하게 처리를 하기 위한 모듈

- CustomError class 를 이용하여 에러 발생.
- Error class 를 이용하여 예외 case 관리.
- 작업을 문제없이 완료한 경우 0번 코드를 내보낸다.
- 예외 상황은 1000번부터 시작하며, 필요한 경우 예외 상태 및 상태 코드를 추가할 수 있다.
- 나머지 염두하지 않은 에러는 999번으로 처리한다.

### 2.3.2 log.py
API 호출시 로그를 남겨 모니터링시 활용하기 위한 모듈

- API 당 로그를 3번씩 남김
  - IN : 넘겨 받은 input parameters
  - OUT : 내보내는 response
  - TOOK : 총 작업 시간

- 각 로그 데이터는 json 형태로 저장되며, 매일 자정마다 파일 분리 (TimedRotatingFileHandler 사용)

- Fields

 Name   | Type     | Description
 ------ | -------- | -----------
 time   | datetime | 발생시간 (YYYY-MM-DD"T"HH24:MI:SSSSSS)
 method | str      | API 메소드 (GET, POST, ...)
 path   | str      | API 경로
 tag    | str      | 구분 (IN, OUT, TOOK)
 level  | str      | 로그 레벨 (INFO, WARNING, ERROR, ...)
 ip     | str      | 사용자 접속 IP
 data   | object   | input parameters 혹은 response 데이터
 id     | int      | 호출한 API 의 pk (IN, OUT, TOOK 3개 짝을 맞춰보기 위한 key 값)
 took   | int      | 소요시간 (tag=TOOK 일 때만 출력)

- Sample
~~~
# IN
{
    "time": "2020-12-26T23:27:48.777486+09:00", 
    "method": "POST", 
    "path": "/test/dump", 
    "tag": "IN", 
    "level": "INFO", 
    "ip": "127.0.0.1", 
    "data": "{\"category\": \"테마파크\", \"order_by\": \"price\"}", 
    "id": 1608992868777
}

# OUT
{
    "time": "2020-12-26T23:27:48.827136+09:00", 
    "method": "POST", 
    "path": "/test/dump", 
    "tag": "OUT", 
    "level": "INFO", 
    "ip": "127.0.0.1", 
    "data": "{\"code\": 0, \"msg\": \"SUCCESS\", \"data\": [{\"contents_id\": 5, \"contents_name\": \"[서울 삼성] 코엑스 아쿠아리움\", ", 
    "id": 1608992868777
}

# TOOK
{
    "time": "2020-12-26T23:27:48.827136+09:00", 
    "method": "POST", 
    "path": "/test/dump", 
    "tag": "TOOK", 
    "level": "INFO", 
    "ip": "127.0.0.1", 
    "data": "50ms", 
    "id": 1608992868777, 
    "took": 50
}
~~~

### 2.3.3 response.py
status 200 일 시에 기본적인 response 형태를 잡아주기 위한 모듈로서 아래와 같이 정의한다.

#### 성공시
요구하는 작업을 에러 없이 완료한 경우.

 Name | Type   | Description
 ---- | ------ | -----------
 code | int    | 상태 코드 (성공: 0)
 msg  | str    | 상태 메시지 (성공: SUCCESS)
 data | object | 데이터

- Sample
~~~
{
    "code": 0,
    "msg": "SUCCESS",
    "data": {
        "contents_id": 4,
        "contents_name": "[에버랜드] X-MAS 축제 오픈",
        "region": "경기도 용인",
        "address": "경기도 용인시 처인구 포곡읍 ---",
        "category": "테마파크",
        "price": 15000,
        "start_dtm": "2020-12-01T09:00:00+09:00",
        "end_dtm": "2021-01-01T09:00:00+09:00",
        "register_dtm": "2020-12-26T18:04:02.567711+09:00"
    }
}
~~~

#### 예외 상태시
예측 가능한 예외 상황이 발생한 경우 그에 따른 알맞은 처리를 위해 여러 case 들을 정의.

 Name  | Type | Description
 ----- | ---- | -----------
 code  | int  | 예외 상태 코드 (예외: 1000 ~)
 error | str  | 예외 상태명
 msg   | str  | 상태 메시지 

- Sample
~~~
{
    "code": 1002,
    "error": "INVALID_PARAMETER"
    "msg": "[Error 1002] INVALID_PARAMETER: statr_date"
}
~~~

#### 에러시
정의해뒀던 예외 상태 이밖의 에러가 발생한 경우.

 Name  | Type | Description
 ----- | ---- | -----------
 code  | int  | 상태 코드 (에러: 999)
 error | str  | 에러 상태
 msg   | str  | 에러 메시지

- Sample
~~~
{
    "code": 999,
    "error": "ValueError"
    "msg": "too many values to unpack (expected 2)",
}
~~~

### 2.3.4 utils.py
공통으로 사용 가능한 기타 유용한 기능들 관리.

- ex.) 요청값에서 ip를 가져오는 함수를 정의하여 세션 관리시 혹은 logging 시에 사용가능

## 2.4 settings
개발 혹은 배포시 환경 설정을 별도로 관리.

- base, prod, dev로 나누어서 관리
  - base.py: 개발과 배포 환경에서 공통으로 사용되는 환경 변수 정의
  - dev.py: 개발시 로컬 환경에서 필요한 변수 관리
  - prod.py: 배포시 필요한 환경 변수 조정
  - 배포시에는 아래와 같이 prod 환경으로 실행
~~~
$> python manage.py runserver --settings=config.settings.prod
~~~

- router.py 에서 DB 라우터를 정의하여 필요에 따라 두 개 이상의 DB와 연결 가능하도록 설정

- LOGGING 변수를 dev, prod 로 나누어 관리하여 배포 환경에서 별도로 로그 파일이 쌓이는 경로 및 주기 변경 가능
