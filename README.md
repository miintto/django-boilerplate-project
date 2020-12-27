# Boilerplate Project
확장성 및 높은 코드 품질을 위한 초기 설정이 완료된 boilerplate 프로젝트 제작

# 1. Quick Start
## 1.1 Clone
~~~bash
$> git clone https://github.com/miintto/django-boilerplate-project.git
~~~

## 1.2 Install Libraries
~~~bash
$> cd django-boilerplate-project
$> pip install -r requirements.txt
~~~

## 1.3 Set Private Data
~~~bash
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
- 모델 migrate
~~~bash
$> python manage.py migrate
~~~
- 샘플 데이터 업로드
~~~bash
$> python manage.py loaddata dumps.json
~~~

## 1.5 Run Server
~~~bash
$> python manage.py runserver
~~~

# 2. Descriptions
## 2.1 구조
~~~bash
.
├─ config            # Config app
│   ├─ env             # 보안이 필요한 변수 관리
│   ├─ modules         # 공통으로 사용하는 모듈
│   └─ settings        # 환경 설정 관리
├─ app_test          # 테스트용 sample app
│   ├─ migrations
│   └─ serializers
├─ logs              # 로그 저장
└─ manage.py
~~~

## 2.2 Env 
기본 setting 값 이외에 사용자가 별도로 설정하는 환경 변수들을 관리하기 위해 사용

- secret.json : Secret key 와 DB connection 정보와 같이 보안이 필요한 변수 관리
  - .gitignore 파일에 추가하여 배포되지 않도록 주의가 필요함
  - git 으로 관리되지 않으므로 로컬 환경과 배포 환경 개별적으로 설정해두어야 함
- config.py : secret.json 값을 읽어와서 dict 형식으로 바꾸는 모듈

## 2.3 Modules
여러 app으로 확장시 공통적으로 사용하는 기능들을 한 번에 모아 관리

### 2.3.1 exceptions.py
설계된 로직으로는 처리하기 힘들거나 작업 도중 예측하지 못한 에러가 발생하였을 때 상황별 적절하게 처리를 하기 위한 모듈

- CustomError class 를 이용하여 에러 발생.
- Error class 를 이용하여 예외 case 관리.
  - 작업을 문제없이 완료한 경우 0번 코드를 내보낸다.
  - 예외 상태 코드는 1000번부터 시작하며, 필요한 경우 예외 상태 및 상태 코드를 추가할 수 있다.
  - 나머지 염두하지 않은 에러는 999번으로 처리한다.

### 2.3.2 log.py
API 호출시 로그를 남겨 모니터링으로 활용하기 위한 모듈

- API 당 로그를 3번씩 남김
  - IN : 넘겨 받은 input parameters
  - OUT : 내보내는 response
  - TOOK : 총 작업 시간

- 로그 데이터는 json 형식으로 저장하여 각 필드별로 관찰 가능하도록 한다.

- 매일 자정마다 파일 분리 (TimedRotatingFileHandler 사용)

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
~~~bash
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
    "data": "{\"code\": 0, \"msg\": \"SUCCESS\", \"data\": [{\"contents_id\": 5, \"contents_name\": \"[서울 삼성] ...", 
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
status 200 일 시에 기본적인 response 형태를 잡아주기 위한 모듈

- 해당 기능을 send_format 함수로 구현하여 decorator 로 활용 가능

#### 성공시
요구하는 작업을 에러 없이 완료한 경우

 Name | Type   | Description
 ---- | ------ | -----------
 code | int    | 상태 코드 (성공: 0)
 msg  | str    | 상태 메시지 (성공: SUCCESS)
 data | object | 데이터

- Sample
~~~bash
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
예측 가능한 예외 상황이 발생한 경우 그에 따른 알맞은 처리를 위해 여러 case 들을 정의

 Name  | Type | Description
 ----- | ---- | -----------
 code  | int  | 예외 상태 코드 (예외: 1000 ~)
 error | str  | 예외 상태명
 msg   | str  | 상태 메시지 

- Sample
~~~bash
{
    "code": 1002,
    "error": "INVALID_PARAMETER"
    "msg": "[Error 1002] INVALID_PARAMETER: statr_date"
}
~~~

#### 에러시
정의해뒀던 예외 이밖의 에러가 발생한 경우

 Name  | Type | Description
 ----- | ---- | -----------
 code  | int  | 상태 코드 (에러: 999)
 error | str  | 에러 상태
 msg   | str  | 에러 메시지

- Sample
~~~bash
{
    "code": 999,
    "error": "ValueError"
    "msg": "too many values to unpack (expected 2)",
}
~~~

### 2.3.4 utils.py
공통으로 사용 가능한 기타 유용한 기능들 관리

- ex.) 요청값에서 ip를 가져오는 함수를 정의하여 세션 관리시 혹은 logging 시에 사용가능

## 2.4 Settings
개발 혹은 배포시 필요한 설정 값들을 별도로 관리

- base, dev, prod 로 나누어서 관리
  - base.py: 개발과 배포 환경에서 공통으로 사용되는 환경 변수 정의
  - dev.py: 개발시 로컬 환경에서 필요한 변수 관리
  - prod.py: 배포시 필요한 환경 변수 조정
  - 배포 환경에는 아래와 같이 prod 설정값 으로 실행
~~~bash
$> python manage.py runserver --settings=config.settings.prod
~~~

- Test app은 개발 환경에서만 작동하도록 dev 에 설정

- router.py 에서 DB 라우터를 정의하여 필요에 따라 두 개 이상의 DB와 연결 가능하도록 설정

- LOGGING 변수를 dev, prod 로 나누어 관리하여 배포 환경에서 별도로 로그 파일이 쌓이는 경로 및 주기 변경 가능

## 2.5 App 구성
### 2.5.1 구조
~~~bash
.
├─ migrations
├─ serializers
│   ├─ model_serializers.py
│   └─ validators.py
├─ admin.py
├─ app.py
├─ managers.py
├─ models.py
├─ services.py
├─ tests.py
├─ urls.py
└─ views.py
~~~

### 2.5.2 Details
- Views 는 전체적인 API 작업을 컨트롤하는 역할
  - input parameters 유효성 검사
  - logging

- Models 에서 데이터 객체 관리
  - Model 각각의 개별적인 로직은 연결된 managers 에서 정의

- Services 에서 복합적인 로직 통합적으로 관리
  - 비즈니스 로직 처리
  - 예외 처리 및 response 형태 관리

- Serializer 는 역할에 따라 나누어 관리
  - model_serializers: Models 객체를 직렬화하는 역할
  - validators: 요청값으로 받은 parameters 의 유효성 검사

# 3. Sample API
## 3.1 정상적인 결과
- Case 1.
~~~bash
GET /test/sample?contents_id=2
~~~
~~~bash
HTTP 200 OK
{
    "code": 0,
    "msg": "SUCCESS",
    "data": {
        "contents_id": 2,
        "contents_name": "[제주] 제주KAL호텔 특가",
        "region": "제주",
        "address": "제주특별자치도 제주시 주르레길 ...",
        "category": "숙박",
        "price": 78000,
        "start_dtm": "2020-12-23T09:00:00+09:00",
        "end_dtm": "2021-03-23T09:00:00+09:00",
        "register_dtm": "2020-12-28T03:12:29+09:00"
    }
}
~~~

- Case 2.
~~~bash
POST /test/sample
{
    "category": "테마파크", 
    "order_by": "price"
}
~~~
~~~bash
HTTP 200 OK
{
    "code": 0,
    "msg": "SUCCESS",
    "data": [
        {
            "contents_id": 3,
            "contents_name": "[경기] 양지파인 스노우파크 눈썰매",
            "region": "경기도 용인",
            "address": "경기도 용인시 처인구 양지면 ...",
            "category": "테마파크",
            "price": 11000,
            "start_dtm": "2020-12-23T09:00:00+09:00",
            "end_dtm": "2021-03-23T09:00:00+09:00",
            "register_dtm": "2020-12-28T03:12:29+09:00"
        },

        ...

    ]
}
~~~
## 3.2 예외 케이스
- 잘못된 input parameter
~~~bash
GET /test/sample?id=2
~~~
~~~bash
HTTP 400 Bad Request
{
    "contents_id": [
        "This field is required."
    ]
}
~~~
- 범위 밖의 input 값
~~~bash
GET /test/sample?contents_id=-1
~~~
~~~bash
HTTP 200 OK
{
    "code": 1000,
    "error": "NO_DATA",
    "msg": "[Error 1000] NO_DATA: -1"
}
~~~
~~~bash
POST /test/sample
{
    "category": "숙박", 
    "order_by": "srart_dtm"
}
~~~
~~~bash
HTTP 200 OK
{
    "code": 1001,
    "error": "INVALID_PARAMETER",
    "msg": "[Error 1001] INVALID_PARAMETER: srart_dtm"
}
~~~
