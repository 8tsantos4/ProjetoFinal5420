import os
from tkinter import *
from tkinter import filedialog, ttk, messagebox
from LeituraDeDados import ListaInserir, Leituraficheiro, CompararDados
from ligacao import liga


###########################Funções###############################

def ComandoSQL(valor):

    con = liga()
    if con:
        cursor = con.cursor()  # cria zona de transferencia de dados
        sql = "select name from sys.databases where name like 'turma30';"  # Obtem nome de todas BDs
        try:
            cursor.execute(sql)  # Manda executar instrução sql
        except:
            print("Não consegui executar o sql")
        # precisamos de "pescar" o resultado no cursor
        dados = cursor.fetchone()  # pesca so um

        if dados:
            sql = "use turma30;"
            try:
                cursor.execute(sql)
            except:
                print("Não foi possivel usar a database. ")
        else:
            sql = "create database turma30;"
            try:
                cursor.execute(sql)
            except:
                print("Não foi possivel criar a database. ")

            sql = "use turma30;"
            try:
                cursor.execute(sql)
            except:
                print("Não foi possivel fazer ligacao a database. ")

        #################################criar a base de dados se não existir ##########################

        sql = """
            if not exists (
                select * from INFORMATION_SCHEMA.TABLES
                where TABLE_NAME = 'aluno')
            begin
                create table aluno(
                        id int primary key identity(1,1),
                        nome varchar(30),
                        apelido varchar(30),
                        email varchar(50)
                );
            end
        """
        try:
            cursor.execute(sql)
        except:
            print("Não criou a tabela.")

        ################################## inserir valores na tabela ##########################
        
        sucesso = 0
        for item in valor:
            sql = f"""insert into aluno(nome,apelido,email) values('{item["Nome"]}', '{item["Apelido"]}', '{item["Email"]}'); """
            
            try:
                cursor.execute(sql)
                sucesso += 1
            # em MySQL precisa forçar a gravação "commit"
            # cursor.commit() #- não precisa pois existe "autocommit=True" na conexão
            except:
                print("Não consegui executar o sql")

def percentagemRegistoSucesso(valor):
    sucessoVar.set(valor)
    sucesso_label.config(text=f"Percentagem de valores inseridos com  sucesso: {valor:.2f}%")
    janela.update_idletasks()

def nomesSemApelido(valor):
    apelidoVar.set(valor)
    semapelidos_label.config(text=f"Percentagem de nomes de apelidos: {valor:.2f}%")
    janela.update_idletasks()

def percentagemerrosemail(valor):
    erromailVar.set(valor)
    erromail_label.config(text=f"Percentagem de falta de emails: {valor:.2f}%")
    janela.update_idletasks()

def Ler_Ficheiro():
    content = filedialog.askopenfilename(
        title="Selecione o ficheiro CVS",
        filetypes=[("Ficheiros CSV", "*.csv")])
    if content:
        caminhoFicheiro.set(content)

#######################janela de visualizacao dos dados inseridos #############

def mostrarDadosInseridos(dados):
    janela_dados = Toplevel(janela)
    janela_dados.title("Dados Inseridos na Base de Dados")
    janela_dados.geometry("700x400")

    ttk.Label(janela_dados, text="Registos Inseridos com Sucesso", font=("Segoe UI", 12, "bold")).pack(pady=10)

    frame_tree = Frame(janela_dados)
    frame_tree.pack(fill="both", expand=True, padx=10, pady=10)

    colunas = ("Nome", "Apelido", "Email")
    tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", height=15)

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=200)

    for item in dados:
        tree.insert("", "end", values=(item["Nome"], item["Apelido"], item["Email"]))

    
    scroll_y = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scroll_y.set)
    scroll_y.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)

    ttk.Button(janela_dados, text="Fechar", command=janela_dados.destroy).pack(pady=10)



               ############ janela de erro.log ########
def abrirErroLog():
    janela2 = Toplevel(janela)
    janela2.title("Registo de Erros")
    janela2.geometry("600x400")

    ttk.Label(janela2, text="Conteúdo do ficheiro erro.log:", font=("Segoe UI", 12, "bold")).pack(pady=10)

    botoes_frame = ttk.Frame(janela2)
    botoes_frame.pack(pady=10)

    ttk.Button(botoes_frame, text="Guardar", command=lambda: guardarAlteracoes(text_box)).pack(side="left", padx=5)


    text_box = Text(janela2, wrap="word", font=("Consolas", 10))
    text_box.pack(fill="both", expand=True, padx=10, pady=10)


    # Verifica se o ficheiro existe

    if os.path.exists("erro.log"):
        with open("erro.log", "r", encoding="utf-8-sig") as fp:
            conteudo = fp.read()
            text_box.insert("1.0", conteudo)
    else:
        text_box.insert("1.0", "Ficheiro erro.log não encontrado.")


    def guardarAlteracoes(text_widget):
        with open("erro.log", "w", encoding="utf-8") as fp:
            fp.write(text_widget.get("1.0", "end-1c"))
        messagebox.showinfo("Guardado", "Alterações guardadas com sucesso!")

    def confirmarFechar():
        if messagebox.askyesno("Sair", "Deseja sair sem guardar alterações?"):
            janela2.destroy()

    ttk.Button(botoes_frame, text="Fechar", command=confirmarFechar).pack(side="left", padx=5)

def executarPrograma():
    if not caminhoFicheiro.get():
        messagebox.showwarning("Aviso", "Selecione primeiro um ficheiro CSV!")
        return
    
    # Lê o ficheiro completo
    conteudoFicheiroInserido = Leituraficheiro(caminhoFicheiro.get())
    total = len(conteudoFicheiroInserido)
    
    # Filtra emails válidos
    conteudoFiltrado = ListaInserir(conteudoFicheiroInserido)
    validos = len(conteudoFiltrado)
    
    # Remove duplicados da BD
    dadosParaInsercao = CompararDados(conteudoFiltrado)
    inseriveis = len(dadosParaInsercao)
    
    # Insere os dados no SQL
    ComandoSQL(dadosParaInsercao)
    mostrarDadosInseridos(dadosParaInsercao)
    
    # Cálculos das percentagens com base em dados reais
    # Percentagem de sucesso = inseridos / total lidos
    perc_sucesso = (inseriveis * 100) / total if total else 0
    
    # Percentagem de emails inválidos = (total - válidos) / total
    perc_email_invalido = ((total - validos) * 100) / total if total else 0
    
    # Percentagem sem apelido = registros cujo apelido == "Sem apelido"
    sem_apelido = len([x for x in conteudoFicheiroInserido if x.get("Apelido") == "Sem apelido"])
    perc_sem_apelido = (sem_apelido * 100) / total if total else 0
    
    # Atualiza barras de progresso e labels
    percentagemRegistoSucesso(perc_sucesso)
    percentagemerrosemail(perc_email_invalido)
    nomesSemApelido(perc_sem_apelido)

    messagebox.showinfo("Sucesso", "Processamento concluído! Clique em 'Ver Erros' para consultar o erro.log.")

###################################### Modo Grafico ##########################################################
janela = Tk()
##################### Centrar janela #################################
largecra = janela.winfo_screenwidth()
altecra = janela.winfo_screenheight()
larg = 800
alt = 600
posx = (largecra // 2) - (larg // 2)
posy = (altecra // 2) - (alt // 2)
janela.geometry(f"{larg}x{alt}+{posx}+{posy}")
janela.resizable(False, False)

janela.title('Anexar dados em base de dados')  #dar nome a janela

############################## criar conteudo para dentro da janela principal###################



label1 = Label(janela, text="Selecione o ficheiro de nomes (CSV):", font=("Segoe UI", 11)).pack(pady=20)

frame = Frame(janela)
frame.pack()
caminhoFicheiro = StringVar()
sucessoVar = DoubleVar()
apelidoVar = DoubleVar()
erromailVar = DoubleVar()

entrada = ttk.Entry(frame,textvariable= caminhoFicheiro,width=50)
entrada.pack(side="left", padx=5)

ttk.Button(frame, text="Procurar...", command=Ler_Ficheiro).pack(side="left", padx=5)

ttk.Button(janela, text="Executar", command=executarPrograma).pack(pady=20)
ttk.Button(janela, text="Ver Erros", command=abrirErroLog).pack(pady=10)

ttk.Button(janela, text="Sair", command=janela.quit).pack(side="bottom", pady=10)


sucesso_label = ttk.Label(janela, text="Percentagem de dados inseridos com sucesso: 0%")
sucesso_label.pack()

barra_sucesso = ttk.Progressbar(
    janela,
    variable=sucessoVar,
    maximum= 100,
    length= 300,
    mode='determinate'
)
barra_sucesso.pack(pady=20)

semapelidos_label= ttk.Label(janela, text="Percentagem de nomes sem apelido: 0%")
semapelidos_label.pack()

barra_semapelidos = ttk.Progressbar(
    janela,
    variable=apelidoVar,
    maximum= 100,
    length= 300,
    mode='determinate'
)
barra_semapelidos.pack(pady=20)

erromail_label = ttk.Label(janela, text="Percentagem de falta de emails: 0%")
erromail_label.pack()

barra_erromail = ttk.Progressbar(
    janela,
    variable=erromailVar,
    maximum=100,
    length=300,
    mode='determinate'
)
barra_erromail.pack(pady=20)

janela.mainloop()