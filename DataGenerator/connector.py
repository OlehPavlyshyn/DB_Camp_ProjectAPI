import pyodbc

def connection():
    cnxn = pyodbc.connect(r'Driver={SQL Server};Server=.\OLEH_PAVLYSHYN;Database=_Projectv2;Trusted_Connection=yes;')
    return cnxn
