"""jwt生成和解析 工具函数 命名为 mjwt 与 jwt 模块区分 """
import jwt
from datetime import timedelta, datetime, timezone
from core.config import settings

jwt_config = settings.api_auth
def gen_jwt(data: dict) -> str:
    """
    创建 jwt token 到期日期使用统一utc，其余参数在config.py中配置
    :param data:
    :return:
    """
    to_encode = data.copy()
    expires_delta = datetime.now(timezone.utc) + timedelta(minutes=jwt_config.expires_min)
    to_encode.update({"exp": int(expires_delta.timestamp())})
    return jwt.encode(to_encode, jwt_config.secret_key, algorithm=jwt_config.algorithm)


def parse_jwt(token: str) -> dict | None:
    """
    解析 jwt token
    :param token:
    :return: 失败或到期返回None
    """
    try:
        _payload = jwt.decode(token, jwt_config.secret_key, algorithms=[jwt_config.algorithm])
    except jwt.PyJWTError:
        return None
    else:
        exp = _payload["exp"]

        # 全部作为utc比较
        if datetime.now(timezone.utc) > datetime.fromtimestamp(exp, tz=timezone.utc):
            return None
    return _payload


def test_gen_jwt():
    data = {"username": "test", "password": "<PASSWORD>"}
    token = gen_jwt(data)
    return token


def test_parse_jwt(token: str):
    _payload = parse_jwt(token)
    print(_payload)


if __name__ == '__main__':
    t = test_gen_jwt()
    print(t)
    test_parse_jwt(t)

    utc_7 = timezone(timedelta(hours=8))
    print(datetime.now(utc_7))
