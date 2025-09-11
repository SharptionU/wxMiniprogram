from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PostgresDsn, MongoDsn
from typing import List, Dict, Optional, Literal
import os
from pathlib import Path


# 1. 嵌套配置模型（对应字典中的子结构）
class UvicornConfig(BaseSettings):
    """Uvicorn 服务器配置"""
    app: str = "main:app"
    host: str = "0.0.0.0"
    port: int = 5000
    reload: bool = True
    reload_dirs: List[str] = ["./"]
    reload_includes: List[str] = ["*.py", "*.html", "*.css", "*.js"]
    reload_excludes: List[str] = ["*.pyc", "*.pyo", "*.swp"]
    log_level: Literal["debug", "info", "warning", "error"] = "info"
    workers: int = 4


class PasswordConfig(BaseSettings):
    """密码加密策略配置"""
    algorithm: str = "argon2id"
    time_cost: int = 2
    memory_cost: int = 65536
    parallelism: int = 4
    hash_len: int = 32
    salt_len: int = 16


class ApiAuthConfig(BaseSettings):
    """API 认证配置（JWT 等）"""
    secret_key: str = ""  # 从环境变量获取
    algorithm: str = "HS256"
    expires_min: int = 60 * 24 * 7  # 7天
    expires_refresh_max: int = 60 * 24 * 7


class MongoDBConfig(BaseSettings):
    """MongoDB 数据库配置"""
    db_uri: MongoDsn ="mongodb://localhost:27017"
    db_name: str = "mall"
    db_user: str = ""
    db_pass: str = ""  # 敏感信息从环境变量获取
    tls_ssl: bool = False
    primary: str = ""
    secondary: str = ""


class MySQLConfig(BaseSettings):
    """MySQL 数据库配置（示例）"""
    db_uri: str = "mysql+pymysql://user:pass@localhost:3306/mall"
    db_name: str = "mall"
    db_user: Optional[str] = ""
    db_pass: Optional[str] = ""


class RedisConfig(BaseSettings):
    """Redis 配置"""
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password:str  = ""



class BusinessConfig(BaseSettings):
    """业务相关配置"""
    payment_code: Dict[str, str] = {
        "wechat": "11",
        "alipay": "12",
        "card": "13",
        "cash": "14",
        "cancel": "00",
        "refund": "01",
    }


class LanguageConfig(BaseSettings):
    """国际化配置"""
    default: str = "zh_CN"
    support: List[str] = ["zh_CN", "en_US"]
    tool: str = "gettext"
    domain: str = "messages"
    path: Path = Path(os.path.join(os.path.dirname(__file__), "locale"))


class DefaultConfig(BaseSettings):
    """默认值配置"""
    avatar: str = "/static/avatar/__default__.png"


# 2. 主配置模型（聚合所有子配置）
class Settings(BaseSettings):
    """全局配置主模型"""

    name:str="山语户外"
    version: str = "1.0"
    api_prefix: str = "/api/v1"

    environment: Literal["dev", "prod"] = "dev"

    # 嵌套子配置
    uvicorn: UvicornConfig = UvicornConfig()
    password: PasswordConfig = PasswordConfig()
    api_auth: ApiAuthConfig = ApiAuthConfig()
    mongo: MongoDBConfig = MongoDBConfig()
    mysql: MySQLConfig = MySQLConfig()
    redis: RedisConfig = RedisConfig()
    business: BusinessConfig = BusinessConfig()
    language: LanguageConfig = LanguageConfig()
    default: DefaultConfig = DefaultConfig()
    # 配置模型设置
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env",  # 从 .env 文件加载环境变量
        env_file_encoding="utf-8",
        case_sensitive=False,  # 环境变量不区分大小写（如 API_AUTH_SECRET_KEY 和 api_auth_secret_key 等效）
        env_nested_delimiter="__",  # 嵌套配置的环境变量分隔符（如 database__mongodb__db_uri）
    )


# 3. 实例化配置（全局唯一）
settings = Settings()
