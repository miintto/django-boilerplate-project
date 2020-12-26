from datetime import datetime
from pytz import timezone

tz = timezone("Asia/Seoul")


def get_client_ip(request):
    """
    request 내부의 값으로 유저의 IP 주소 체크
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_date_now():
    """
    현재 일시 반환
    """
    return datetime.now(tz=tz)
