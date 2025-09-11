import time
import random
from core.config import settings

business_config= settings.business
# 支付方式编码映射
def get_payment_method_code(payment_method: str) -> str:
    payment_codes = business_config.payment_code
    """
    将支付方式映射为2位编码
    可根据实际支付方式进行扩展
    """
    # 如果支付方式不在映射表中，默认返回00
    return payment_codes.get(payment_method.lower(), "00")


def gen_luhn_code(data: str) -> str:
    # 计算校验码 - 使用Luhn算法
    digits = list(map(int, data))
    total = 0
    # 从右向左，偶数位乘以2
    for i in range(len(digits) - 1, -1, -1):
        # 偶数位置（从右向左数，从0开始）
        if (len(digits) - 1 - i) % 2 == 1:
            double = digits[i] * 2
            total += double if double <= 9 else double - 9
        else:
            total += digits[i]
    # 校验码应为 (10 - (total % 10)) % 10
    check_code = str((10 - (total % 10)) % 10)
    return check_code


def check_order_id(order_id: str) -> bool:
    """
    检查订单号是否合法
    """
    if len(order_id) != 19:
        return False
    if not order_id.isalnum():
        return False
    # 校验校验码
    digits = list(map(int, order_id))
    check_code = digits[-1]
    # 使用Luhn算法验证
    expected_check_code = int(gen_luhn_code(order_id[:-1]))
    return check_code == expected_check_code


def generate_order_id(payment_method: str) -> str:
    """
    生成订单号
    格式: 时间戳整数+支付方式(2位)+6位随机数+1位校验码
    """
    # 1. 生成时间戳整数 确保只有10位
    timestamp = str(int(time.time()))[:10]

    # 2. 处理支付方式(2位)
    payment_code = get_payment_method_code(payment_method)

    # 3. 生成6位随机数
    random_str = "".join([str(random.randint(0, 9)) for _ in range(6)])

    # 4. 组合前18位
    prefix = timestamp + payment_code + random_str

    # 5. 计算校验码 - 使用Luhn算法
    check_code = gen_luhn_code(prefix)
    order_id = prefix + check_code
    # print(len(timestamp),len(random_str),len(prefix),len(order_id))
    return order_id


def test():
    iddd = generate_order_id("wechat")
    print(iddd)
    print(check_order_id(iddd))


if __name__ == "__main__":
    test()
