# -*- coding: utf-8 -*-
# @Author      : LJQ
# @Time        : 2019/8/1 15:11
# @Version     : Python 3.6.8
# @Description :
EARTH_RADIUS = 6370996.81
MERCATOR_BAND = [12890594.86, 8362377.87, 5591021, 3481989.83, 1678043.12, 0]
BD09LL_BAND = [75, 60, 45, 30, 15, 0]
MERCATOR_TO_BD09LL = [
    [1.410526172116255e-8, 0.00000898305509648872, -1.9939833816331, 200.9824383106796, -187.2403703815547,
     91.6087516669843, -23.38765649603339, 2.57121317296198, -0.03801003308653, 17337981.2],
    [-7.435856389565537e-9, 0.000008983055097726239, -0.78625201886289, 96.32687599759846, -1.85204757529826,
     -59.36935905485877, 47.40033549296737, -16.50741931063887, 2.28786674699375, 10260144.86],
    [-3.030883460898826e-8, 0.00000898305509983578, 0.30071316287616, 59.74293618442277, 7.357984074871,
     -25.38371002664745, 13.45380521110908, -3.29883767235584, 0.32710905363475, 6856817.37],
    [-1.981981304930552e-8, 0.000008983055099779535, 0.03278182852591, 40.31678527705744, 0.65659298677277,
     -4.44255534477492, 0.85341911805263, 0.12923347998204, -0.04625736007561, 4482777.06],
    [3.09191371068437e-9, 0.000008983055096812155, 0.00006995724062, 23.10934304144901, -0.00023663490511,
     -0.6321817810242, -0.00663494467273, 0.03430082397953, -0.00466043876332, 2555164.4],
    [2.890871144776878e-9, 0.000008983055095805407, -3.068298e-8, 7.47137025468032, -0.00000353937994,
     -0.02145144861037, -0.00001234426596, 0.00010322952773, -0.00000323890364, 826088.5]]
BD09LL_TO_MERCATOR = [
    [-0.0015702102444, 111320.7020616939, 1704480524535203, -10338987376042340, 26112667856603880, -35149669176653700,
     26595700718403920, -10725012454188240, 1800819912950474, 82.5],
    [0.0008277824516172526, 111320.7020463578, 647795574.6671607, -4082003173.641316, 10774905663.51142,
     -15171875531.51559, 12053065338.62167, -5124939663.577472, 913311935.9512032, 67.5],
    [0.00337398766765, 111320.7020202162, 4481351.045890365, -23393751.19931662, 79682215.47186455, -115964993.2797253,
     97236711.15602145, -43661946.33752821, 8477230.501135234, 52.5],
    [0.00220636496208, 111320.7020209128, 51751.86112841131, 3796837.749470245, 992013.7397791013, -1221952.21711287,
     1340652.697009075, -620943.6990984312, 144416.9293806241, 37.5],
    [-0.0003441963504368392, 111320.7020576856, 278.2353980772752, 2485758.690035394, 6070.750963243378,
     54821.18345352118, 9540.606633304236, -2710.55326746645, 1405.483844121726, 22.5],
    [-0.0003218135878613132, 111320.7020701615, 0.00369383431289, 823725.6402795718, 0.46104986909093,
     2351.343141331292, 1.58060784298199, 8.77738589078284, 0.37238884252424, 7.45]]


def mercator2bd(mercator_x, mercator_y):
    offset = None
    mercator_x = abs(mercator_x)
    mercator_y = abs(mercator_y)
    for index, band in enumerate(MERCATOR_BAND):
        if mercator_y >= band:
            offset = MERCATOR_TO_BD09LL[index]
            break

    location = __converter(mercator_x, mercator_y, offset)
    return location


def bd2mercator(bd_lng, bd_lat):
    offset = None
    bd_lng = __get_longitude(bd_lng, -180, 180)
    bd_lat = __get_latitude(bd_lat, -74, 74)
    for index, band in enumerate(BD09LL_BAND):
        if bd_lat >= band:
            offset = BD09LL_TO_MERCATOR[index]
            break

    if offset is not None:
        for index in range(BD09LL_BAND.__len__() - 1, -1, -1):
            if bd_lat <= -BD09LL_BAND[index]:
                offset = BD09LL_TO_MERCATOR[index]
                break

    return __converter(bd_lng, bd_lat, offset)


def __get_longitude(longitude, _min, _max):
    while longitude > _max:
        longitude -= _max - _min

    while longitude < _min:
        longitude += _max - _min

    return longitude


def __get_latitude(latitude, _min, _max):
    if _min is not None:
        latitude = max(latitude, _min)

    if _max is not None:
        latitude = min(latitude, _max)

    return latitude


def __converter(mercator_x, mercator_y, offset):
    x_temp = offset[0] + offset[1] * abs(mercator_x)
    deviation = abs(mercator_y) / offset[9]
    y_temp = (offset[2] + offset[3] * deviation + offset[4] * deviation * deviation +
              offset[5] * deviation * deviation * deviation +
              offset[6] * deviation * deviation * deviation * deviation +
              offset[7] * deviation * deviation * deviation * deviation * deviation +
              offset[8] * deviation * deviation * deviation * deviation * deviation * deviation)
    x_temp *= -1 if mercator_x < 0 else 1
    y_temp *= -1 if mercator_y < 0 else 1
    return x_temp, y_temp


if __name__ == '__main__':
    print(bd2mercator(113.65166099999993, 34.77967796897911))
    print(mercator2bd(12651782.690569153, 4109381.0843539275))
