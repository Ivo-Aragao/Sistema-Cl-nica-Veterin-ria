import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk

class DonationRegistrationScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Doações")
        self.root.geometry("600x300")

        # Defina o ícone da janela
        icon_path = "assets/dog.ico"
        self.root.iconbitmap(icon_path)

        # Adicionar fundo branco
        background_label = tk.Label(self.root, bg="white")
        background_label.place(relwidth=1, relheight=1)

        # Carregar GIF usando Pillow
        gif_path = "C:/Users/Ivo/Desktop/Projetos Prontos pra uso/Projeto Clinica movelpet/assets/animation2.gif"
        self.gif = Image.open(gif_path)

        # Adicionar GIF no canto inferior direito
        self.gif_label = tk.Label(self.root, bg="white")
        self.gif_label.place(relx=0.6, rely=0)

        self.gif_frames = []
        self.idx = 0
        self.load_gif_frames()

        self.animate_gif()

        self.create_widgets()

    def load_gif_frames(self):
        try:
            i = 0
            while True:
                self.gif.seek(i)
                frame = self.gif.copy()
                self.gif_frames.append(ImageTk.PhotoImage(frame))
                i += 1
        except EOFError:
            pass

    def animate_gif(self):
        self.gif_label.config(image=self.gif_frames[self.idx])
        self.idx += 1
        if self.idx == len(self.gif_frames):
            self.idx = 0
        self.root.after(100, self.animate_gif)

    def create_widgets(self):
        # Título
        title_label = tk.Label(self.root, text="Cadastro de Doações", font=('Arial', 16, 'bold'), bg="white", bd=1)
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Formulário de cadastro de doações
        # Coluna 1
        col1 = 0

        donor_name_label = tk.Label(self.root, text="Nome do Doador:", bg="white", bd=1)
        donor_name_label.grid(row=1, column=col1)
        self.donor_name_entry = tk.Entry(self.root)
        self.donor_name_entry.grid(row=1, column=col1+1)

        donation_type_label = tk.Label(self.root, text="Tipo de Doação:", bg="white", bd=1)
        donation_type_label.grid(row=2, column=col1)
        self.donation_type_entry = tk.Entry(self.root)
        self.donation_type_entry.grid(row=2, column=col1+1)

        donation_description_label = tk.Label(self.root, text="Descrição da Doação:", bg="white", bd=1)
        donation_description_label.grid(row=3, column=col1)
        self.donation_description_entry = tk.Entry(self.root)
        self.donation_description_entry.grid(row=3, column=col1+1)

        donation_date_label = tk.Label(self.root, text="Data da Doação (DD-MM-YYYY):", bg="white", bd=1)
        donation_date_label.grid(row=4, column=col1)
        self.donation_date_entry = tk.Entry(self.root)
        self.donation_date_entry.grid(row=4, column=col1+1)
        self.donation_date_entry.bind("<KeyRelease>", self.auto_insert_hyphen)

        # Botão de cadastrar doação
        register_button = tk.Button(self.root, text="Cadastrar Doação", command=self.register_donation, bg="white", bd=1)
        register_button.grid(row=5, column=col1, columnspan=2, pady=20)

        # Botão de fechar
        close_button = tk.Button(self.root, text="Fechar", command=self.close_window, bg="white", bd=1)
        close_button.grid(row=5, column=1, columnspan=2, pady=10)

    def auto_insert_hyphen(self, event):
        # Função para inserir hífens automaticamente na data (DD-MM-YYYY)
        date = self.donation_date_entry.get()
        if len(date) == 2 and event.keysym != "BackSpace":
            self.donation_date_entry.insert(tk.END, "-")
        elif len(date) == 5 and event.keysym != "BackSpace":
            self.donation_date_entry.insert(tk.END, "-")

    def register_donation(self):
        # Obtém os dados da doação dos campos
        donor_name = self.donor_name_entry.get()
        donation_type = self.donation_type_entry.get()
        donation_description = self.donation_description_entry.get()
        donation_date = self.donation_date_entry.get()

        # Verifica se todos os campos obrigatórios estão preenchidos
        if not (donor_name and donation_type and donation_description and donation_date):
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")
            return

        try:
            # Conecta ao banco de dados SQLite
            conn = sqlite3.connect('doacoes.db')
            cursor = conn.cursor()

            # Cria a tabela de doações se ela não existir
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS doacoes (
                    id INTEGER PRIMARY KEY,
                    donor_name TEXT,
                    donation_type TEXT,
                    donation_description TEXT,
                    donation_date TEXT
                )
            ''')

            # Insere os dados da doação na tabela
            cursor.execute('''
                INSERT INTO doacoes (donor_name, donation_type, donation_description, donation_date)
                VALUES (?, ?, ?, ?)
            ''', (donor_name, donation_type, donation_description, donation_date))

            # Commit as alterações e fecha a conexão
            conn.commit()
            conn.close()

            # Exibir uma mensagem de sucesso
            messagebox.showinfo("Cadastro de Doação", "Doação registrada com sucesso!")

            # Perguntar se o usuário quer fazer outra doação
            self.ask_for_another_donation()

        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", str(e))

        # Limpa os campos após o cadastro
        self.clear_fields()

    def clear_fields(self):
        # Limpa os campos do formulário para um novo cadastro
        if hasattr(self, 'donor_name_entry') and hasattr(self, 'donation_type_entry') \
                and hasattr(self, 'donation_description_entry') and hasattr(self, 'donation_date_entry'):

            # Verifica se o widget ainda existe antes de tentar manipulá-lo
            if self.donor_name_entry.winfo_exists():
                self.donor_name_entry.delete(0, tk.END)

            if self.donation_type_entry.winfo_exists():
                self.donation_type_entry.delete(0, tk.END)

            if self.donation_description_entry.winfo_exists():
                self.donation_description_entry.delete(0, tk.END)

            if self.donation_date_entry.winfo_exists():
                self.donation_date_entry.delete(0, tk.END)


    def ask_for_another_donation(self):
        # Pergunta se o usuário quer fazer outra doação
        response = messagebox.askyesno("Nova Doação", "Deseja fazer outra doação?")
        if response:
            # Limpa os campos para um novo cadastro
            self.donor_name_entry.delete(0, tk.END)
            self.donation_type_entry.delete(0, tk.END)
            self.donation_description_entry.delete(0, tk.END)
            self.donation_date_entry.delete(0, tk.END)
        else:
            # Fecha a janela se o usuário escolher não fazer outra doação
            self.close_window()

    def close_window(self):
        # Função para fechar a janela
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DonationRegistrationScreen(root)
    root.mainloop()
