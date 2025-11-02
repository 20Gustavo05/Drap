from tkinter import *
from tkinter import ttk
import sqlite3

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser

#criando uma janela
janela = Tk()

# Classe para preenchimento correto de valores nas entrys
class Validador:
# valida se todas as Entrys do frame 1 aba 2 estão preenchidas
    def ativa_botão(self):
        if self.entrada_var():
            return self.bt_comprar.config(state="normal")
        else:
            return self.bt_comprar.config(state="disabled")

# Classe para criar relatorios em PDF
class Relatorios:
    def printCliente(self):
        webbrowser.open("cliente.pdf")
    
    def geraRelatCliente(self):
        self.c = canvas.Canvas("cliente.pdf")
        self.codigoRel = self.cod_entry.get()
        self.nomeRel = self.nome_entry.get()
        self.registroRel = self.registro_entry.get()
        self.telefoneRel = self.telefone_entry.get()
        self.usuarioRel = self.usuario_entry.get()
        self.enderecoRel = self.endereco_entry.get()
        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, 'Ficha do Cliente')

        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, 700, 'Código: ' + self.codigoRel)
        self.c.drawString(50, 670, 'Nome: ' + self.nomeRel) 
        self.c.drawString(50, 640, 'Registro: ' + self.registroRel)
        self.c.drawString(50, 610, 'Telefone: ' + self.telefoneRel)
        self.c.drawString(50, 580, 'Usuário: ' + self.usuarioRel)
        self.c.drawString(50, 550, 'Endereço: ' + self.enderecoRel)

        self.c.rect(20, 750, 550 , 5, fill=False , stroke=True)
        self.c.rect(20, 500, 550 , 5, fill=True, stroke=False)

        self.c.showPage()
        self.c.save()
        self.printCliente()

# Classe de funcionalidades do sistema
class Funcs():
# função conectar banco    
    def conecta_banco(self):
        self.conn = sqlite3.connect('pojetoPrincipal_database.db')
        self.cursor = self.conn.cursor()
        print("Conectando ao banco de dados")

# função desconectar banco    
    def desconecta_banco(self):
        self.conn.close()
        print("Desconectando do banco de dados")

# função criar tabela dentro do banco dados caso não existam  
    def monta_tabela(self):
        self.conecta_banco()
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                nome TEXT,
                telefone TEXT,
                endereco VARCHAR(100),
                usuario VARCHAR(8),
                cpf CHAR(11) NOT NULL
                );
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                modelo TEXT,
                tamanho TEXT,
                preco TEXT
                );
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                cliente_id INTEGER,
                produto_id INTEGER,
                data_pedido DATE,
                status_pagamento TEXT,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id),
                FOREIGN KEY (produto_id) REFERENCES produtos(id)
                )
            """)
        self.conn.commit()
        self.desconecta_banco()

# função para limmpar os entrys do frame 1
    def limpar_tela(self):
        self.clie_cod_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.registro_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.endereco_entry.delete(0, END)
        self.usuario_entry.delete(0, END)
        self.prod_cod_entry.delete(0, END)
        self.modelo_entry.delete(0, END)
        self.tamanho_entry.delete(0, END)

# função atualizar dados da tabela clientes
    def atualizar_dados(self):
        self.variaveisClientes()
        self.variaveisProdutos()
        aba_ativa = self.notebook.select()
        nome_aba = self.notebook.tab(aba_ativa, "text")
        if nome_aba == "Clientes":
            self.conecta_banco()
            self.cursor.execute("""UPDATE clientes SET nome = ?, cpf = ?, telefone = ?, usuario = ?, endereco = ? WHERE id = ?""", (self.nome, self.registro, self.telefone, self.usuario, self.endereco, self.codClie))
            self.conn.commit()
            self.desconecta_banco()
            self.listar_dados()
            self.limpar_tela()
        elif nome_aba == "Produtos":
            self.conecta_banco()
            self.cursor.execute("""UPDATE produtos SET modelo = ?, tamanho = ?, preco = ? WHERE id = ?""", (self.modelo, self.tamanho, self.preco, self.codProd))
            self.conn.commit()
            self.desconecta_banco()
            self.listar_dados()
            self.limpar_tela() 

# função deletar dados 
    def deletar_dados(self):
        self.variaveisClientes()
        self.variaveisProdutos()
        aba_ativa = self.notebook.select()
        nome_aba = self.notebook.tab(aba_ativa, "text")
        if nome_aba == "Clientes":
            self.lista_clientes.delete(*self.lista_clientes.get_children())
            self.conecta_banco()
            self.cursor.execute("DELETE FROM clientes WHERE id = ?", (self.codClie))
            self.conn.commit()
            self.desconecta_banco()
            self.listar_dados()
            self.limpar_tela()
        elif nome_aba == "Produtos":
            self.lista_produtos.delete(*self.lista_produtos.get_children())
            self.conecta_banco()
            self.cursor.execute("DELETE FROM clientes WHERE id = ?", (self.codProd))
            self.conn.commit()
            self.desconecta_banco()
            self.listar_dados()
            self.limpar_tela()

# função inserir dados detro da tabela clientes do banco de dados
    def inserir_dados(self):
        self.variaveisClientes()
        self.variaveisProdutos()
        aba_ativa = self.notebook.select()
        nome_aba = self.notebook.tab(aba_ativa, "text")
        if nome_aba == "Clientes":
            self.conecta_banco()
            self.cursor.execute(""" INSERT INTO clientes (nome, cpf, telefone, usuario, endereco) VALUES (?, ?, ?, ?, ?)""", (self.nome, self.registro, self.telefone, self.usuario, self.endereco))
            self.conn.commit()
            self.desconecta_banco()
            self.listar_dados()
            self.limpar_tela()
        if nome_aba == "Produtos":
            self.conecta_banco()
            self.cursor.execute(""" INSERT INTO produtos (modelo, tamanho, preco) VALUES (?, ?, ?)""", (self.modelo, self.tamanho, self.preco))
            self.conn.commit()
            self.desconecta_banco()
            self.listar_dados()
            self.limpar_tela()

# função listar dados dentro da tabela widget_frame2
    def listar_dados(self, event=None):
        aba_ativa = self.notebook.select()
        nome_aba = self.notebook.tab(aba_ativa, "text")
        configuracoes = {
            "Clientes": {
                "tabela": "clientes",
                "campos": "id, nome, cpf, telefone, usuario, endereco",
                "widgets": self.lista_clientes,
                "variaveis_func": self.variaveisClientes
            },
            "Produtos": {
                "tabela": "produtos",
                "campos": "id, modelo, tamanho, preco",
                "widgets": self.lista_produtos,
                "variaveis_func": self.variaveisProdutos
            }
        }
        if nome_aba in configuracoes:
            cfg = configuracoes[nome_aba]
            cfg["variaveis_func"]()
            cfg["widgets"].delete(*cfg["widgets"].get_children())
            self.conecta_banco()
            query = f"SELECT {cfg['campos']} FROM {cfg['tabela']} ORDER BY id ASC;"
            resultados = self.cursor.execute(query)
            for linha in resultados:
                cfg["widgets"].insert("", END, values=linha)
            self.desconecta_banco()

# função buscar dados
    def buscar_dados_clie(self):
        self.variaveisClientes()
        self.lista_clientes.delete(*self.lista_clientes.get_children())
        self.conecta_banco()
        item = self.cursor.execute("""SELECT * FROM clientes WHERE id = ?""", (self.codClie,))
        for i in item:
            self.lista_clientes.insert("", END, value=i)
        self.desconecta_banco()
        self.limpar_tela()
# função buscar dados
    def buscar_dados_prod(self):
        self.variaveisProdutos()
        self.lista_produtos.delete(*self.lista_produtos.get_children())
        self.conecta_banco()
        item = self.cursor.execute("""SELECT * FROM produtos WHERE id = ?""", (self.codProd,))
        for i in item:
            self.lista_produtos.insert("", END, value=i)
        self.desconecta_banco()
        self.limpar_tela()

# função clicar duas vezes
    def duplo_clique(self, event):
        self.limpar_tela()
        aba_ativa = self.notebook.select()
        nome_aba = self.notebook.tab(aba_ativa, "text")
        if nome_aba == "Clientes":
            self.lista_clientes.selection()
            for n in self.lista_clientes.selection():
                col1, col2, col3, col4, col5, col6 = self.lista_clientes.item(n, "value")
                self.clie_cod_entry.insert(END, col1)
                self.nome_entry.insert(END, col2)
                self.registro_entry.insert(END, col3)
                self.telefone_entry.insert(END, col4)
                self.usuario_entry.insert(END, col5)
                self.endereco_entry.insert(END, col6)
        elif nome_aba == "Produtos":
            self.lista_produtos.selection()
            for m in self.lista_produtos.selection():
                col1, col2, col3 = self.lista_produtos.item(m, "value")
                self.prod_cod_entry.insert(END, col1)
                self.modelo_entry.insert(END, col2)
                self.tamanho_entry.insert(END, col3)
                self.preco_entry.insert(END, col4)

# função para as variáveis dos produtos
    def variaveisClientes(self):
        self.codClie = self.clie_cod_entry.get()
        self.nome = self.nome_entry.get()
        self.registro = self.registro_entry.get()
        self.telefone = self.telefone_entry.get()
        self.endereco = self.endereco_entry.get()
        self.usuario = self.usuario_entry.get()
# função para as variaveis dos produtos
    def variaveisProdutos(self):
        self.codProd = self.prod_cod_entry.get()
        self.modelo = self.modelo_entry.get()
        self.tamanho = self.tamanho_entry.get()
        self.preco = self.preco_entry.get()     

# Visualizando tudo que existe na janela
class Aplicacao(Funcs, Relatorios, Validador):
    def __init__(self, master=None):
        self.janela = janela
        self.tela()
        self.abas()
        self.frames()
        self.menus()
        self.widgets_frame1()
        self.widgets_frame2()
        self.monta_tabela()
        self.listar_dados()
        janela.mainloop()

# configurando a telas
    def tela(self):
        self.janela.title("Sistema de Gerenciamento")
        self.janela.configure(background="#1e3743")
        self.janela.geometry("700x500")
        self.janela.resizable(True, True)
        self.janela.maxsize(width=900, height=700)  
        self.janela.minsize(width=700, height=500)

# criando e configurando um nova janela
    def nova_janela(self):
        self.janela2 = Toplevel()
        self.janela2.title("Segunda Janela")
        self.janela2.configure(background="#1e3743")
        self.janela.geometry("700x500")
        self.janela.resizable(True, True)
        self.janela.maxsize(width=900, height=700)  
        self.janela.minsize(width=700, height=500)
        self.janela2.transient(self.janela) # define de onde virá a segunda janela
        self.janela2.focus_force() # força a segunda janela a fincar na frente da primeia
        self.janela2.grab_set() # não permite que a primeira janela seja editada enquanto a segunda estiver aberta

# criando abas
    def abas(self):
        self.notebook = ttk.Notebook(self.janela)
        self.notebook.pack(fill="both", expand="True")
        self.aba1 = Frame(self.notebook)
        self.aba2 = Frame(self.notebook)
        self.aba3 = Frame(self.notebook)
        self.notebook.add(self.aba1, text="Clientes")
        self.notebook.add(self.aba2, text="Produtos")
        self.notebook.add(self.aba3, text="Pedidos")

# criando frames das abas
    def frames(self):
    # criando frames da aba 1
        self.frame1_aba1 = Frame(self.aba1, bd=4, bg="#dadfe2", highlightbackground="#2d3e5a", highlightthickness=2)
        self.frame1_aba1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)
        self.frame2_aba1 = Frame(self.aba1, bd=4, bg="#dadfe2", highlightbackground="#2d3e5a", highlightthickness=2)
        self.frame2_aba1.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)   
    # criando frames da aba 2
        self.frame1_aba2 = Frame(self.aba2, bd=4, bg="#dadfe2", highlightbackground="#2d3e5a", highlightthickness=2)
        self.frame1_aba2.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.3)
        self.frame2_aba2 = Frame(self.aba2, bd=4, bg="#dadfe2", highlightbackground="#2d3e5a", highlightthickness=2)
        self.frame2_aba2.place(relx=0.02, rely=0.34, relwidth=0.48, relheight=0.62)
        self.frame3_aba2 = Frame(self.aba2, bd=4, bg="#dadfe2", highlightbackground="#2d3e5a", highlightthickness=2)
        self.frame3_aba2.place(relx=0.52, rely=0.34, relwidth=0.46, relheight=0.62)
        self.frame1_aba3 = Frame(self.aba3, bd=4, bg="#dadfe2", highlightbackground="#2d3e5a", highlightthickness=2)
        self.frame1_aba3.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.6)
        self.frame2_aba3 = Frame(self.aba3, bd=4, bg="#dadfe2", highlightbackground="#2d3e5a", highlightthickness=2)
        self.frame2_aba3.place(relx=0.02, rely=0.64, relwidth=0.96, relheight=0.33)
        
# criando os menus da janela
    def menus(self):
        self.bar_menu = Menu(self.janela)
        self.janela.configure(menu=self.bar_menu)
        self.bt_menu1 = Menu(self.bar_menu)
        self.bar_menu.add_cascade(label="Arquivo", menu=self.bt_menu1)
        self.bt_menu1.add_command(label="Nova Janela", command=self.nova_janela)
        self.bt_menu1.add_command(label="Relatorio", command=self.geraRelatCliente)

# criando botões e caixas de texto dentro dos frames 1
    def widgets_frame1(self):
    # botões, labels e entrys do frame 1 da aba 1
        self.bt_buscar_aba1 = Button(self.frame1_aba1, text="Buscar", bd=2, bg="#4987a3", fg="white", font=("Verdana", 9, "bold "), command=self.buscar_dados_clie)
        self.bt_buscar_aba1.place(relx=0.2, rely=0.2, relwidth=0.1, relheight=0.13)
        self.bt_limpar_aba1 = Button(self.frame1_aba1, text="Limpar", bd=2, bg="#4987a3", fg="white", font=("Verdana", 9, "bold "), command=self.limpar_tela)     
        self.bt_limpar_aba1.place(relx=0.3, rely=0.2, relwidth=0.1, relheight=0.13)
        self.bt_inserir_aba1 = Button(self.frame1_aba1, text="Inserir", bd=2, bg="#4987a3", fg="white", font=("Verdana", 9, "bold "), command=self.inserir_dados)     
        self.bt_inserir_aba1.place(relx=0.5, rely=0.2, relwidth=0.1, relheight=0.13)
        self.bt_atul_aba1 = Button(self.frame1_aba1, text="Atualizar", bd=2, bg="#4987a3", fg="white", font=("Verdana", 9, "bold "), command=self.atualizar_dados)     
        self.bt_atul_aba1.place(relx=0.6, rely=0.2, relwidth=0.1, relheight=0.13)
        self.bt_deletar_aba1 = Button(self.frame1_aba1, text="Deletar", bd=2, bg="#4987a3", fg="white", font=("Verdana", 9, "bold "), command=self.deletar_dados)     
        self.bt_deletar_aba1.place(relx=0.7, rely=0.2, relwidth=0.1, relheight=0.13)
    # criando labels (textos)
        self.lb_cod_clie = Label(self.frame1_aba1, text="Código", font=("Arial", 10), bg="#dadfe2", fg="#1e3743")
        self.lb_cod_clie.place(relx=0.05, rely=0.1)
        self.lb_nome = Label(self.frame1_aba1, text="Nome", font=("Arial", 10), bg="#dadfe2", fg="#1e3743")
        self.lb_nome.place(relx=0.05, rely=0.4)
        self.lb_registro = Label(self.frame1_aba1, text="CPF/CNP-J", font=("Arial", 10), bg="#dadfe2", fg="#1e3743")
        self.lb_registro.place(relx=0.3, rely=0.4)
        self.lb_telefone = Label(self.frame1_aba1, text="Telefone", font=("Arial", 10), bg="#dadfe2", fg="#1e3743")
        self.lb_telefone.place(relx=0.6, rely=0.4)
        self.lb_usuario = Label(self.frame1_aba1, text="Usuário", font=("Arial", 10), bg="#dadfe2", fg="#1e3743")
        self.lb_usuario.place(relx=0.05, rely=0.65)
        self.lb_endereco = Label(self.frame1_aba1, text="Endereço", font=("Arial", 10), bg="#dadfe2", fg="#1e3743")
        self.lb_endereco.place(relx=0.3, rely=0.65)
    # criando entrys (caixas de texto)
        self.clie_cod_entry = Entry(self.frame1_aba1)
        self.clie_cod_entry.place(relx=0.05, rely=0.2, relwidth=0.08)
        self.nome_entry = Entry(self.frame1_aba1)
        self.nome_entry.place(relx=0.05, rely=0.5, relwidth=0.2)
        self.registro_entry = Entry(self.frame1_aba1)
        self.registro_entry.place(relx=0.3, rely=0.5, relwidth=0.25)
        self.telefone_entry = Entry(self.frame1_aba1)
        self.telefone_entry.place(relx=0.6, rely=0.5, relwidth=0.2)
        self.usuario_entry = Entry(self.frame1_aba1)
        self.usuario_entry.place(relx=0.05, rely=0.75, relwidth=0.2)
        self.endereco_entry = Entry(self.frame1_aba1)
        self.endereco_entry.place(relx=0.3, rely=0.75, relwidth=0.5)
    # botões, labels e entrys do frame 1 da aba 2
        self.bt_buscar_aba2 = Button(self.frame1_aba2, text="Buscar", bd=2, bg="#4987a3", fg="white", font=("Verdana", 9, "bold "), command=self.buscar_dados_prod)
        self.bt_buscar_aba2.place(relx=0.2, rely=0.2, relwidth=0.1, relheight=0.2)
        self.bt_limpar_aba2 = Button(self.frame1_aba2, text="Limpar", bd=2, bg="#4987a3", fg="white", font=("Verdana", 9, "bold "), command=self.limpar_tela)     
        self.bt_limpar_aba2.place(relx=0.3, rely=0.2, relwidth=0.1, relheight=0.2)
        self.bt_inserir_aba2 = Button(self.frame1_aba2, text="Inserir", bd=2, bg="#4987a3", fg="white", font=("Verdana", 9, "bold "), command=self.inserir_dados)     
        self.bt_inserir_aba2.place(relx=0.5, rely=0.2, relwidth=0.1, relheight=0.2)
        self.bt_atul_aba2 = Button(self.frame1_aba2, text="Atualizar", bd=2, bg="#4987a3", fg="white", font=("Verdana", 9, "bold "), command=self.atualizar_dados)     
        self.bt_atul_aba2.place(relx=0.6, rely=0.2, relwidth=0.1, relheight=0.2)
        self.bt_deletar_aba2 = Button(self.frame1_aba2, text="Deletar", bd=2, bg="#4987a3", fg="white", font=("Verdana", 9, "bold "), command=self.deletar_dados)     
        self.bt_deletar_aba2.place(relx=0.7, rely=0.2, relwidth=0.1, relheight=0.2)
    # criando labels (textos)
        self.lb_cod_prod = Label(self.frame1_aba2, text="Código", font=("Arial", 10), bg="#dadfe2", fg="#1e3743")
        self.lb_cod_prod.place(relx=0.05, rely=0.1)
        self.lb_modelo = Label(self.frame1_aba2, text="Modelo", font=("Arial", 10), bg="#dadfe2", fg="#1e3743")
        self.lb_modelo.place(relx=0.05, rely=0.5)
        self.lb_tamanho = Label(self.frame1_aba2, text="Tamanho", font=("Arial", 10), bg="#dadfe2", fg="#1e3743")
        self.lb_tamanho.place(relx=0.3, rely=0.5)
        self.lb_preco_entry = Label(self.frame1_aba2, text="Preço", font=("Arial", 10), bg="#dadfe2", fg="#1e3743")
        self.lb_preco_entry.place(relx=0.55, rely=0.5)
    # criando entrys (caixas de texto)
        self.prod_cod_entry = Entry(self.frame1_aba2)
        self.prod_cod_entry.place(relx=0.05, rely=0.25, relwidth=0.08)
        self.modelo_entry = Entry(self.frame1_aba2)
        self.modelo_entry.place(relx=0.05, rely=0.7, relwidth=0.2)
        self.tamanho_entry = Entry(self.frame1_aba2)
        self.tamanho_entry.place(relx=0.3, rely=0.7, relwidth=0.2)
        self.preco_entry = Entry(self.frame1_aba2)
        self.preco_entry.place(relx=0.55, rely=0.7, relwidth=0.2)
    # Botões, labels e Entrys de Frame 3 da aba 2
        self.descricao_label = Label(self.frame3_aba2, text="Descrição do Produto", font=("Arial", 10), bg="#dadfe2", fg="#1e3743")
        self.descricao_label.place(relx=0.02, rely=0.02)
        self.descricao_text = Text(self.frame3_aba2)
        self.descricao_text.place(relx=0.02, rely=0.15, relwidth=0.96, relheight=0.8)
        
# craindo listas dentro dos frames
    def widgets_frame2(self):
    # craindo lista no frame 2 da aba 1
        self.lista_clientes = ttk.Treeview(self.frame2_aba1, height=3, columns=("col1", "col2", "col3", "col4", "col5", "col6"))
        self.lista_clientes.heading("#0", text="")
        self.lista_clientes.heading("#1", text="Cód")
        self.lista_clientes.heading("#2", text="Nome")
        self.lista_clientes.heading("#3", text="CPF/CNPJ")
        self.lista_clientes.heading("#4", text="Telefone")
        self.lista_clientes.heading("#5", text="Usuário")
        self.lista_clientes.heading("#6", text="Endereço")
        self.lista_clientes.column("#0", width=1)
        self.lista_clientes.column("#1", width=25)
        self.lista_clientes.column("#2", width=75)
        self.lista_clientes.column("#3", width=100)
        self.lista_clientes.column("#4", width=80)
        self.lista_clientes.column("#5", width=70)
        self.lista_clientes.column("#6", width=200)
        self.lista_clientes.place(relx=0.01, rely=0.05, relwidth=0.95, relheight=0.9)
        self.scrool_lista_cliente = Scrollbar(self.frame2_aba1, orient="vertical")
        self.scrool_lista_cliente.configure(command=self.lista_clientes.yview)
        self.scrool_lista_cliente.place(relx=0.96, rely=0.05, relwidth=0.03, relheight=0.9)
        self.lista_clientes.configure(yscrollcommand=self.scrool_lista_cliente.set)
        self.lista_clientes.bind("<Double-1>", self.duplo_clique)
    # craindo lista no frame 2 da aba 2
        self.lista_produtos = ttk.Treeview(self.frame2_aba2, height=3, columns=("col1", "col2", "col3", "col4"))
        self.lista_produtos.heading("#0", text="")
        self.lista_produtos.heading("#1", text="Cód")
        self.lista_produtos.heading("#2", text="Modelo")
        self.lista_produtos.heading("#3", text="Tamanho")
        self.lista_produtos.heading("#4", text="Preço")
        self.lista_produtos.column("#0", width=1)
        self.lista_produtos.column("#1", width=25)
        self.lista_produtos.column("#2", width=100)
        self.lista_produtos.column("#3", width=75)
        self.lista_produtos.column("#4", width=85)
        self.lista_produtos.place(relx=0.01, rely=0.05, relwidth=0.93, relheight=0.9)
        self.scrool_lista_produtos = Scrollbar(self.frame2_aba2, orient="vertical")
        self.scrool_lista_produtos.configure(command=self.lista_produtos.yview)
        self.scrool_lista_produtos.place(relx=0.94, rely=0.05, relwidth=0.05, relheight=0.9)
        self.lista_produtos.configure(yscrollcommand=self.scrool_lista_produtos.set)
        self.lista_produtos.bind("<Double-1>", self.duplo_clique)
    # criando lista no frame 2 da aba 3 
        self.lista_pedidos = ttk.Treeview(self.frame2_aba3, height=3, columns=("col1", "col2", "col3", "col4", "col5", "col6"))
        self.lista_pedidos.heading("#0", text="")
        self.lista_pedidos.heading("#1", text="Cód Cliente")
        self.lista_pedidos.heading("#2", text="Nome Cliente")
        self.lista_pedidos.heading("#3", text="Cód Produto")
        self.lista_pedidos.heading("#4", text="Nome Produto")
        self.lista_pedidos.heading("#5", text="Data do Pedido")
        self.lista_pedidos.heading("#6", text="Status de Pagamen")
        self.lista_pedidos.column("#0", width=1)
        self.lista_pedidos.column("#1", width=25)
        self.lista_pedidos.column("#2", width=80)
        self.lista_pedidos.column("#3", width=25)
        self.lista_pedidos.column("#4", width=80)
        self.lista_pedidos.column("#5", width=100)
        self.lista_pedidos.column("#6", width=100)
        self.lista_pedidos.place(relx=0.01, rely=0.05, relwidth=0.95, relheight=0.9)
        self.scrool_lista_cliente = Scrollbar(self.frame2_aba3, orient="vertical")
        self.scrool_lista_cliente.configure(command=self.lista_pedidos.yview)
        self.scrool_lista_cliente.place(relx=0.96, rely=0.05, relwidth=0.03, relheight=0.9)
        self.lista_pedidos.configure(yscrollcommand=self.scrool_lista_cliente.set)
        self.lista_pedidos.bind("<Double-1>", self.duplo_clique)

Aplicacao()