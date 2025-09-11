import argon2

from core.config import settings

password_config = settings.password
# 创建密码哈希器（使用 Argon2id 算法）
password_hasher = argon2.PasswordHasher(
    time_cost=password_config.time_cost,  # 计算时间（越高越安全，但越慢）
    memory_cost=password_config.memory_cost,  # 内存使用量（KB）
    parallelism=password_config.parallelism,  # 并行线程数
    hash_len=password_config.hash_len,  # 哈希长度
    salt_len=password_config.salt_len,  # 盐值长度
)
