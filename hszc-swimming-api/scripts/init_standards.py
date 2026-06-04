"""初始化游泳运动员等级标准数据 (2025版)"""

from decimal import Decimal


def get_standards_data():
    """
    中国游泳运动员技术等级标准 (2025版)
    数据来源：国家体育总局《运动员技术等级标准》
    50米池标准
    """

    standards = []

    # ========== 50米池 - 男子 ==========
    # 自由泳
    male_freestyle_50m = [
        # (距离, 等级, 成绩秒)
        (50, 'international', Decimal('21.89')),
        (50, 'national', Decimal('23.01')),
        (50, 'level_1', Decimal('24.04')),
        (50, 'level_2', Decimal('26.04')),
        (50, 'level_3', Decimal('28.04')),

        (100, 'international', Decimal('48.29')),
        (100, 'national', Decimal('50.74')),
        (100, 'level_1', Decimal('52.74')),
        (100, 'level_2', Decimal('55.74')),
        (100, 'level_3', Decimal('58.74')),

        (200, 'international', Decimal('105.71')),
        (200, 'national', Decimal('110.96')),
        (200, 'level_1', Decimal('115.61')),
        (200, 'level_2', Decimal('120.61')),
        (200, 'level_3', Decimal('125.61')),

        (400, 'international', Decimal('227.00')),
        (400, 'national', Decimal('238.35')),
        (400, 'level_1', Decimal('248.35')),
        (400, 'level_2', Decimal('258.35')),
        (400, 'level_3', Decimal('268.35')),

        (800, 'international', Decimal('470.91')),
        (800, 'national', Decimal('494.46')),
        (800, 'level_1', Decimal('514.46')),
        (800, 'level_2', Decimal('534.46')),
        (800, 'level_3', Decimal('554.46')),

        (1500, 'international', Decimal('884.72')),
        (1500, 'national', Decimal('929.05')),
        (1500, 'level_1', Decimal('954.05')),
        (1500, 'level_2', Decimal('989.05')),
        (1500, 'level_3', Decimal('1019.05')),
    ]

    # 仰泳
    male_backstroke = [
        (50, 'international', Decimal('24.92')),
        (50, 'national', Decimal('26.16')),
        (50, 'level_1', Decimal('27.41')),
        (50, 'level_2', Decimal('29.41')),
        (50, 'level_3', Decimal('31.41')),

        (100, 'international', Decimal('53.36')),
        (100, 'national', Decimal('56.03')),
        (100, 'level_1', Decimal('58.68')),
        (100, 'level_2', Decimal('61.68')),
        (100, 'level_3', Decimal('64.68')),

        (200, 'international', Decimal('114.92')),
        (200, 'national', Decimal('120.67')),
        (200, 'level_1', Decimal('126.02')),
        (200, 'level_2', Decimal('131.02')),
        (200, 'level_3', Decimal('136.02')),
    ]

    # 蛙泳
    male_breaststroke = [
        (50, 'international', Decimal('26.67')),
        (50, 'national', Decimal('28.03')),
        (50, 'level_1', Decimal('29.28')),
        (50, 'level_2', Decimal('31.28')),
        (50, 'level_3', Decimal('33.28')),

        (100, 'international', Decimal('58.96')),
        (100, 'national', Decimal('61.91')),
        (100, 'level_1', Decimal('64.66')),
        (100, 'level_2', Decimal('67.66')),
        (100, 'level_3', Decimal('70.66')),

        (200, 'international', Decimal('128.57')),
        (200, 'national', Decimal('135.09')),
        (200, 'level_1', Decimal('141.09')),
        (200, 'level_2', Decimal('146.09')),
        (200, 'level_3', Decimal('151.09')),
    ]

    # 蝶泳
    male_butterfly = [
        (50, 'international', Decimal('22.76')),
        (50, 'national', Decimal('23.92')),
        (50, 'level_1', Decimal('25.07')),
        (50, 'level_2', Decimal('27.07')),
        (50, 'level_3', Decimal('29.07')),

        (100, 'international', Decimal('50.74')),
        (100, 'national', Decimal('53.31')),
        (100, 'level_1', Decimal('55.81')),
        (100, 'level_2', Decimal('58.81')),
        (100, 'level_3', Decimal('61.81')),

        (200, 'international', Decimal('111.42')),
        (200, 'national', Decimal('117.00')),
        (200, 'level_1', Decimal('122.00')),
        (200, 'level_2', Decimal('127.00')),
        (200, 'level_3', Decimal('132.00')),
    ]

    # 混合泳
    male_medley = [
        (200, 'international', Decimal('115.55')),
        (200, 'national', Decimal('121.33')),
        (200, 'level_1', Decimal('126.83')),
        (200, 'level_2', Decimal('131.83')),
        (200, 'level_3', Decimal('136.83')),

        (400, 'international', Decimal('243.73')),
        (400, 'national', Decimal('255.92')),
        (400, 'level_1', Decimal('267.42')),
        (400, 'level_2', Decimal('277.42')),
        (400, 'level_3', Decimal('287.42')),
    ]

    # 添加男子数据
    for distance, level, time in male_freestyle_50m:
        standards.append(('male', 50, 'freestyle', distance, level, time))
    for distance, level, time in male_backstroke:
        standards.append(('male', 50, 'backstroke', distance, level, time))
    for distance, level, time in male_breaststroke:
        standards.append(('male', 50, 'breaststroke', distance, level, time))
    for distance, level, time in male_butterfly:
        standards.append(('male', 50, 'butterfly', distance, level, time))
    for distance, level, time in male_medley:
        standards.append(('male', 50, 'medley', distance, level, time))

    # ========== 50米池 - 女子 ==========
    # 自由泳
    female_freestyle = [
        (50, 'international', Decimal('24.05')),
        (50, 'national', Decimal('25.25')),
        (50, 'level_1', Decimal('26.50')),
        (50, 'level_2', Decimal('28.50')),
        (50, 'level_3', Decimal('30.50')),

        (100, 'international', Decimal('52.21')),
        (100, 'national', Decimal('54.81')),
        (100, 'level_1', Decimal('57.31')),
        (100, 'level_2', Decimal('60.31')),
        (100, 'level_3', Decimal('63.31')),

        (200, 'international', Decimal('114.02')),
        (200, 'national', Decimal('119.82')),
        (200, 'level_1', Decimal('125.32')),
        (200, 'level_2', Decimal('130.32')),
        (200, 'level_3', Decimal('135.32')),

        (400, 'international', Decimal('236.83')),
        (400, 'national', Decimal('248.67')),
        (400, 'level_1', Decimal('260.07')),
        (400, 'level_2', Decimal('270.07')),
        (400, 'level_3', Decimal('280.07')),

        (800, 'international', Decimal('485.12')),
        (800, 'national', Decimal('509.37')),
        (800, 'level_1', Decimal('531.87')),
        (800, 'level_2', Decimal('551.87')),
        (800, 'level_3', Decimal('571.87')),

        (1500, 'international', Decimal('936.86')),
        (1500, 'national', Decimal('983.70')),
        (1500, 'level_1', Decimal('1018.70')),
        (1500, 'level_2', Decimal('1058.70')),
        (1500, 'level_3', Decimal('1098.70')),
    ]

    # 仰泳
    female_backstroke = [
        (50, 'international', Decimal('27.48')),
        (50, 'national', Decimal('28.85')),
        (50, 'level_1', Decimal('30.25')),
        (50, 'level_2', Decimal('32.25')),
        (50, 'level_3', Decimal('34.25')),

        (100, 'international', Decimal('58.21')),
        (100, 'national', Decimal('61.12')),
        (100, 'level_1', Decimal('64.02')),
        (100, 'level_2', Decimal('67.02')),
        (100, 'level_3', Decimal('70.02')),

        (200, 'international', Decimal('124.18')),
        (200, 'national', Decimal('130.49')),
        (200, 'level_1', Decimal('136.49')),
        (200, 'level_2', Decimal('141.49')),
        (200, 'level_3', Decimal('146.49')),
    ]

    # 蛙泳
    female_breaststroke = [
        (50, 'international', Decimal('29.88')),
        (50, 'national', Decimal('31.38')),
        (50, 'level_1', Decimal('32.88')),
        (50, 'level_2', Decimal('34.88')),
        (50, 'level_3', Decimal('36.88')),

        (100, 'international', Decimal('65.15')),
        (100, 'national', Decimal('68.41')),
        (100, 'level_1', Decimal('71.41')),
        (100, 'level_2', Decimal('74.41')),
        (100, 'level_3', Decimal('77.41')),

        (200, 'international', Decimal('140.46')),
        (200, 'national', Decimal('147.48')),
        (200, 'level_1', Decimal('154.48')),
        (200, 'level_2', Decimal('159.48')),
        (200, 'level_3', Decimal('164.48')),
    ]

    # 蝶泳
    female_butterfly = [
        (50, 'international', Decimal('25.49')),
        (50, 'national', Decimal('26.78')),
        (50, 'level_1', Decimal('28.03')),
        (50, 'level_2', Decimal('30.03')),
        (50, 'level_3', Decimal('32.03')),

        (100, 'international', Decimal('56.03')),
        (100, 'national', Decimal('58.83')),
        (100, 'level_1', Decimal('61.58')),
        (100, 'level_2', Decimal('64.58')),
        (100, 'level_3', Decimal('67.58')),

        (200, 'international', Decimal('121.87')),
        (200, 'national', Decimal('128.02')),
        (200, 'level_1', Decimal('134.02')),
        (200, 'level_2', Decimal('139.02')),
        (200, 'level_3', Decimal('144.02')),
    ]

    # 混合泳
    female_medley = [
        (200, 'international', Decimal('125.81')),
        (200, 'national', Decimal('132.10')),
        (200, 'level_1', Decimal('138.60')),
        (200, 'level_2', Decimal('143.60')),
        (200, 'level_3', Decimal('148.60')),

        (400, 'international', Decimal('262.52')),
        (400, 'national', Decimal('275.65')),
        (400, 'level_1', Decimal('288.65')),
        (400, 'level_2', Decimal('298.65')),
        (400, 'level_3', Decimal('308.65')),
    ]

    # 添加女子数据
    for distance, level, time in female_freestyle:
        standards.append(('female', 50, 'freestyle', distance, level, time))
    for distance, level, time in female_backstroke:
        standards.append(('female', 50, 'backstroke', distance, level, time))
    for distance, level, time in female_breaststroke:
        standards.append(('female', 50, 'breaststroke', distance, level, time))
    for distance, level, time in female_butterfly:
        standards.append(('female', 50, 'butterfly', distance, level, time))
    for distance, level, time in female_medley:
        standards.append(('female', 50, 'medley', distance, level, time))

    # ========== 25米池成绩换算 ==========
    # 25米池成绩通常比50米池快0.5-1秒（转身优势）
    # 这里添加25米池标准（略快于50米池）
    male_25m_pool = []
    female_25m_pool = []

    for gender, pool, stroke, distance, level, time in standards:
        if gender == 'male':
            # 25米池比50米池快约0.5秒
            adjusted_time = time - Decimal('0.50')
            male_25m_pool.append((gender, 25, stroke, distance, level, adjusted_time))
        else:
            adjusted_time = time - Decimal('0.50')
            female_25m_pool.append((gender, 25, stroke, distance, level, adjusted_time))

    standards.extend(male_25m_pool)
    standards.extend(female_25m_pool)

    return standards


def run():
    """执行初始化"""
    from apps.standards.models import SwimmingStandard

    # 清空现有数据
    SwimmingStandard.objects.all().delete()

    # 插入新数据
    standards_data = get_standards_data()
    records = []
    for data in standards_data:
        records.append(SwimmingStandard(
            gender=data[0],
            pool_length=data[1],
            stroke=data[2],
            distance=data[3],
            level=data[4],
            qualifying_time=data[5],
            version='2025'
        ))

    SwimmingStandard.objects.bulk_create(records)
    print(f'成功插入 {len(records)} 条游泳等级标准数据')


if __name__ == '__main__':
    run()