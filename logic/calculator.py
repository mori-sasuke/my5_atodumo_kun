from .constants import SETTINGS

# 日本語 → 英語の対応表
RATE_KEY_MAP = {
    "BIG": "big",
    "REG": "reg",
    "合算": "total",
    "ブドウ": "grape",
}

def evaluate_all(spins, big, reg, diff):
    result = {}
    actual_rate = {}

    # 実際の確率を計算
    if big > 0:
        actual_rate["BIG"] = spins / big
    if reg > 0:
        actual_rate["REG"] = spins / reg
    if (big + reg) > 0:
        actual_rate["合算"] = spins / (big + reg)
    if spins != 0:
        estimated_grape = diff / 3
        if estimated_grape > 0:
            actual_grape = spins / estimated_grape
            actual_rate["ブドウ"] = 1 / actual_grape

    # 各項目に対して最も近い設定を求める
    for jp_key, actual in actual_rate.items():
        en_key = RATE_KEY_MAP[jp_key]
        closest_setting = min(
            SETTINGS.items(),
            key=lambda item: abs((1 / item[1][en_key]) - actual)
        )
        setting_num, setting_data = closest_setting
        result[jp_key] = {
            "closest": setting_num,
            "actual": actual,
            "setting_value": 1 / setting_data[en_key]
        }

    return result
