def merge_config(default, override):
    merged = default.copy()
    for k, v in override.items():
        if isinstance(v, dict):
            merged[k] = {**default.get(k, {}), **v}
        else:
            merged[k] = v
    return merged
