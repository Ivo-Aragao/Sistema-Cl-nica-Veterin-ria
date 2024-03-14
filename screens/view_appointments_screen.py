import tkinter as tk
from tkcalendar import DateEntry
import sqlite3
from tkinter import ttk, messagebox, filedialog  # Adicione filedialog
from reportlab.pdfgen import canvas  # Adicione esta linha
import shutil
import os

class ViewAppointmentsScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizar Agendamentos por Data")
        self.root.geometry("800x400")

        # Configurar o layout para que as colunas e linhas se expandam
        for i in range(6):
            self.root.columnconfigure(i, weight=1)
        self.root.rowconfigure(2, weight=1)
        
        # Defina o ícone da janela
        icon_path = "C:/Users/Ivo/Desktop/backup print2/print2/assets/dog.ico"  # Substitua pelo caminho real do ícone
        self.root.iconbitmap(icon_path)

        self.create_widgets()

    def create_widgets(self):
        # Título
        title_label = tk.Label(self.root, text="Visualizar Agendamentos por Data", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=6, pady=20)

        # Data de consulta
        date_label = tk.Label(self.root, text="Data (DD-MM-YYYY):")
        date_label.grid(row=1, column=0)

        # Use o DateEntry para a entrada de data
        self.date_entry = DateEntry(self.root, date_pattern="dd-mm-yyyy")
        self.date_entry.grid(row=1, column=1)
        search_button = tk.Button(self.root, text="Buscar", command=self.search_appointments)
        search_button.grid(row=1, column=2)

        # Tabela de agendamentos
        columns = ("ID", "Tutor", "CPF", "Pet", "Espécie", "Raça", "Gênero", "Horário")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)  # Defina a largura da coluna
        self.tree.grid(row=2, column=0, columnspan=6, sticky='nsew')  # Use sticky para preencher a célula
        self.tree.bind("<Double-1>", self.on_item_double_click)

        # Botões de ação
        edit_button = tk.Button(self.root, text="Editar", command=self.edit_appointment)
        edit_button.grid(row=3, column=0)
        delete_button = tk.Button(self.root, text="Excluir", command=self.delete_appointment)
        delete_button.grid(row=3, column=1)

        # Botão de fechar
        close_button = tk.Button(self.root, text="Fechar", command=self.root.destroy)
        close_button.grid(row=3, column=2)

        # Botão de ação para gerar PDF
        pdf_button = tk.Button(self.root, text="Gerar PDF", command=self.choose_destination_and_generate_pdf)
        pdf_button.grid(row=3, column=3)

        backup_button = tk.Button(self.root, text="Backup do Banco de Dados", command=self.choose_backup_destination_and_backup)
        backup_button.grid(row=3, column=4)

    def search_appointments(self):
        date = self.date_entry.get()
        conn = sqlite3.connect('agendamentos.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, tutor_name, cpf, pet_name, species, breed, gender, time FROM agendamentos WHERE date = ?', (date,))
        appointments = cursor.fetchall()
        conn.close()

        for record in self.tree.get_children():
            self.tree.delete(record)

        for appointment in appointments:
            self.tree.insert("", "end", values=appointment)

    def edit_appointment(self):
        item = self.tree.selection()
        if not item:
            messagebox.showerror("Erro", "Selecione um agendamento para editar.")
            return
        appointment_id = self.tree.item(item, "values")[0]
        if not appointment_id:
            messagebox.showerror("Erro", "ID de agendamento inválido.")
            return
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Editar Agendamento")

        # Defina o ícone da janela de edição
        icon_path = "C:/Users/Ivo/Desktop/backup print2/print2/assets/dog.ico"  # Substitua pelo caminho real do ícone
        edit_window.iconbitmap(icon_path)

        # Aumentar o tamanho da janela de edição
        edit_window.geometry("500x450")

        conn = sqlite3.connect('agendamentos.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM agendamentos WHERE id = ?', (appointment_id,))
        appointment = cursor.fetchone()
        conn.close()

        # Crie e preencha os campos para edição de todas as informações
        fields = ["Tutor", "CPF", "Endereço", "Telefone", "Pet", "Espécie", "Raça", "Genero", "Peso", "Idade", "Data", "Horário"]
        entries = []

        for i, field in enumerate(fields):
            label = tk.Label(edit_window, text=f"{field}:")
            label.grid(row=i, column=0, padx=10, pady=5)

            entry = tk.Entry(edit_window, width=40)  # Ajuste a largura da coluna conforme necessário
            entry.insert(0, appointment[i + 1])  # appointment[0] é o ID, por isso começamos de i+1
            entry.grid(row=i, column=1, padx=10, pady=5)

            entries.append(entry)

        def update_appointment():
            new_values = [entry.get() for entry in entries]

            conn = sqlite3.connect('agendamentos.db')
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE agendamentos
                SET tutor_name = ?,
                    cpf = ?,
                    address = ?,
                    phone = ?,
                    pet_name = ?,
                    species = ?,
                    breed = ?,
                    gender = ?, 
                    weight = ?,
                    age = ?,
                    date = ?,
                    time = ?
                WHERE id = ?
            ''', (new_values + [appointment_id]))
            conn.commit()
            conn.close()

            edit_window.destroy()
            self.search_appointments()
            
            messagebox.showinfo("Editar agendamento", "Agendamento atualizado com sucesso!")

        update_button = tk.Button(edit_window, text="Atualizar", command=update_appointment)
        update_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

            # Botão de fechar
        close_button = tk.Button(edit_window, text="Fechar", command=edit_window.destroy)
        close_button.grid(row=len(fields), column=2, columnspan=2, pady=10)

    def delete_appointment(self):
        item = self.tree.selection()
        if not item:
            messagebox.showerror("Erro", "Selecione um agendamento para excluir.")
            return
        appointment_id = self.tree.item(item, "values")[0]
        if not appointment_id:
            messagebox.showerror("Erro", "ID de agendamento inválido.")
            return
        confirm = messagebox.askyesno("Confirmar Exclusão", "Tem certeza de que deseja excluir este agendamento?")
        if confirm:
            conn = sqlite3.connect('agendamentos.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM agendamentos WHERE id = ?', (appointment_id,))
            conn.commit()
            conn.close()
            self.search_appointments()

    def choose_backup_destination_and_backup(self):
        # Abra uma caixa de diálogo para escolher a pasta de destino
        backup_destination_folder = filedialog.askdirectory()

        # Se o usuário cancelar a escolha da pasta, retorne
        if not backup_destination_folder:
            return

        # Chame a função para backup do banco de dados passando a pasta de destino
        self.backup_database(backup_destination_folder)

    def backup_database(self, backup_destination_folder):
        # Utilize a pasta de destino escolhida pelo usuário
        backup_filename = os.path.join(backup_destination_folder, "agendamentos_backup.db")

        # Restante do código para fazer o backup do banco de dados
        try:
            # Copie o arquivo do banco de dados para o local de backup
            shutil.copy2('agendamentos.db', backup_filename)
            messagebox.showinfo("Backup", "Backup do banco de dados realizado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao fazer backup do banco de dados: {str(e)}")

    def on_item_double_click(self, event):
        self.edit_appointment()

    def choose_destination_and_generate_pdf(self):
        # Abra uma caixa de diálogo para escolher a pasta de destino
        destination_folder = filedialog.askdirectory()

        # Se o usuário cancelar a escolha da pasta, retorne
        if not destination_folder:
            return

        # Chame a função para gerar o PDF passando a pasta de destino
        self.generate_pdf(destination_folder)    

    def generate_pdf(self, destination_folder):
        date = self.date_entry.get()
        conn = sqlite3.connect('agendamentos.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM agendamentos WHERE date = ?', (date,))
        appointments = cursor.fetchall()
        conn.close()

        if not appointments:
            messagebox.showinfo("Informação", "Nenhum agendamento encontrado para a data selecionada.")
            return

        # Formate a data para o nome do arquivo com barras
        formatted_date = date.replace('-', '_')

         # Utilize a pasta de destino escolhida pelo usuário
        pdf_filename = os.path.join(destination_folder, f"agendamentos_{formatted_date}.pdf")

        # Restante do código para gerar o PDF
        pdf = canvas.Canvas(pdf_filename)

        # Configuração do cabeçalho
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, 800, "Agendamentos do Dia")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, 780, f"Data: {date}")

        # Configuração da tabela
        pdf.drawString(50, 750, "ID")
        pdf.drawString(100, 750, "Tutor")
        pdf.drawString(200, 750, "CPF")
        pdf.drawString(300, 750, "Pet")
        pdf.drawString(400, 750, "Espécie")
        pdf.drawString(500, 750, "Raça")
        pdf.drawString(600, 750, "Gênero")
        pdf.drawString(700, 750, "Horário")

        y_position = 730
        for appointment in appointments:
            y_position -= 20
            pdf.drawString(50, y_position, str(appointment[0]))
            pdf.drawString(100, y_position, appointment[1])
            pdf.drawString(200, y_position, appointment[2])
            pdf.drawString(300, y_position, appointment[5])
            pdf.drawString(400, y_position, appointment[6])
            pdf.drawString(500, y_position, appointment[7])
            pdf.drawString(600, y_position, appointment[8])
            pdf.drawString(700, y_position, appointment[11])

        pdf.save()
        messagebox.showinfo("Informação", f"PDF gerado com sucesso: {pdf_filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ViewAppointmentsScreen(root)
    root.mainloop()    