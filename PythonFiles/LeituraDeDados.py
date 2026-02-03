from unidecode import unidecode

from ligacao import liga


def Errolog(erro):
	with open("erro.log", "a", encoding="UTF-8-SIG") as fp:
		fp.write(f"{erro}\n")
def SepararNome(x):
	nome = x[0]
	if (len(x) == 1 ):
		apelido = "Sem apelido"
	else:
		apelido = x[-1]

	return nome, apelido

def CriarEmail(x,y):
	email = ""
	if y != "Sem apelido":
		email = unidecode((x +"."+ y + "@cinel.edu.pt").lower())

	else:
		Errolog(f"{x}: Sem apelido")

	return email

def ListaInserir(dic):
	novaListaInserir = []
	for item in dic:
		if "@" in item.get("Email", ""):
			novaListaInserir.append({
				"Nome": item.get("Nome", ""),
				"Apelido": item.get("Apelido", ""),
				"Email": item.get("Email", "")
			})
		else:
			Errolog(f"{item.get('Nome', '')} {item.get('Apelido', '')}: não tem email válido.")

	return novaListaInserir

def CriarDicionario(fp):
	dicionarioCompleto = []
	for linha in fp:
		nomeCompleto = linha.strip().split(" ")
		nome, apelido = SepararNome(nomeCompleto)
		mail = CriarEmail(nome, apelido)
		dic = {
			"Nome": nome,
			"Apelido": apelido,
			"Email": mail
		}
		dicionarioCompleto.append(dic)
	return dicionarioCompleto, len(dicionarioCompleto)

def Leituraficheiro(caminho):
	with open(caminho, "r", encoding="UTF-8-SIG") as fp:
		dicionario = fp.readlines()
		dici, _ = CriarDicionario(dicionario)
		return dici


def CompararDados(valor):
	dadosBD = DadosdaBD() or []

	email_bd = [item.get("Email", "") for item in dadosBD]

	dadosProcessados = []
	for item in valor:
		email = item.get("Email", "")
		if email and (email not in email_bd):
			dadosProcessados.append(item)
		else:
			Errolog(f"{item}: Já se encontra na base de dados!")
	return dadosProcessados


def DadosdaBD():
	con = liga()
	if not con:
		return []

	cursor = con.cursor()
	sql = "use turma30;"
	try:
		cursor.execute(sql)
	except Exception as e:
		print("Nao foi possivel usar a base de dados", e)

	sql = "select * from aluno;"
	try:
		cursor.execute(sql)

		if cursor.description is not None:
			newdados = cursor.fetchall()
		else:
			newdados = []

		dados = []
		for item in newdados:
			dados.append({
				"Nome": item[1],
				"Apelido": item[2],
				"Email": item[3]
			})

		return dados

	except Exception as e:
		print("Erro a retirar dados da Bd", e)
		return []


	






