import json

class LogRecord:
    def __init__(self, environment, log_name, date_time, msg, log_level, module, func_name, correlation_id):
        self.env = environment
        self.name = log_name
        self.dt = date_time
        self.message = msg
        self.level = log_level
        self.module = module
        self.func_name = func_name
        self.id = correlation_id

    def __str__(self):
        return json.dumps({
            'environment': self.env,
            'loggerName': self.name,
            'logLevel': self.level,
            'dateTime': self.dt,
            'module': self.module,
            'functionName': self.func_name,
            'message': self.message,
            'correlationId': self.id
        })