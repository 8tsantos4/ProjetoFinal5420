import pyodbc

def liga():
	driver ="ODBC Driver 17 for SQL Server"
	server = "" #colocar o server
	login = "" #colocar o userLogin
	senha = "" #colocar a password
	try:
		conn = pyodbc.connect(f"DRIVER={driver}; SERVER={server}; UID={login}; PWD={senha}", autocommit=True)
		return conn
	except:
		return False




