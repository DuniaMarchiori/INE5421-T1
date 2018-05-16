from tkinter import *


class SelecionaElemento:
	__controller = None

	__root = None

	__frame_menu_principal = None

	__listbox_lista_de_elementos = None

	__parent = None

	__int_elemento_selecionado = None

	def __init__(self, parent):
		self.__parent = parent

	def __inicializar_root(self):
		self.__root = Toplevel(self.__parent)
		self.__root.transient(self.__parent)
		self.__root.title("Seleção de Elemento")
		self.__root.resizable(width=True, height=True)

	def __inicializar_variaveis(self):
		self.__int_elemento_selecionado = -1

	def __inicializar_menus(self, lista_de_opcoes):
		padding = 10
		self.__frame_menu_principal = Frame(self.__root, padx=padding, pady=padding)
		self.__frame_menu_principal.pack()

		l = Label(self.__frame_menu_principal, text="Com qual outro elemento você deseja aplicar a operação escolhida?")
		l.pack()

		self.__listbox_lista_de_elementos = Listbox(self.__frame_menu_principal, selectmode=SINGLE, exportselection=False)
		for elemento in lista_de_opcoes:
			self.__listbox_lista_de_elementos.insert(END, elemento)
		self.__listbox_lista_de_elementos.pack(expand=True, fill=Y)

		b = Button(self.__frame_menu_principal, text="Realizar Operação", command=self.__cb_confirma_operacao)
		b.pack()

	def __mostrar_menu(self, mostrar):
		if mostrar:
			self.__frame_menu_principal.pack(expand=True, fill=BOTH)
		else:
			self.__frame_menu_principal.pack_forget()

	def __cb_confirma_operacao(self):
		selecionado = self.__listbox_lista_de_elementos.curselection()
		if selecionado:
			self.__int_elemento_selecionado = selecionado[0]
		self.close()

	def get_selecionado(self):
		return self.__int_elemento_selecionado

	def get_root(self):
		return self.__root

	def is_showing(self):
		return self.__root is not None

	def show(self, lista_de_opcoes):
		self.__inicializar_root()
		self.__inicializar_menus(lista_de_opcoes)
		self.__mostrar_menu(True)
		self.__root.minsize(width=400, height=300)
		self.__root.protocol("WM_DELETE_WINDOW", self.close)
		self.__root.grab_set()
		self.__parent.wait_window(self.__root)
		return self.get_selecionado()

	def pass_set(self):
		self.__root.grab_set()

	def close(self):
		self.__root.destroy()
		self.__root = None
