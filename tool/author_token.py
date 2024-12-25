import re
import jwt
import json
import datetime
from config.env import JWT_KEY
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    secret = JWT_KEY
    # secret = '176100855585'

    # 密码加密
    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    # 密码校验
    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    # token生成
    def encode_token(self, user_id, minutes=10080):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=minutes), # 超时时间
            # 'exp': datetime.utcnow() + timedelta(days=0, minutes=1), # 超时时间
            'iat': datetime.utcnow(),
            'sub': user_id  # 自定义用户ID
        }
        return str(jwt.encode(payload, self.secret, algorithm='HS256'))

    # token 解码
    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return {'code':200, 'user_id':payload['sub']}
        except jwt.ExpiredSignatureError:
            # raise HTTPException(status_code=400, detail='Token已经超期，请重新登录！')
            return {'code': 400, 'message': 'Token超期，请重新登录！'}
        except jwt.InvalidTokenError as e:
            # raise HTTPException(status_code=400, detail='非法的token！请重新登陆!')
            return {'code': 400, 'message': '非法的token！'}

    def auth_wrapper(self, oauth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(oauth.credentials)

    def check_re(self, data, type):
        """正则表达式数据校验"""
        type_dict = {
            'email': r'\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}',
            'url': r'^((https|http|ftp|rtsp|mms)?:\/\/)[^\s]+',
            'phone': r'^1(3|4|5|7|8|9)[0-9]{9}',
            'id_card': r'^\d{17}[\d|x]|\d{15}',
            'ip': r'^(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)'
        }
        if type_dict[type]:
            res = re.search(type_dict[type], data)
            if res:
                return res.group(0)
        return None

    def check_space(self, data):
        '''检查密码虹是否含有空格'''
        return ' ' not in data


permissions = AuthHandler()
