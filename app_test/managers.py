from django.db.models import manager
from config.modules.exceptions import CustomError, Error


class DumpModelManager(manager.Manager):
    def get_data_sort_by(self, category, data_date, order_by):
        if order_by not in ["price", "start_dtm", "end_dtm"]:
            raise CustomError(Error.INVALID_PARAMETER, order_by)

        return self.filter(category=category,
                           start_dtm__lte=data_date,
                           end_dtm__gte=data_date).order_by(order_by)
