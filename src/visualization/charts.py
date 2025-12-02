import matplotlib.pyplot as plt
import pandas as pd
import io
from typing import Optional

def generate_bar_chart(
    df: pd.DataFrame, 
    x_col: str, 
    y_col: str, 
    title: str = "Bar Chart", 
    xlabel: Optional[str] = None, 
    ylabel: Optional[str] = None
) -> io.BytesIO:
    """
    Generates a bar chart and returns it as a BytesIO object.
    """
    plt.figure(figsize=(10, 6))
    plt.bar(df[x_col], df[y_col], color='skyblue')
    plt.title(title)
    plt.xlabel(xlabel if xlabel else x_col)
    plt.ylabel(ylabel if ylabel else y_col)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    
    return img_buffer

def generate_line_chart(
    df: pd.DataFrame, 
    x_col: str, 
    y_col: str, 
    title: str = "Line Chart", 
    xlabel: Optional[str] = None, 
    ylabel: Optional[str] = None
) -> io.BytesIO:
    """
    Generates a line chart and returns it as a BytesIO object.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(df[x_col], df[y_col], marker='o', linestyle='-', color='green')
    plt.title(title)
    plt.xlabel(xlabel if xlabel else x_col)
    plt.ylabel(ylabel if ylabel else y_col)
    plt.grid(True)
    plt.tight_layout()
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    
    return img_buffer
