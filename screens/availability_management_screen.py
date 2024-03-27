import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import sqlite3
from datetime import datetime

class AvailabilityManagementScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciamento de Disponibilidade")
        self.root.geometry("600x650")  # Aumentei a altura para acomodar o novo campo

        icon_path = "./assets/dog.ico"  # Substitua pelo caminho real do ícone
        self.root.iconbitmap(icon_path)

        # Conexão com o banco de dados SQLite
        self.connection = sqlite3.connect('clinic_database.db')
        self.cursor = self.connection.cursor()

        # Verifica e adiciona a coluna location à tabela availability, se ainda não existir
        self.check_and_add_location_column()

        # Remove as datas expiradas do banco de dados
        self.remove_expired_dates()

        # Título
        title_label = tk.Label(self.root, text="Gerenciamento de Disponibilidade", font=('Arial', 16, 'bold'))
        title_label.pack(pady=20)

        # Calendário para seleção de data
        date_label = tk.Label(self.root, text="Selecione uma Data:")
        date_label.pack()
        self.calendar = Calendar(self.root, selectmode='day')
        self.calendar.pack(pady=10)

        # Horários disponíveis
        time_label = tk.Label(self.root, text="Horários Disponíveis:")
        time_label.pack()
        self.time_entry = ttk.Entry(self.root)
        self.time_entry.pack(pady=10)
        self.time_entry.config(validate="key", validatecommand=(self.root.register(self.validate_time_entry), "%P"))

        # Tipos de Atendimento
        service_label = tk.Label(self.root, text="Tipos de Atendimento:")
        service_label.pack()
        self.service_entry = ttk.Entry(self.root)
        self.service_entry.pack(pady=10)

        # Veterinários Disponíveis
        vet_label = tk.Label(self.root, text="Veterinários Disponíveis:")
        vet_label.pack()
        self.vet_var = tk.StringVar()
        self.vet_dropdown = ttk.Combobox(self.root, textvariable=self.vet_var)
        self.vet_dropdown.pack(pady=10)
        self.populate_vet_dropdown()

        # Local de Atendimento
        location_label = tk.Label(self.root, text="Local de Atendimento:")
        location_label.pack()
        self.location_entry = ttk.Entry(self.root)
        self.location_entry.pack(pady=10)

        # Frame para botões
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        # Botão para adicionar disponibilidade
        add_button = tk.Button(button_frame, text="Adicionar Disponibilidade", command=self.add_availability)
        add_button.pack(side=tk.LEFT, padx=10)

        # Botão para fechar a tela
        close_button = tk.Button(button_frame, text="Fechar", command=self.root.destroy)
        close_button.pack(side=tk.LEFT, padx=10)

    def check_and_add_location_column(self):
        # Verifica se a coluna 'location' já existe na tabela 'availability'
        self.cursor.execute("PRAGMA table_info(availability)")
        table_info = self.cursor.fetchall()
        location_column_exists = any('location' in column_info for column_info in table_info)
        if not location_column_exists:
            # Adiciona a coluna 'location' à tabela 'availability'
            self.cursor.execute("ALTER TABLE availability ADD COLUMN location TEXT")
            self.connection.commit()
            print("Coluna 'location' adicionada com sucesso.")

    def remove_expired_dates(self):
        # Verificar se a coluna 'appointment_date' existe na tabela 'availability'
        self.cursor.execute("PRAGMA table_info(availability)")
        table_info = self.cursor.fetchall()
        date_column_exists = any('appointment_date' in column_info for column_info in table_info)

        # Se a coluna 'appointment_date' existir, remover as datas expiradas do banco de dados (datas anteriores ao dia atual)
        if date_column_exists:
            current_date = datetime.now().date()
            self.cursor.execute("DELETE FROM availability WHERE appointment_date < ?", (current_date,))
            self.connection.commit()
        else:
            print("A coluna 'appointment_date' não existe na tabela 'availability'.")

    def populate_vet_dropdown(self):
        # Recupera a lista de veterinários do banco de dados e popula a caixa de seleção
        self.cursor.execute("SELECT name FROM veterinarians")
        vet_names = self.cursor.fetchall()
        self.vet_dropdown['values'] = [vet[0] for vet in vet_names]

    def validate_time_entry(self, new_text):
        # Valida o formato do horário (ex: "09:00") e limita a entrada a cinco caracteres
        if len(new_text) > 5:
            return False
        if not new_text:
            return True
        if len(new_text) in [3]:
            if new_text[-1] != ':':
                self.time_entry.insert(tk.END, ':')
            return True
        if len(new_text) == 5:
            try:
                hour, minute = map(int, new_text.split(':'))
                if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                    return False
            except ValueError:
                return False
        return True

    def add_availability(self):
        # Obter os dados inseridos pelo usuário
        selected_date = self.calendar.get_date()
        selected_time = self.time_entry.get()
        selected_service = self.service_entry.get()
        selected_vet = self.vet_var.get()
        selected_location = self.location_entry.get()  # Obtendo o valor do local de atendimento

        # Verificar se todos os campos foram preenchidos
        if not (selected_date and selected_time and selected_service and selected_vet and selected_location):
            messagebox.showerror("Erro", "Preencha todos os campos para adicionar a disponibilidade.")
            return

        # Inserir os dados no banco de dados
        self.cursor.execute("INSERT INTO availability (appointment_date, time, service, vet, location) VALUES (?, ?, ?, ?, ?)",
                            (selected_date, selected_time, selected_service, selected_vet, selected_location))
        self.connection.commit()

        # Exibir os dados inseridos
        messagebox.showinfo("Dados de Disponibilidade", f"Data: {selected_date}\nHorário: {selected_time}\nTipo de Atendimento: {selected_service}\nVeterinário: {selected_vet}\nLocal de Atendimento: {selected_location}")

        # Perguntar ao usuário se deseja realizar outro cadastro
        answer = messagebox.askyesno("Disponibilizar outra data", "Gostaria de disponibilizar outra data?")

        if answer:
            # Se sim, limpar os campos para um novo cadastro
            self.clear_fields()
        else:
            # Se não, fechar a janela
            self.root.destroy()

    def clear_fields(self):
        # Limpar todos os campos de entrada para um novo cadastro
        self.calendar.set_date('')
        self.time_entry.delete(0, tk.END)
        self.service_entry.delete(0, tk.END)
        self.vet_dropdown.set('')
        self.location_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = AvailabilityManagementScreen(root)
    root.mainloop()
