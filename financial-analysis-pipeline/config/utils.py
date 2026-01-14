def merge_config(defaults, overrides):
    merged = defaults.copy()
    for k, v in overrides.items():
        if isinstance(v, dict) and isinstance(merged.get(k), dict):
            merged[k] = merge_config(merged[k], v)
        else:
            merged[k] = v  # replace completely if not both dicts
    return merged
