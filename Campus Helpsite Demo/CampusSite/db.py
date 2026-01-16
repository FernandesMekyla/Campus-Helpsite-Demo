import pyodbc

def get_conn():
    conn_str = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=(localdb)\\ProjectModels;"
        "Database=CampusHelpdesk;"
        "Trusted_connection=yes;"
        "TrustServerCertificate=yes;"  
    )
    return pyodbc.connect(conn_str)
