import pandas as pd

def format_decimal(value, precision=4):
    """
    Format a float value with dynamic precision for cleaner display.
    Micro-priced tokens like PEPE might require more decimals.
    """
    try:
        if value >= 1:
            return f"{value:.2f}"
        elif value >= 0.01:
            return f"{value:.4f}"
        elif value >= 0.0001:
            return f"{value:.6f}"
        else:
            return f"{value:.8f}"
    except Exception as e:
        print(f"[Decimal Format Error] {e}")
        return value

def is_uptrend(df: pd.DataFrame, ema_fast='EMA9', ema_slow='EMA21'):
    """
    Determine if the current trend is uptrend based on EMA crossover.
    """
    try:
        return df[ema_fast].iloc[-1] > df[ema_slow].iloc[-1]
    except Exception as e:
        print(f"[Trend Check Error] {e}")
        return False

def is_downtrend(df: pd.DataFrame, ema_fast='EMA9', ema_slow='EMA21'):
    """
    Determine if the current trend is downtrend based on EMA crossover.
    """
    try:
        return df[ema_fast].iloc[-1] < df[ema_slow].iloc[-1]
    except Exception as e:
        print(f"[Trend Check Error] {e}")
        return False

def score_signal(rsi, macd_histogram, proximity_score, trend_factor):
    """
    Generate a composite signal score for decision-making.
    """
    try:
        score = 0
        if 40 < rsi < 60:
            score += 2
        elif rsi < 30 or rsi > 70:
            score += 1

        if macd_histogram > 0:
            score += 2

        score += proximity_score

        if trend_factor == "up":
            score += 2
        elif trend_factor == "neutral":
            score += 1

        return score
    except Exception as e:
        print(f"[Signal Score Error] {e}")
        return 0