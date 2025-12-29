def clamp(value, min_val=0, max_val=100):
    return max(min_val, min(value, max_val))


def weighted_score(section_score, weight):
    return clamp(section_score) * weight
