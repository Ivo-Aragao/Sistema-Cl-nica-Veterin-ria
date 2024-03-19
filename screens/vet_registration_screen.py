import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

class VetRegistrationScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Veterinários")
        self.root.geometry("400x450")

        # Título
        title_label = tk.Label(self.root, text="Cadastro de Veterinários", font=('Arial', 16, 'bold'))
        title_label.pack(pady=20)

        # Campos de Cadastro
        name_label = tk.Label(self.root, text="Nome Completo:")
        name_label.pack()
        self.name_entry = ttk.Entry(self.root)
        self.name_entry.pack(pady=5)

        birthdate_label = tk.Label(self.root, text="Data de Nascimento:")
        birthdate_label.pack()
        self.birthdate_entry = DateEntry(self.root, date_pattern='dd-mm-yyyy')
        self.birthdate_entry.pack(pady=5)

        address_label = tk.Label(self.root, text="Endereço Residencial:")
        address_label.pack()
        self.address_entry = ttk.Entry(self.root)
        self.address_entry.pack(pady=5)

        phone_label = tk.Label(self.root, text="Número de Telefone:")
        phone_label.pack()
        self.phone_entry = ttk.Entry(self.root)
        self.phone_entry.pack(pady=5)

        email_label = tk.Label(self.root, text="Endereço de E-mail:")
        email_label.pack()
        self.email_entry = ttk.Entry(self.root)
        self.email_entry.pack(pady=5)

        specialty_label = tk.Label(self.root, text="Especialização:")
        specialty_label.pack()
        self.specialty_var = tk.StringVar()
        self.specialty_combobox = ttk.Combobox(self.root, textvariable=self.specialty_var, values=["Cirurgião", "Atendimento Clínico"])
        self.specialty_combobox.pack(pady=5)

        # Botões de Cadastrar e Fechar
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(pady=20)

        register_button = ttk.Button(buttons_frame, text="Cadastrar", command=self.register_vet)
        register_button.grid(row=0, column=0, padx=5)

        close_button = ttk.Button(buttons_frame, text="Fechar", command=self.root.destroy)
        close_button.grid(row=0, column=1, padx=5)

    def register_vet(self):
        # Obter os dados inseridos pelo usuário
        vet_name = self.name_entry.get()
        birthdate = self.birthdate_entry.get()
        address = self.address_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        specialty = self.specialty_var.get()

        # Verificar se todos os campos foram preenchidos
        if not (vet_name and birthdate and address and phone and email and specialty):
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")
            return

        # Inserir os dados no banco de dados
        self.cursor.execute("INSERT INTO veterinarians (name, birthdate, address, phone, email, specialty) VALUES (?, ?, ?, ?, ?, ?)",
                            (vet_name, birthdate, address, phone, email, specialty))
        self.connection.commit()

         # Exibir mensagem de sucesso
        messagebox.showinfo("Cadastro de Veterinários", f"Veterinário {vet_name} cadastrado com sucesso!")
        # Perguntar ao usuário se deseja realizar outro cadastro
        answer = messagebox.askyesno("Novo Cadastro", "Gostaria de realizar outro cadastro?")

        if answer:
            # Se sim, limpar os campos para um novo cadastro
            self.clear_fields()
        else:
            # Se não, fechar a janela
            self.root.destroy()

    def clear_fields(self):
        # Limpa os campos do formulário
        self.name_entry.delete(0, tk.END)
        self.birthdate_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.specialty_combobox.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = VetRegistrationScreen(root)
    root.mainloop()
