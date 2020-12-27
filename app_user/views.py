from rest_framework.views import APIView
from rest_framework.response import Response

from app_user.serializers import *
from .models import User, UserProfile
from django.utils import *
import time


# def findUser(id):
#   # TODO: 조만간 작업 예정.
# 	User.object.
def getCurrentTimestamp():
    return time.time()

class UserView(APIView):

    def get(self, request):
        id = request.query_params["user_id"]
        user = User.objects.get(pk=id)

        return Response(UserSerializer(user).data)

    def post(self, request):
        body = request.data
        body['joined_at'] = getCurrentTimestamp()
        serializer = UserSerializer(data=body)
        user = serializer.save()

        return Response(serializer.data)

    def patch(self, request):
        body = request.data
        user = User.objects.get(pk=body["id"])
        body['updated_at'] = getCurrentTimestamp()
        serializer = UserSerializer(user, data=body)
        user = serializer.save()

        return Response(serializer.data)

    def delete(self, request, user_id):
        if user_id is None:
            return Response('삭제불가')
        user = User.objects.get(pk=user_id)
        if user.type == "일반":  # 일반 사용자라면 기본조건만 확인 후 삭제해준다
            if len(user.orders) > 1:
                for order in user.orders:
                    if order.usable == True:
                        return Response("삭제불가")
                    else:
                        pass
            else:
                if order.usable == True:
                    return Response("삭제불가")
                else:
                    pass

            if user.joined_at < 1600308400:
                return Response("삭제불가")
            user.delete()
            return Response("삭제완료")

        elif user.type == '프리미엄':  # 프리미엄 사용자는 특정상품구매 내역이 있다면 삭제할 수 없다.
            if len(user.orders) > 1:
                for order in user.orders:
                    if order.usable == True:
                        return Response("삭제불가")
                    else:
                        # TODO:
                        pass
            else:
                if order.usable == True:
                    return Response("삭제불가")
                else:
                    pass

            if user.joined_at < 1600308400:
                return Response("삭제불가")

            for order in user.orders:
                if order.product.category == "프리미엄ONLY":
                    return Response("삭제불가")

            user.delete()
            return Response("삭제완료")

        return Response("삭제불가")
