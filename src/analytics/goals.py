import pandas as pd

def calculate_percent_to_goal(actual: float, goal: float) -> float:
    """
    Calculates percentage to goal.
    """
    if goal == 0:
        return 0.0
    return (actual / goal) * 100

def track_goals(df: pd.DataFrame, actual_col: str, goal_col: str) -> pd.DataFrame:
    """
    Adds 'PercentToGoal' and 'GapToGoal' columns.
    """
    df_goals = df.copy()
    df_goals['PercentToGoal'] = (df_goals[actual_col] / df_goals[goal_col]) * 100
    df_goals['GapToGoal'] = df_goals[goal_col] - df_goals[actual_col]
    return df_goals
