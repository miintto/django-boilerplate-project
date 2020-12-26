from config.modules.exceptions import CustomError, Error
from config.modules.response import send_format
from config.modules.utils import get_date_now
from app_test.models import DumpModel
from app_test.serializers.model_serializers import DumpModelSerializer


class TestGetSevice:
    def __init__(self, params):
        self.contents_id = params.get("contents_id")
        self.result = dict()

    def _get_data(self):
        try:
            query_set = DumpModel.objects.get(contents_id=self.contents_id)
        except:
            raise CustomError(Error.NO_DATA, self.contents_id)
        serializer = DumpModelSerializer(query_set)
        self.result = serializer.data

    @send_format
    def run(self):
        self._get_data()
        return self.result


class TestPostService:
    def  __init__(self, params):
        self.order_by = params.get("order_by")
        self.category = params.get("category")
        self.result = dict()

    def _set_default_date(self):
        self.data_date = get_date_now()

    def _get_data(self):
        query_set = DumpModel.objects.get_data_sort_by(self.category, self.data_date, self.order_by)
        if len(query_set)==0:
            raise CustomError(Error.NO_DATA)
        serializer = DumpModelSerializer(query_set, many=True)
        self.result = serializer.data

    @send_format
    def run(self):
        self._set_default_date()
        self._get_data()
        return self.result
