from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, func
from sqlalchemy.orm import declarative_base
from datetime import datetime
from service.encrypt import md5

Base = declarative_base()


class BaseModel(object):
    create_time = Column(DateTime, default=datetime.now(), comment='创建时间')
    update_time = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), comment='更新时间')

    def to_dict(self, exclude=[], reverse=True, time_=True):
        '''
        reverse=True: not in exclude：输出去除该列表里面的字段
        reverse=False: in exclude：输出只有该列表里面的字段
        '''
        if reverse:
            data = {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in exclude}
        else:
            if time_:
                exclude = exclude + ['create_time', 'update_time']
            data = {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name in exclude}

        if time_:
            data['create_time'] = data['create_time'].strftime('%Y-%m-%d %H:%M:%S') if data['create_time'] else ''
            data['update_time'] = data['update_time'].strftime('%Y-%m-%d %H:%M:%S') if data['update_time'] else ''

        return data


class Test(Base):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True)
    user = Column(String(255), comment='操作者')
    msg = Column(Text, comment='信息')
    sort = Column(Integer, comment='顺序')


class Department(Base, BaseModel):
    '''部门'''
    __tablename__ = 'ums_department'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), comment='部门名称')
    leader = Column(String(50), comment='负责人')
    pid = Column(Integer, comment='上级部门ID')
    is_deleted = Column(Boolean, default=False, comment='是否删除 0-未删除 1-已删除')

    def json(self):
        data = self.to_dict()
        data['children'] = []
        return data

    def json_department_tree(self):
        return {
            "id": self.id,
            "title": self.name,
            "pid": self.pid,
            "spread": True,
            "children": [],
        }

    def json_tree(self):
        return {
            "id": self.id,
            "name": self.name,
            "pid": self.pid,
        }


class Log(Base, BaseModel):
    '''日志'''
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True)
    user = Column(String(255), nullable=True, comment='操作者')
    action = Column(String(50), nullable=True, comment='操作类型 CREATE/UPDATE/DELETE')
    model_name = Column(String(255), nullable=True, comment='操作的哪张表')
    object_id = Column(String(255), nullable=True, comment='被操作对象的id')
    object_repr = Column(String(255), nullable=True, comment='被操作对象的表示')
    url = Column(String(255), nullable=True, comment='当前访问的路径/接口')
    browser = Column(String(255), nullable=True, comment='浏览器类型')
    ip_address = Column(String(39), nullable=True, comment='IP地址')
    status = Column(String(50), comment='http请求状态码 - (成功200/服务器错误500)')
    message = Column(Text, nullable=True, comment='500的错误信息')

    def json(self):
        return self.to_dict()


class Rights(Base, BaseModel):
    '''权限'''
    __tablename__ = 'ums_rights'
    id = Column(Integer, primary_key=True)
    title = Column(String(20), comment='权限名称')
    code = Column(String(30), nullable=True, comment='权限标识')
    kind = Column(String(30), comment='权限类型')
    url = Column(String(50), nullable=True, comment='路径地址')
    icon_sign = Column(String(128), nullable=True, comment='图标')
    is_enabled = Column(Boolean, default=True, comment='权限是否可用 0-禁止 1-可用')
    sort = Column(Integer, default=0, comment='显示排序')
    open_type = Column(String(128), nullable=True, default='_iframe', comment='打开方式')
    remark = Column(String(255), nullable=True, comment='备注')
    pid = Column(Integer, nullable=True, comment='父权限ID')
    is_deleted = Column(Boolean, default=False, comment='是否删除 0-未删除 1-已删除')

    def menu_json(self):
        type_map_dict = {"menu": 0, "menu-z": 1, "menu-bug": 2}
        return {
            "id": self.id,
            "pid": self.pid if self.pid is not None else 0,
            "title": self.title,
            "type": type_map_dict[self.kind],
            "href": self.url,
            "icon": self.icon_sign,
            "sort": self.sort,
            "openType": self.open_type or "_iframe",
            "remark": self.remark
        }

    def json(self):
        data = self.to_dict()
        data['name'] = self.title  # 特殊处理name字段
        data['children'] = []
        return data

    def json_tree(self):
        return {
            "id": self.id,
            "name": self.title,
            "pid": self.pid,
        }

    def json_power_tree(self):
        return {
            "id": self.id,
            "title": self.title,
            "pid": self.pid,
            "sort": self.sort,
            "spread": True,
            "children": [],
        }


class Role(Base, BaseModel):
    '''角色'''
    __tablename__ = 'ums_role'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), comment='角色名称')
    code = Column(String(20), comment='角色标识符')
    desc = Column(Text, nullable=True, comment='角色描述')
    is_enabled = Column(Boolean, default=True, comment='角色是否可用 0-禁用 1-可用')
    rights_ids = Column(String(512), nullable=True, comment='权限ids,1,2,5')
    is_deleted = Column(Boolean, default=False, comment='是否删除 0-未删除 1-已删除')

    def json(self):
        return self.to_dict()


class User(Base, BaseModel):
    '''角色'''
    __tablename__ = 'ums_user'
    id = Column(Integer, primary_key=True)
    nickname = Column(String(128), comment='昵称')
    username = Column(String(128), comment='用户名')
    password_hash = Column(String(255), comment='登录密码')
    mobile = Column(String(11), comment='手机')
    email = Column(String(64), comment='邮箱')
    avatar = Column(Text, nullable=True, comment='头像地址')
    postion = Column(String(64), comment='职位')
    gender = Column(Integer, default=3, comment='性别')
    is_enabled = Column(Boolean, default=True, comment='账号是否可用 0-禁用 1-可用')
    department_id = Column(Integer, nullable=True, comment='部门ID')
    is_super = Column(Boolean, default=False, comment='是否是超级管理员')
    sign = Column(String(255), nullable=True, comment='个性签名')
    role_ids = Column(String(512), nullable=True, comment='角色ids,1,2,5')
    is_deleted = Column(Boolean, default=False, comment='是否删除 0-未删除 1-已删除')

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = md5(password)

    def json(self):
        return self.to_dict()