import tkinter as tk
from tkinter import messagebox
import sqlite3

class AppointmentScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Agendamento")
        self.root.geometry("650x500")

        # Defina o ícone da janela
        icon_path = "C:/Users/Ivo/Desktop/Projetos Prontos pra uso/Projeto Clinica movelpet/assets/dog.ico"
        self.root.iconbitmap(icon_path)

        # Adicionar fundo branco
        background_label = tk.Label(self.root, bg="white")
        background_label.place(relwidth=1, relheight=1)

        # Chame a função para carregar os locais de atendimento disponíveis
        self.load_available_locations()

    def load_available_locations(self):
        # Conecta ao banco de dados SQLite
        conn = sqlite3.connect('clinic_database.db')
        cursor = conn.cursor()

        # Recupera os locais de atendimento disponíveis do banco de dados
        cursor.execute('''
            SELECT DISTINCT location FROM availability
        ''')
        available_locations = cursor.fetchall()

        # Fecha a conexão com o banco de dados
        conn.close()

        # Converte os resultados em uma lista simples
        self.available_locations = [location[0] for location in available_locations]

        if not self.available_locations:
            messagebox.showerror("Erro", "Nenhum local de atendimento disponível.")
            return

        # Cria a variável de controle para a opção de local de atendimento
        self.location_var = tk.StringVar(self.root)
        self.location_var.set(self.available_locations[0])  # Definindo o valor inicial

        # Cria a variável de controle para a opção de data
        self.date_var = tk.StringVar(self.root)

        # Depois de inicializar as variáveis de controle, chame o método create_widgets()
        self.create_widgets()

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

        pet_name_label = tk.Label(self.root, text="Nome do Pet:", bg="white", bd=1)
        pet_name_label.grid(row=5, column=col1)
        self.pet_name_entry = tk.Entry(self.root)
        self.pet_name_entry.grid(row=5, column=col1+1)

        species_label = tk.Label(self.root, text="Espécie:", bg="white", bd=1)
        species_label.grid(row=6, column=col1)
        self.species_entry = tk.Entry(self.root)
        self.species_entry.grid(row=6, column=col1+1)

        breed_label = tk.Label(self.root, text="Raça:", bg="white", bd=1)
        breed_label.grid(row=7, column=col1)
        self.breed_entry = tk.Entry(self.root)
        self.breed_entry.grid(row=7, column=col1+1)

        gender_label = tk.Label(self.root, text="Gênero:", bg="white", bd=1)
        gender_label.grid(row=8, column=col1)
        self.gender_entry = tk.Entry(self.root)
        self.gender_entry.grid(row=8, column=col1+1)

        weight_label = tk.Label(self.root, text="Peso Estimado:", bg="white", bd=1)
        weight_label.grid(row=9, column=col1)
        self.weight_entry = tk.Entry(self.root)
        self.weight_entry.grid(row=9, column=col1+1)

        age_label = tk.Label(self.root, text="Idade:", bg="white", bd=1)
        age_label.grid(row=10, column=col1)
        self.age_entry = tk.Entry(self.root)
        self.age_entry.grid(row=10, column=col1+1)

        pet_disease_label = tk.Label(self.root, text="Doença do Pet:", bg="white", bd=1)
        pet_disease_label.grid(row=11, column=col1)
        self.pet_disease_entry = tk.Entry(self.root)
        self.pet_disease_entry.grid(row=11, column=col1+1)

        # Local de Atendimento
        location_label = tk.Label(self.root, text="Local de Atendimento:", bg="white", bd=1)
        location_label.grid(row=1, column=2)
        self.location_dropdown = tk.OptionMenu(self.root, self.location_var, *self.available_locations, command=self.update_options)
        self.location_dropdown.config(bg="white", bd=1)
        self.location_dropdown.grid(row=1, column=3, pady=10)

        # DateEntry para selecionar a data
        date_label = tk.Label(self.root, text="Data:", bg="white", bd=1)
        date_label.grid(row=2, column=2)
        self.date_dropdown = tk.OptionMenu(self.root, self.date_var, "Selecione uma Data", command=self.update_appointment_options)
        self.date_dropdown.config(bg="white", bd=1)
        self.date_dropdown.grid(row=2, column=3, pady=10)

        # Opções de agendamento
        self.time_var = tk.StringVar(self.root)
        self.time_var.set("Selecione o Horário")
        self.type_var = tk.StringVar(self.root)
        self.type_var.set("Selecione o Tipo de Atendimento")
        self.vet_var = tk.StringVar(self.root)
        self.vet_var.set("Selecione o Veterinário")

        self.time_label = tk.Label(self.root, text="Horário:", bg="white", bd=1)
        self.time_label.grid(row=3, column=2)
        self.time_dropdown = tk.OptionMenu(self.root, self.time_var, "Selecione o Horário")
        self.time_dropdown.config(bg="white", bd=1)
        self.time_dropdown.grid(row=3, column=3, pady=10)

        self.type_label = tk.Label(self.root, text="Tipo de Atendimento:", bg="white", bd=1)
        self.type_label.grid(row=4, column=2)
        self.type_dropdown = tk.OptionMenu(self.root, self.type_var, "Selecione o Tipo de Atendimento")
        self.type_dropdown.config(bg="white", bd=1)
        self.type_dropdown.grid(row=4, column=3, pady=10)

        self.vet_label = tk.Label(self.root, text="Veterinário:", bg="white", bd=1)
        self.vet_label.grid(row=5, column=2)
        self.vet_dropdown = tk.OptionMenu(self.root, self.vet_var, "Selecione o Veterinário")
        self.vet_dropdown.config(bg="white", bd=1)
        self.vet_dropdown.grid(row=5, column=3, pady=10)

        # Botão de agendar
        schedule_button = tk.Button(self.root, text="Agendar", command=self.schedule_appointment, bg="white", bd=1)
        schedule_button.grid(row=12, column=0, columnspan=4, pady=20)

        # Botão de fechar
        close_button = tk.Button(self.root, text="Fechar", command=self.close_window, bg="white", bd=1)
        close_button.grid(row=12, column=2, columnspan=4, pady=10)

        # Atualize as opções quando o local de atendimento for selecionado
        self.update_options()

    def update_options(self, *args):
        # Atualiza as opções de data com base no local de atendimento selecionado
        selected_location = self.location_var.get()

        # Conecta ao banco de dados SQLite
        conn = sqlite3.connect('clinic_database.db')
        cursor = conn.cursor()

        # Recupera as datas disponíveis para o local selecionado
        cursor.execute('''
            SELECT DISTINCT appointment_date FROM availability WHERE location = ?
        ''', (selected_location,))
        available_dates = cursor.fetchall()

        # Fecha a conexão com o banco de dados
        conn.close()

        # Converte as datas em uma lista simples
        available_dates = [date[0] for date in available_dates]

        # Atualiza as opções no menu suspenso de data
        self.date_dropdown['menu'].delete(0, 'end')
        for date in available_dates:
            self.date_dropdown['menu'].add_command(label=date, command=lambda date=date: self.set_date_and_update_options(date))

    def set_date_and_update_options(self, date):
        # Define a data selecionada e atualiza as opções de agendamento
        self.date_var.set(date)
        self.update_appointment_options()

    def update_appointment_options(self, *args):
        # Atualiza as opções de horário, tipo de atendimento e veterinário com base na data selecionada
        selected_date = self.date_var.get()

        # Verifica se a data está selecionada
        if not selected_date:
            return

        # Recupera o local de atendimento selecionado
        location = self.location_var.get()

        conn = sqlite3.connect('clinic_database.db')
        cursor = conn.cursor()

        # Recupera os horários disponíveis para o local e data selecionados
        cursor.execute('''
            SELECT DISTINCT time FROM availability WHERE location = ? AND appointment_date = ?
        ''', (location, selected_date))
        available_times = cursor.fetchall()

        # Recupera os tipos de atendimento disponíveis para o local e data selecionados
        cursor.execute('''
            SELECT DISTINCT service FROM availability WHERE location = ? AND appointment_date = ?
        ''', (location, selected_date))
        available_services = cursor.fetchall()

        # Recupera os veterinários disponíveis para o local e data selecionados
        cursor.execute('''
            SELECT DISTINCT vet FROM availability WHERE location = ? AND appointment_date = ?
        ''', (location, selected_date))
        available_vets = cursor.fetchall()

        # Fecha a conexão com o banco de dados
        conn.close()

        # Atualiza as opções nos menus suspensos
        self.time_dropdown['menu'].delete(0, 'end')
        for time in available_times:
            self.time_dropdown['menu'].add_command(label=time[0], command=lambda time=time[0]: self.time_var.set(time))

        self.type_dropdown['menu'].delete(0, 'end')
        for service in available_services:
            self.type_dropdown['menu'].add_command(label=service[0], command=lambda service=service[0]: self.type_var.set(service))

        self.vet_dropdown['menu'].delete(0, 'end')
        for vet in available_vets:
            self.vet_dropdown['menu'].add_command(label=vet[0], command=lambda vet=vet[0]: self.vet_var.set(vet))

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
        pet_disease = self.pet_disease_entry.get()
        location = self.location_var.get()
        appointment_date = self.date_var.get()  # Obter a data selecionada corretamente
        time = self.time_var.get()
        service = self.type_var.get()
        vet = self.vet_var.get()

        # Verifica se todos os campos obrigatórios estão preenchidos
        if not (tutor_name and cpf and address and phone and pet_name and species and breed and gender and weight and age and pet_disease and location and appointment_date and time and service and vet):
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")
            return

        # Verifica se já existe um agendamento para o horário fornecido
        if self.appointment_exists(appointment_date, time):
            messagebox.showerror("Erro", "Já existe um agendamento para este horário. Escolha outro horário.")
            return

        # Conecta ao banco de dados SQLite
        conn = sqlite3.connect('clinic_database.db')
        cursor = conn.cursor()

        # Insere os dados do agendamento na tabela
        cursor.execute('''
            INSERT INTO agendamentos (tutor_name, cpf, address, phone, pet_name, species, breed, gender, weight, age, pet_disease, location, appointment_date, time, service, vet)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (tutor_name, cpf, address, phone, pet_name, species, breed, gender, weight, age, pet_disease, location, appointment_date, time, service, vet))

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

    def appointment_exists(self, appointment_date, time):
        # Verifica se já existe um agendamento para a data e horário fornecidos
        conn = sqlite3.connect('clinic_database.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM agendamentos
            WHERE appointment_date = ? AND time = ?
        ''', (appointment_date, time))

        existing_appointment = cursor.fetchone()

        conn.close()

        return existing_appointment is not None

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
        self.pet_disease_entry.delete(0, tk.END)
        self.location_var.set("Selecione o Local de Atendimento")
        self.date_var.set("Selecione uma Data")
        self.time_var.set("Selecione o Horário")
        self.type_var.set("Selecione o Tipo de Atendimento")
        self.vet_var.set("Selecione o Veterinário")

    def close_window(self):
        # Função para fechar a janela
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AppointmentScreen(root)
    root.mainloop()
