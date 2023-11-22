import math

def my_round(val):
    return round(val * 100) / 100

def score(min_val, max_val, value):
    value = min(max_val, max(min_val, value))
    return my_round(1 + 9 * (value - min_val) / (max_val - min_val))

def z_score(max_val, value):
    return score(0, max_val, value)

def i_score(min_val, max_val, value):
    value = min(max_val, max(min_val, value))
    return my_round(1 + 9 * (max_val - value) / (max_val - min_val))

def iz_score(max_val, value):
    return i_score(0, max_val, value)

def aggregate(weights, values):
    max_val = 10 * sum(weights)
    min_val = 1 * sum(weights)
    total = sum(weight * value for weight, value in zip(weights, values))
    return score(min_val, max_val, total)