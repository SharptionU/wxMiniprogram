import math


def calc_dist(lat1, lon1, lat2, lon2):
    """
    计算两个经纬度点之间的直线距离（单位：米）
    :param lat1: 第一个点的纬度（度）
    :param lon1: 第一个点的经度（度）
    :param lat2: 第二个点的纬度（度）
    :param lon2: 第二个点的经度（度）
    :return: 两点间距离（米）
    """
    # 将角度转换为弧度
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # 地球半径（米）
    earth_radius = 6371000  # 约6371公里

    # 半正矢公式
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # 计算距离
    distance = earth_radius * c
    return distance

def test_calculate_distance():
    # 示例：计算北京天安门到上海东方明珠的距离
    # 天安门坐标：39.9042° N, 116.4074° E
    # 东方明珠坐标：31.2304° N, 121.4737° E
    distance = calc_dist(39.9042, 116.4074, 31.2304, 121.4737)
    print(f"两点间直线距离：{distance:.2f} 米")
    print(f"约合：{distance / 1000:.2f} 公里")

if __name__ == '__main__':

    test_calculate_distance()
