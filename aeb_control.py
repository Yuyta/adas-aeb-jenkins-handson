def calculate_brake_level(distance: float, relative_speed: float) -> float:
    """衝突被害軽減ブレーキ (AEB) のブレーキ強度を計算する

    Args:
        distance (float): 前方車両との距離 (m)。0以上。
        relative_speed (float): 自車と前方車両の相対速度 (m/s)。
            正の値は接近していることを示し、負の値は離れていっていることを示す。

    Returns:
        float: ブレーキ強度 (0.0 から 1.0)
            0.0: ブレーキなし
            1.0: 緊急フルブレーキ
    """

    # 距離が負、または相対速度が0以下の場合はブレーキ不要
    if distance < 0.0 or relative_speed <= 0.0:
        return 0.0

    # ゼロ除算防止
    distance = max(distance, 0.1)

    # 衝突予測時間 (TTC: Time-To-Collision)
    ttc = distance / relative_speed

    # 衝突回避に必要な減速度
    # v² = 2ad → a = v²/(2d)
    required_decel = (relative_speed ** 2) / (2.0 * distance)

    # ---- 緊急フルブレーキ判定 ----
    # TTCが極端に短い場合は躊躇せず最大制動
    if ttc <= 0.8:
        return 1.0

    # ---- 危険度評価 ----
    # TTC危険度
    # TTC 3秒以上 → 0
    # TTC 0.8秒以下 → 1
    ttc_risk = max(0.0, min((3.0 - ttc) / (3.0 - 0.8), 1.0))

    # 必要減速度危険度
    # 1m/s²までは快適
    # 8m/s²以上は緊急レベル
    decel_risk = max(
        0.0,
        min((required_decel - 1.0) / (8.0 - 1.0), 1.0)
    )

    # TTCと必要減速度を組み合わせる
    risk = max(ttc_risk, decel_risk)

    # ---- 滑らかな立ち上がり ----
    # 線形ではなくSmoothstepを使用
    # 急な変化を抑えて自然なブレーキ感にする
    brake_level = risk * risk * (3.0 - 2.0 * risk)

    return round(brake_level, 2)
