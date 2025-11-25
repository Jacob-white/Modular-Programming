import pandas as pd

def generate_html_report(df: pd.DataFrame, title: str) -> str:
    """
    Generates a simple HTML report from a DataFrame.
    """
    html = f"""
    <html>
    <head>
        <title>{title}</title>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #dddddd; text-align: left; padding: 8px; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        {df.to_html(index=False)}
    </body>
    </html>
    """
    return html
