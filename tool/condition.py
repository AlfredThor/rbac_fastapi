from sqlalchemy import Integer, String, func


class Condition:
    '''
        如果数据表中有Integet字段,将其转换为String字段,主要针对postgres数据库
    '''
    def __init__(self, model):
        self.model = model

    def process_condition(self, attr, value):
        if isinstance(value, str):
            return getattr(self.model, attr).ilike(f"%{value}%")
        elif isinstance(value, int) and isinstance(getattr(self.model, attr).type, Integer):
            return func.cast(getattr(self.model, attr), String).ilike(f"%{str(value)}%")
        else:
            return getattr(self.model, attr) == value