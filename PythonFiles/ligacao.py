import pyodbc

def liga():
	driver ="ODBC Driver 17 for SQL Server"
	server ="(localdb)\\MSSQLLocalDB" #em casa
	#server = "AUD-PORT-003\\SQLEXPRESS" #no cinel
	login ="tiagosantos"
	#login = "sa" #no cinel
	senha ="tiago" #em casa
	#senha = "cinel"
	#senha = "z43VGYT@Iu"
	try:
		conn = pyodbc.connect(f"DRIVER={driver}; SERVER={server}; UID={login}; PWD={senha}", autocommit=True)
		return conn
	except:
		return False




