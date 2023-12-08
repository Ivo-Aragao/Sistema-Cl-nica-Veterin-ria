import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
  

class PlaceholderEntry(ttk.Entry):
    def __init__(self, master=None, placeholder="", color='gray', show=None):
        super().__init__(master)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['foreground']
        self.show = show
        self.is_placeholder = True

        self.bind("<FocusIn>", self.on_entry_click)
        self.bind("<FocusOut>", self.on_focus_out)

        self.put_placeholder()

    def on_entry_click(self, event):
        if self.is_placeholder:
            self.delete(0, "end")
            self['foreground'] = self.default_fg_color
            self.config(show=self.show)
            self.is_placeholder = False

    def on_focus_out(self, event):
        if not self.get():
            self.put_placeholder()

    def put_placeholder(self):
        self.delete(0, "end")
        self.insert(0, self.placeholder)
        self['foreground'] = self.placeholder_color
        self.config(show='')

class LoginScreen:
    def __init__(self, root, on_login_success, get_image_path_func):
        self.root = root
        self.on_login_success = on_login_success
        self.get_image_path = get_image_path_func
        self.root.geometry("1500x800")

        # Defina o ícone da janela
        icon_path = get_image_path_func("dog.ico")
        self.root.iconbitmap(icon_path)

         # Defina o título da janela
        root.title("Tela de Login")

        try:
            image_path = self.get_image_path("clini2.jpeg")
            self.background_image = Image.open(image_path)
            self.background_photo = ImageTk.PhotoImage(self.background_image)
        except FileNotFoundError:
            messagebox.showerror("Erro", "Imagem de fundo não encontrada")
            return

        self.create_widgets()

    def create_widgets(self):
        # Parte Esquerda (Imagem)
        background_label = ttk.Label(self.root, image=self.background_photo)
        background_label.place(relx=0.25, rely=0.5, anchor='center')

        # Parte Direita (Fundo branco com widgets)
        frame_right = ttk.Frame(self.root, width=670, height=750, style='Right.TFrame')
        frame_right.place(relx=0.75, rely=0.5, anchor='center')

        # Estilo para o frame da parte direita
        style = ttk.Style(self.root)
        style.configure('Right.TFrame', background='white')

        # Rótulo de plano de fundo para o nome "Clinica Movel" (parte direita)
        background_text_label = tk.Label(frame_right, text="Clinica Movel", font=('Arial', 45, 'bold'), foreground='black', background='white')
        background_text_label.place(relx=0.5, rely=0.30, anchor='center')

        # Rótulo para "Usuário" (parte direita)
        user_label = tk.Label(frame_right, text="Usuário:", font=('Arial', 17), background='white')
        user_label.place(relx=0.465, rely=0.385, anchor='center')

        # Campo de Email com texto de dica (parte direita)
        self.email_entry = PlaceholderEntry(frame_right, "Email", color='gray')
        self.email_entry.place(relx=0.5, rely=0.425, anchor='center')

        # Rótulo para "Senha" (parte direita)
        password_label = tk.Label(frame_right, text="Senha:", font=('Arial', 17), background='white')
        password_label.place(relx=0.458, rely=0.48, anchor='center')

        # Campo de Senha com texto de dica (parte direita)
        self.password_entry = PlaceholderEntry(frame_right, "Password", color='gray', show='*')
        self.password_entry.place(relx=0.5, rely=0.52, anchor='center')

        # Botão de login (parte direita)
        login_button = ttk.Button(frame_right, text="Entrar", command=self.login)
        login_button.place(relx=0.5, rely=0.6, anchor='center')

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Implemente sua lógica de login aqui, comparando email e senha com credenciais válidas
        if email == "ivo" and password == "123":
            messagebox.showinfo("Login", "Login bem-sucedido!")

            # Login bem-sucedido, fecha a janela de login
            self.root.withdraw()

            # Chame a função de retorno para mostrar a tela de opções
            self.on_login_success()
        else:
            messagebox.showerror("Erro", "Email ou senha incorretos")

# Exemplo de uso
def on_login_success():
    print("Login bem-sucedido. Você pode prosseguir para a próxima tela.")

if __name__ == "__main__":
    root = tk.Tk()
    
    login_screen = LoginScreen(root, on_login_success)

    # Estilo para o frame da parte direita
    style = ttk.Style()
    style.configure('Right.TFrame', background='white')

    root.mainloop()