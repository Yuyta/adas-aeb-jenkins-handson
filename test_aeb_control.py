import pytest

from aeb_control import calculate_brake_level


def test_safe_distance():
    # 安全な距離（TTC = 10m / 2m/s = 5s）
    # ブレーキは不要であること
    assert calculate_brake_level(10.0, 2.0) == 0.0


def test_warning_brake():
    # 警告域（TTC = 3m / 2m/s = 1.5s）
    # 緊急ブレーキではないが、一定以上のブレーキがかかること
    level = calculate_brake_level(3.0, 2.0)
    assert level == pytest.approx(0.77, abs=0.02)


def test_emergency_brake():
    # 緊急ブレーキ（TTC = 1m / 2m/s = 0.5s）
    # 緊急ブレーキが発動すること
    assert calculate_brake_level(1.0, 2.0) == 1.0


def test_negative_distance():
    # 不正な距離（負の値）ではブレーキがかからないこと
    assert calculate_brake_level(-5.0, 2.0) == 0.0


def test_moving_away():
    # 離れていく場合はブレーキがかからないこと（相対速度が負）
    assert calculate_brake_level(5.0, -2.0) == 0.0
    # 相対速度が0（並走状態）でもふれーきを書けないこと
    assert calculate_brake_level(5.0, 0.0) == 0.0


def test_high_speed_approach():
    # TTCは2sと比較的長いが、高速で接近しているため危険と判断し強いブレーキがかかること
    level = calculate_brake_level(40.0, 20.0)

    assert level == pytest.approx(0.61, abs=0.02)


def test_brake_level_range():
    # ブレーキ強度は常に0.0~1.0の範囲内であること
    level = calculate_brake_level(5.0, 3.0)

    assert 0.0 <= level <= 1.0


def test_ttc_boundary():
    # TTC = 0.8sでは緊急ブレーキ(1.0)にはならないこと
    assert calculate_brake_level(1.6, 2.0) == 1.0

    # TTCが0.8s未満になると、緊急ブレーキになること
    assert calculate_brake_level(2.0, 2.0) < 1.0
