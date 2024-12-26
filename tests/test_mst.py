# tests/test_mst.py
import pytest
from utils.mst_algorithm import calculate_mst

def test_calculate_mst():
    towns = 8
    roads = [
        {'start': 1, 'end': 2, 'length': 5},
        {'start': 3, 'end': 4, 'length': 6},
        {'start': 1, 'end': 3, 'length': 7},
        {'start': 4, 'end': 5, 'length': 8},
        {'start': 5, 'end': 6, 'length': 10},
        {'start': 6, 'end': 7, 'length': 12},
        {'start': 7, 'end': 8, 'length': 14},
    ]

    result = calculate_mst(towns, roads)

    expected_result = {
        'newRoads': [
            {'start': 1, 'end': 2, 'length': 5},
            {'start': 3, 'end': 4, 'length': 6},
            {'start': 1, 'end': 3, 'length': 7},
            {'start': 4, 'end': 5, 'length': 8},
            {'start': 5, 'end': 6, 'length': 10},
            {'start': 6, 'end': 7, 'length': 12},
            {'start': 7, 'end': 8, 'length': 14},
        ]
    }

    assert result == expected_result

def test_invalid_input():
    # 测试无效的输入数据
    with pytest.raises(Exception):
        calculate_mst(7, [])  # 城镇数目小于8
        calculate_mst(8, [{'start': 1, 'end': 2, 'length': 5}])  # 道路数目小于16
        calculate_mst(8, [{'start': 0, 'end': 2, 'length': 5}])  # 城镇编号不在合法范围内
        calculate_mst(8, [{'start': 1, 'end': 2, 'length': -1}])  # 道路长度为负数