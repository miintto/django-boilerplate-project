from config.modules.exceptions import Error
from config.modules.utils import get_client_ip
import json
from datetime import datetime
import time
import pytz

tz = pytz.timezone('Asia/Seoul')


class Log:
    def __init__(self, logger, request):
        self.logger = logger
        self.method = request.method
        self.path = request.path
        self.ip = get_client_ip(request)
        self.created_time = int(round(time.time() * 1000))


    def input(self, data: dict):
        level = "INFO"
        data = self.json_dumps(data)
        self.write(level, "IN", data)


    def invalid(self, data: dict):
        level = "ERROR"
        data = self.json_dumps(data)
        self.write(level, "OUT", data)


    def output(self, data: dict):
        try:
            code = data.get("code")
            if code == Error.SUCCESS.value:
                level = "INFO"
            else:
                level = "ERROR"
            data = self.json_dumps(data)
            self.write(level, "OUT", data)
            self.took()

        except Exception as e:
            self.write("WARNING", "OUT", str(e))
            self.took()


    def took(self):
        level = "INFO"
        now = int(round(time.time() * 1000))
        time_interval = now - self.created_time
        self.write(level, "TOOK", f"{time_interval}ms", time_interval)


    def write(self, level: str, tag: str, data: str, time_interval=None):
        log_data = {
            "time": datetime.now(tz).isoformat(),
            "method": self.method,
            "path": self.path,
            "tag": tag,
            "level": level,
            "ip": self.ip,
            "data": data,
            "id": self.created_time
        }
        if time_interval is not None:
            log_data.update({"took": time_interval})

        self.logger.info(self.json_dumps(log_data))


    def json_dumps(self, json_data: dict) -> str:
        try:
            json_dump_result = json.dumps(json_data, ensure_ascii=False)
        except Exception as e:
            json_dump_result = f"FAIL TO DUMP JSON: {e}"
        return json_dump_result
