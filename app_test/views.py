from rest_framework.views import APIView
from rest_framework.response import Response
from app_test.serializers import validators
from app_test import services
from django.utils import *

from config.modules.log import Log
import logging
logger = logging.getLogger(__name__)


class TestSampleView(APIView):
    def get(self, request):
        params = validators.ContentIdxSerializer(data=request.query_params)

        log = Log(logger, request)
        log.input(params.initial_data)

        if not params.is_valid():
            log.output(params.errors)
            return Response(params.errors, status=400)

        service = services.TestGetSevice(params.validated_data)
        res = service.run()
        log.output(res)
        return Response(res)


    def post(self, request):
        params = validators.ContentsListSerializer(data=request.data)

        log = Log(logger, request)
        log.input(params.initial_data)

        if not params.is_valid():
            log.output(params.errors)
            return Response(params.errors, status=400)

        service = services.TestPostService(params.validated_data)
        res = service.run()
        log.output(res)
        return Response(res)
