from tkinter import *

class View:

    __controller = None

    __root = None

    __frame_menuPrincipal = None

    __listBox_listaDeLinguagens = None

    def __init__(self):#, controller):
        #self.__controller = controller

        self.__root = Tk()
        self.__root.title("T1 INE5421 - Dúnia Marchiori, Vinicius Steffani Schweitzer")
        self.__root.resizable(width=True, height=True)

        #self.__root.minsize(width=800, height=600)

        self.inicializarMenus()

        self.__root.mainloop()

    def inicializarMenus(self):
        self.__frame_menuPrincipal = Frame(self.__root)
        self.__frame_menuPrincipal.configure(background='blue')

        #region Lista de Linguagens

        __frame_listaDeLinguagens = Frame(self.__frame_menuPrincipal, bd=5, relief=SUNKEN)
        __frame_listaDeLinguagens.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=N+S+E+W)
        __frame_listaDeLinguagens.grid_rowconfigure(0, weight=1)
        __frame_listaDeLinguagens.grid_columnconfigure(0, weight=1)
        __frame_listaDeLinguagens.configure(background='red')

        self.__listBox_listaDeLinguagens = Listbox(__frame_listaDeLinguagens)
        self.__listBox_listaDeLinguagens.grid(row=0, column=0, columnspan=3)
        self.__listBox_listaDeLinguagens.grid_rowconfigure(0, weight=1)
        self.__listBox_listaDeLinguagens.grid_columnconfigure(0, weight=1)

        #__button_novaLinguagem = Button(__frame_listaDeLinguagens, text="+")
        #__button_novaLinguagem.grid(row=1, column=0)
        #__button_deletarLinguagem = Button(__frame_listaDeLinguagens, text="-")
        #__button_deletarLinguagem.grid(row=1, column=1)
        #__button_clonarLinguagem = Button(__frame_listaDeLinguagens, text="2x")
        #__button_clonarLinguagem.grid(row=1, column=2)

        #endregion

        #region Opções de Manipulação

        #__frame_opcoesDeManipulacao= Frame(self.__frame_menuPrincipal)
        #__frame_opcoesDeManipulacao.grid(column=1)
        #__frame_opcoesDeManipulacao.grid_rowconfigure(0, weight=1)
        #__frame_opcoesDeManipulacao.grid_columnconfigure(0, weight=3)
        #__frame_opcoesDeManipulacao.configure(background='yellow')

        #endregion

        self.mostrarMenu(True)

    def mostrarMenu(self, mostrar):
        if mostrar:
            self.__frame_menuPrincipal.pack(expand=True)
        else:
            self.__frame_menuPrincipal.pack_forget()

        



view = View()