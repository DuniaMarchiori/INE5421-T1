from tkinter import *
from tkinter import ttk
from model.Gramatica import Gramatica
from model.Expressao import Expressao
from model.AF.AutomatoFinito import AutomatoFinito
from view.Criacao import Criacao


class View:

    __controller = None

    __root = None
    __frame_menu_principal = None

    __listbox_lista_de_linguagens = None

    __button_nova_linguagem = None
    __button_deletar_linguagem = None
    __button_clonar_linguagem = None

    __frame_manipulacao_elemento = None
    __frame_elemento_nulo = None
    __notebook_abas_de_representacao = None

    __frame_gr_operacao = None
    __frame_gr_transformacao = None

    __frame_er_operacao = None
    __frame_er_transformacao = None

    __frame_af_operacao = None
    __frame_af_transformacao = None

    __tipo_linguagem_atual = None

    __popup_novo_elemento = None

    def __init__(self, controller):
        self.__controller = controller
        self.__inicializar_root()
        self.__inicializar_variaveis()
        self.__inicializar_menubar()
        self.__inicializar_menus()
        self.atualiza_operacao(Gramatica())
        self.mostrar_menu(True)

    def __inicializar_variaveis(self):
        self.__popup_novo_elemento = Criacao(self.__root, self.__controller)
        self.__tipo_linguagem_atual = StringVar()

    def __inicializar_root(self):
        self.__root = Tk()
        self.__root.title("T1 INE5421 - Dúnia Marchiori, Vinicius Steffani Schweitzer")
        self.__root.resizable(width=True, height=True)
        self.__root.minsize(width=800, height=600)
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)
        self.__root.protocol("WM_DELETE_WINDOW", sys.exit)

    def __inicializar_menubar(self):
        menu_main = Menu(self.__root)

        menu_arquivo = Menu(menu_main, tearoff=0)
        menu_arquivo.add_command(label="Abrir", command=print("Abrir"))
        menu_arquivo.add_command(label="Salvar", command=print("Salvar"))

        menu_main.add_cascade(label="Arquivo", menu=menu_arquivo)
        menu_main.add_command(label="Sobre", command=print("Sobre"))

        # TODO DEBUG remover botões de debug
        menu_main.add_command(label="Debug", command=self.debug)
        menu_main.add_command(label="Debug2", command=self.debug2)

        self.__root.configure(menu=menu_main)

    def __configura_elemento(self, elemento, row=0, column=0, rowspan=1, columnspan=1, rowweight=1, columnweight=1,sticky=N+S+E+W):
        elemento.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky)
        elemento.master.grid_rowconfigure(row, weight=rowweight)
        elemento.master.grid_columnconfigure(column, weight=columnweight)

    def __inicializar_menus(self):
        self.__frame_menu_principal = Frame(self.__root)
        self.__configura_elemento(self.__frame_menu_principal)

        self.__inicializa_lista_de_linguagens()
        self.__inicializa_opcoes_de_manipulacao()

    def __inicializa_lista_de_linguagens(self):
        frame_lista_de_linguagens = LabelFrame(self.__frame_menu_principal, bd=5, relief=SUNKEN, text="Elementos")
        self.__configura_elemento(frame_lista_de_linguagens, row=0, column=0)
        frame_lista_de_linguagens.configure(background='green')

        self.__listbox_lista_de_linguagens = Listbox(frame_lista_de_linguagens, selectmode=BROWSE, bd=5, relief=SUNKEN)
        self.__configura_elemento(self.__listbox_lista_de_linguagens, row=1, column=0, rowspan=1, columnspan=3)
        self.__listbox_lista_de_linguagens.bind('<<ListboxSelect>>', self.seleciona_lista)
        self.__listbox_lista_de_linguagens.configure(background='red')

        self.__button_nova_linguagem = Button(frame_lista_de_linguagens, text="Novo", command=self.abrir_janela_novo_elemento)
        self.__configura_elemento(self.__button_nova_linguagem, row=0, column=0, rowweight=0, columnweight=1)
        self.__button_deletar_linguagem = Button(frame_lista_de_linguagens, text="Remover", command=self.remover_elemento_da_lista)
        self.__configura_elemento(self.__button_deletar_linguagem, row=0, column=1, rowweight=0, columnweight=1)
        self.__button_clonar_linguagem = Button(frame_lista_de_linguagens, text="Duplicar")
        self.__configura_elemento(self.__button_clonar_linguagem, row=0, column=2, rowweight=0, columnweight=1)

    def __inicializa_opcoes_de_manipulacao(self):
        frame_opcoes_de_manipulacao = LabelFrame(self.__frame_menu_principal, bd=5, relief=SUNKEN, text="Manipulações")
        self.__configura_elemento(frame_opcoes_de_manipulacao, row=0, column=1, columnweight=5)
        frame_opcoes_de_manipulacao.configure(background='brown')

        # region Frame sem elemento selecionado
        self.__frame_elemento_nulo = Frame(frame_opcoes_de_manipulacao, bd=5, relief=SUNKEN)
        self.__configura_elemento(self.__frame_elemento_nulo)
        self.__inicializa_tela_sem_selecionado()
        self.__frame_elemento_nulo.configure(background='pink')
        self.__frame_elemento_nulo.grid_remove()
        # endregion

        # region Notebook com as abas
        self.__frame_manipulacao_elemento = LabelFrame(frame_opcoes_de_manipulacao, bd=5, relief=SUNKEN, text="ER")
        self.__configura_elemento(self.__frame_manipulacao_elemento)
        self.__frame_manipulacao_elemento.configure(background='purple')
        self.__frame_manipulacao_elemento.grid_remove()

        self.__notebook_abas_de_representacao = ttk.Notebook(self.__frame_manipulacao_elemento)
        self.__notebook_abas_de_representacao.pack(expand=True, fill=BOTH)

        aba_gramatica = ttk.Frame(self.__notebook_abas_de_representacao)
        self.__notebook_abas_de_representacao.add(aba_gramatica, text='Gramática Regular')
        frame_gramatica = Frame(aba_gramatica, bd=5, relief=SUNKEN)
        frame_gramatica.configure(background='yellow')
        self.__configura_elemento(frame_gramatica)

        aba_expressao = ttk.Frame(self.__notebook_abas_de_representacao)
        self.__notebook_abas_de_representacao.add(aba_expressao, text='Expressão Regular')
        frame_expressao = Frame(aba_expressao, bd=5, relief=SUNKEN)
        frame_expressao.configure(background='green')
        self.__configura_elemento(frame_expressao)

        aba_automato = ttk.Frame(self.__notebook_abas_de_representacao)
        self.__notebook_abas_de_representacao.add(aba_automato, text='Automato Finito')
        frame_automato = Frame(aba_automato, bd=5, relief=SUNKEN)
        frame_automato.configure(background='cyan')
        self.__configura_elemento(frame_automato)
        # endregion

        # region Inicializa frames de GR
        self.__frame_gr_operacao = Frame(frame_gramatica, bd=5, relief=SUNKEN)
        self.__configura_elemento(self.__frame_gr_operacao)
        self.__inicializa_tela_gr_operacao()
        self.__frame_gr_operacao.grid_remove()
        self.__frame_gr_operacao.configure(background='green')

        self.__frame_gr_transformacao = Frame(frame_gramatica, bd=5, relief=SUNKEN)
        self.__configura_elemento(self.__frame_gr_transformacao)
        self.__inicializa_tela_gr_transformacao()
        self.__frame_gr_transformacao.configure(background='green')
        # endregion

        # region Inicializa frames de GR
        self.__frame_er_operacao = Frame(frame_expressao, bd=5, relief=SUNKEN)
        self.__configura_elemento(self.__frame_er_operacao)
        self.__inicializa_tela_er_operacao()
        self.__frame_er_operacao.grid_remove()
        self.__frame_er_operacao.configure(background='green')

        self.__frame_er_transformacao = Frame(frame_expressao, bd=5, relief=SUNKEN)
        self.__configura_elemento(self.__frame_er_transformacao)
        self.__inicializa_tela_er_transformacao()
        self.__frame_er_transformacao.configure(background='green')
        # endregion

        # region Inicializa frames de GR
        self.__frame_af_operacao = Frame(frame_automato, bd=5, relief=SUNKEN)
        self.__configura_elemento(self.__frame_af_operacao)
        self.__inicializa_tela_af_operacao()
        self.__frame_af_operacao.grid_remove()
        self.__frame_af_operacao.configure(background='green')

        self.__frame_af_transformacao = Frame(frame_automato, bd=5, relief=SUNKEN)
        self.__configura_elemento(self.__frame_af_transformacao)
        self.__inicializa_tela_af_transformacao()
        self.__frame_af_transformacao.configure(background='green')
        # endregion

    def __inicializa_tela_gr_operacao(self):
        l = Label(self.__frame_gr_operacao, text="GrOP")
        l.pack()

    def __inicializa_tela_gr_transformacao(self):
        f = Frame(self.__frame_gr_transformacao)
        f.pack(expand=True)
        l = Label(f, text="Você precisa transformar esse elemento em uma gramática regular primeiro")
        l.pack()
        b = Button(f, text="Transformar")
        b.pack()

    def __inicializa_tela_er_operacao(self):
        l = Label(self.__frame_er_operacao, text="ErOP")
        l.pack()

    def __inicializa_tela_er_transformacao(self):
        f = Frame(self.__frame_er_transformacao)
        f.pack(expand=True)
        l = Label(f, text="Você precisa transformar esse elemento em uma expressão regular primeiro")
        l.pack()
        b = Button(f, text="Transformar")
        b.pack()

    def __inicializa_tela_af_operacao(self):
        l = Label(self.__frame_af_operacao, text="AfOP")
        l.pack()

    def __inicializa_tela_af_transformacao(self):
        f = Frame(self.__frame_af_transformacao)
        f.pack(expand=True)
        l = Label(f, text="Você precisa transformar esse elemento em um automato finito primeiro")
        l.pack()
        b = Button(f, text="Transformar")
        b.pack()

    def __inicializa_tela_sem_selecionado(self):
        f = Frame(self.__frame_elemento_nulo)
        f.pack(expand=True)
        l = Label(f, text="Você não possui nenhum elemento selecionado\n"
                          "Crie um novo no painel à esquerda ou selecione um já criado")
        l.pack()
    
    def __estado_botoes_da_lista(self, estado=True):
        state = NORMAL
        if not estado:
            state = DISABLED
        self.__button_deletar_linguagem['state'] = state
        self.__button_clonar_linguagem['state'] = state

    def __altera_tela_operacao(self, num_tela):
        if num_tela == 0:
            self.__frame_manipulacao_elemento.grid_remove()
            self.__frame_elemento_nulo.grid()
        else:
            self.__frame_elemento_nulo.grid_remove()
            self.__frame_manipulacao_elemento.grid()

            if num_tela == 1:  # GR Existe
                self.__frame_gr_transformacao.grid_remove()
                self.__frame_gr_operacao.grid()
            else:  # GR Transforma
                self.__frame_gr_operacao.grid_remove()
                self.__frame_gr_transformacao.grid()

            if num_tela == 2:  # ER Existe
                self.__frame_er_transformacao.grid_remove()
                self.__frame_er_operacao.grid()
            else:  # ER Transforma
                self.__frame_er_operacao.grid_remove()
                self.__frame_er_transformacao.grid()

            if num_tela == 3:  # AF Existe
                self.__frame_af_transformacao.grid_remove()
                self.__frame_af_operacao.grid()
            else:  # AF Transforma
                self.__frame_af_operacao.grid_remove()
                self.__frame_af_transformacao.grid()

    def atualiza_operacao(self, elemento_selecionado):
        if elemento_selecionado is not None:
            self.__estado_botoes_da_lista(estado=True)
            if isinstance(elemento_selecionado, Gramatica):
                self.__altera_tela_operacao(1)
                self.__frame_manipulacao_elemento.configure(text="Gramática Regular")
            if isinstance(elemento_selecionado, Expressao):
                self.__altera_tela_operacao(2)
                self.__frame_manipulacao_elemento.configure(text="Expressão Regular")
            if isinstance(elemento_selecionado, AutomatoFinito):
                self.__altera_tela_operacao(3)
                self.__frame_manipulacao_elemento.configure(text="Automato Finito")
        else:
            self.__altera_tela_operacao(0)
            self.__estado_botoes_da_lista(estado=False)

    def seleciona_lista(self, event):
        print("Selecionei")

    def adicionar_elemento_na_lista(self, nome_do_elemento):
        self.__listbox_lista_de_linguagens.insert(END, nome_do_elemento)

    def remover_elemento_da_lista(self):
        indice = self.__listbox_lista_de_linguagens.curselection()
        self.__listbox_lista_de_linguagens.delete(indice)
        self.atualiza_operacao(None)

    def abrir_janela_novo_elemento(self):
        if not self.__popup_novo_elemento.is_showing():
            self.__popup_novo_elemento.show()

    def mostrar_aviso(self, aviso):
        print(aviso)
        #TODO Janela popup com o erro

    def mostrar_menu(self, mostrar):
        if mostrar:
            self.__frame_menu_principal.pack(expand=True, fill=BOTH)
        else:
            self.__frame_menu_principal.pack_forget()

    def start(self):
        self.__root.mainloop()




    def debug(self):
        popup = Tk()
        v = StringVar()

        e = Entry(popup, textvariable=v)
        e.pack()
        b = Button(popup, text="OK", command=lambda: self.__altera_tela_operacao(int(e.get())))
        b.pack()

    def debug2(self):
        popup = Tk()

        e = Entry(popup, text="asd")
        e.pack()
        b = Button(popup, text="OK", command=lambda: self.__tipo_linguagem_atual.set(e.get()))
        b.pack()