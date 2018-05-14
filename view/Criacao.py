from tkinter import *
from tkinter import ttk

class Criacao:

    __controller = None
    
    __frame_menu_principal = None

    def __init__(self, controller):
        self.__controller = controller
        self.__inicializar_root()
        self.__inicializar_menus()
        self.mostrar_menu(True)
        self.__root.minsize(width=400, height=200)
        self.__root.mainloop()

    def __inicializar_root(self):
        self.__root = Tk()
        self.__root.title("Criação de Elemento")
        self.__root.resizable(width=True, height=True)

    def __inicializar_menus(self):
        padding = 10
        self.__frame_menu_principal = Frame(self.__root, padx=padding, pady=padding)
        self.__frame_menu_principal.pack()
        notebook_abas_de_elementos = ttk.Notebook(self.__frame_menu_principal)
        notebook_abas_de_elementos.pack(expand=True, fill=BOTH)
        self.__inicializar_aba_gramatica(notebook_abas_de_elementos)
        self.__inicializar_aba_expressao(notebook_abas_de_elementos)

    def __inicializar_aba_gramatica(self, notebook):
        self.__criar_aba_generica(notebook, "Gramática Regular")

    def __inicializar_aba_expressao(self, notebook):
        self.__criar_aba_generica(notebook, "Expressão Regular")

    def __criar_aba_generica(self, notebook, elemento):
        aba_elemento = ttk.Frame(notebook)
        notebook.add(aba_elemento, text=elemento)

        padding = 5
        frame_elemento = Frame(aba_elemento, padx=padding, pady=padding)
        frame_elemento.pack(expand=True, fill=BOTH)
        frame_text_area = Frame(frame_elemento, padx=padding, pady=padding)
        frame_text_area.pack(expand=True, fill=BOTH)

        text_elemento = Text(frame_text_area, width=0, height=0)
        text_elemento.pack(expand=True, fill=BOTH, side=LEFT)

        scrollbar_elemento = Scrollbar(frame_text_area, command=text_elemento.yview)
        text_elemento['yscrollcommand'] = scrollbar_elemento.set
        scrollbar_elemento.pack(fill=Y, side=LEFT)

        Button(frame_elemento, text="Adicionar Nova " + elemento).pack()

    def mostrar_menu(self, mostrar):
        if mostrar:
            self.__frame_menu_principal.pack(expand=True, fill=BOTH)
        else:
            self.__frame_menu_principal.pack_forget()