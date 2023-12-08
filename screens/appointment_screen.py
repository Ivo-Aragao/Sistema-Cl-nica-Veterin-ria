import tkinter as tk
from tkinter import messagebox
import sqlite3
from validate_docbr import CPF
from tkinter import simpledialog
from PIL import Image, ImageTk

class AppointmentScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Agendamento")
        self.root.geometry("600x500")

        # Defina o ícone da janela
        icon_path = "C:/Users/Ivo/Desktop/backup print2/print2/assets/dog.ico"
        self.root.iconbitmap(icon_path)

        # Adicionar fundo branco
        background_label = tk.Label(self.root, bg="white")
        background_label.place(relwidth=1, relheight=1)

        # Carregar GIF usando Pillow
        gif_path = "C:/Users/Ivo/Desktop/backup print2/print2/assets/animation.gif"
        self.gif = Image.open(gif_path)

        # Adicionar GIF no canto inferior direito
        self.gif_label = tk.Label(self.root, bg="white")
        self.gif_label.place(relx=0.2, rely=0.55)

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
        title_label = tk.Label(self.root, text="Agendamento", font=('Arial', 16, 'bold'), bg="white", bd=1)
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Formulário de agendamento
        # Coluna 1
        col1 = 0

        tutor_name_label = tk.Label(self.root, text="Nome do Tutor:", bg="white", bd=1)
        tutor_name_label.grid(row=1, column=col1)
        self.tutor_name_entry = tk.Entry(self.root)
        self.tutor_name_entry.grid(row=1, column=col1+1)

        cpf_label = tk.Label(self.root, text="CPF:", bg="white", bd=1)
        cpf_label.grid(row=2, column=col1)
        self.cpf_entry = tk.Entry(self.root)
        self.cpf_entry.grid(row=2, column=col1+1)

        address_label = tk.Label(self.root, text="Endereço:", bg="white", bd=1)
        address_label.grid(row=3, column=col1)
        self.address_entry = tk.Entry(self.root)
        self.address_entry.grid(row=3, column=col1+1)

        phone_label = tk.Label(self.root, text="Telefone (11 dígitos):", bg="white", bd=1)
        phone_label.grid(row=4, column=col1)
        self.phone_entry = tk.Entry(self.root)
        self.phone_entry.grid(row=4, column=col1+1)

        # Coluna 2
        col2 = 2

        pet_name_label = tk.Label(self.root, text="Nome do Pet:", bg="white", bd=1)
        pet_name_label.grid(row=1, column=col2)
        self.pet_name_entry = tk.Entry(self.root)
        self.pet_name_entry.grid(row=1, column=col2+1)

        species_label = tk.Label(self.root, text="Espécie:", bg="white", bd=1)
        species_label.grid(row=2, column=col2)
        self.species_entry = tk.Entry(self.root)
        self.species_entry.grid(row=2, column=col2+1)

        breed_label = tk.Label(self.root, text="Raça:", bg="white", bd=1)
        breed_label.grid(row=3, column=col2)
        self.breed_entry = tk.Entry(self.root)
        self.breed_entry.grid(row=3, column=col2+1)

        gender_label = tk.Label(self.root, text="Gênero:", bg="white", bd=1)
        gender_label.grid(row=4, column=col2)
        self.gender_entry = tk.Entry(self.root)
        self.gender_entry.grid(row=4, column=col2+1)

        weight_label = tk.Label(self.root, text="Peso Estimado:", bg="white", bd=1)
        weight_label.grid(row=5, column=col2)
        self.weight_entry = tk.Entry(self.root)
        self.weight_entry.grid(row=5, column=col2+1)

        age_label = tk.Label(self.root, text="Idade:", bg="white", bd=1)
        age_label.grid(row=6, column=col2)
        self.age_entry = tk.Entry(self.root)
        self.age_entry.grid(row=6, column=col2+1)

        # Data e Hora do Agendamento
        date_label = tk.Label(self.root, text="Data do Agendamento (DD-MM-YYYY):", bg="white", bd=1)
        date_label.grid(row=7, column=col1)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=7, column=col1+1)
        self.date_entry.bind("<KeyRelease>", self.auto_insert_hyphen)

        time_label = tk.Label(self.root, text="Horário do Agendamento (HH:MM):", bg="white", bd=1)
        time_label.grid(row=8, column=col1)
        self.time_entry = tk.Entry(self.root)
        self.time_entry.grid(row=8, column=col1+1)
        self.time_entry.bind("<KeyRelease>", self.auto_insert_colon)

        # Botão de agendar
        schedule_button = tk.Button(self.root, text="Agendar", command=self.schedule_appointment, bg="white", bd=1)
        schedule_button.grid(row=9, column=col1, columnspan=2, pady=20)

        # Botão de fechar
        close_button = tk.Button(self.root, text="Fechar", command=self.close_window, bg="white", bd=1)
        close_button.grid(row=9, column=0, columnspan=5, pady=10)

    def auto_insert_hyphen(self, event):
        # Formata a data (DD-MM-YYYY)
        date = self.date_entry.get()
        if len(date) == 2 and event.keysym != "BackSpace":
            self.date_entry.insert(tk.END, "-")
        elif len(date) == 5 and event.keysym != "BackSpace":
            self.date_entry.insert(tk.END, "-")

    def auto_insert_colon(self, event):
        # Formata o horário (HH:MM)
        time = self.time_entry.get()
        if len(time) == 2 and event.keysym != "BackSpace":
            self.time_entry.insert(tk.END, ":")

    def validate_phone(self, phone):
        return phone.isdigit() and len(phone) == 11
    def schedule_appointment(self):
        # Obtém os dados do agendamento dos campos
        tutor_name = self.tutor_name_entry.get()
        cpf = self.cpf_entry.get()
        address = self.address_entry.get()
        phone = self.phone_entry.get()
        pet_name = self.pet_name_entry.get()
        species = self.species_entry.get()
        breed = self.breed_entry.get()
        gender = self.gender_entry.get()
        weight = self.weight_entry.get()
        age = self.age_entry.get()
        date = self.date_entry.get()
        time = self.time_entry.get()

        # Verifica se todos os campos obrigatórios estão preenchidos
        if not (tutor_name and cpf and address and phone and pet_name and species and breed and gender and weight and age and date and time):
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")
            return

        # Validação do CPF
        cpf_validator = CPF()
        if not cpf_validator.validate(cpf):
            messagebox.showerror("Erro", "CPF inválido. Insira um CPF válido.")
            return

        # Validação do telefone
        if not self.validate_phone(phone):
            messagebox.showerror("Erro", "Telefone inválido. Insira um número de telefone com exatamente 11 dígitos.")
            return

        # Formatação do CPF
        formatted_cpf = cpf_validator.mask(cpf)

        # Conecta ao banco de dados SQLite
        conn = sqlite3.connect('agendamentos.db')
        cursor = conn.cursor()

        # Cria uma tabela se ela não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agendamentos (
                id INTEGER PRIMARY KEY,
                tutor_name TEXT,
                cpf TEXT,
                address TEXT,
                phone TEXT,
                pet_name TEXT,
                species TEXT,
                breed TEXT,
                gender TEXT,
                weight TEXT,
                age TEXT,
                date TEXT,
                time TEXT
            )
        ''')

        # Insere os dados do agendamento na tabela
        cursor.execute('''
            INSERT INTO agendamentos (tutor_name, cpf, address, phone, pet_name, species, breed, gender, weight, age, date, time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (tutor_name, formatted_cpf, address, phone, pet_name, species, breed, gender, weight, age, date, time))

        # Commit as alterações e fecha a conexão
        conn.commit()
        conn.close()

        # Exibir uma mensagem de sucesso
        messagebox.showinfo("Agendamento", "Agendamento realizado com sucesso!")

        answer = messagebox.askyesno("Encerrar", "Deseja fazer outro agendamento?")

        if answer:
            # Se sim, limpa os campos e permite novo agendamento
            self.clear_fields()
        else:
            # Se não, fecha a janela
            self.root.destroy()
            
    def clear_fields(self):
        # Limpa os campos do formulário para um novo agendamento
        self.tutor_name_entry.delete(0, tk.END)
        self.cpf_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.pet_name_entry.delete(0, tk.END)
        self.species_entry.delete(0, tk.END)
        self.breed_entry.delete(0, tk.END)
        self.gender_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)

    def close_window(self):
        # Função para fechar a janela
        self.root.destroy()    

if __name__ == "__main__":
    root = tk.Tk()
    app = AppointmentScreen(root)
    root.mainloop()
