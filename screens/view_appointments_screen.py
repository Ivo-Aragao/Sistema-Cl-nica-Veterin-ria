import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import shutil
import os

class EditAppointmentDialog:
    def __init__(self, parent, appointment_details):
        self.parent = parent
        self.appointment_details = appointment_details

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Editar Agendamento")
        self.dialog.grab_set()

        self.create_widgets()

    def create_widgets(self):
        # Labels e campos de entrada para os detalhes do agendamento
        labels = ["ID", "Tutor", "CPF", "Pet", "Espécie", "Raça", "Gênero", "Horário", "Data"]
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(self.dialog, text=label + ":").grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(self.dialog, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entry.insert(0, self.appointment_details[i])
            self.entries[label] = entry

        # Botão de salvar alterações
        save_button = tk.Button(self.dialog, text="Salvar", command=self.save_changes)
        save_button.grid(row=len(labels), columnspan=2, pady=10)

    def save_changes(self):
        # Obtém os novos detalhes do agendamento dos campos de entrada
        new_details = [self.entries[label].get() for label in self.entries]

        # Atualiza os detalhes do agendamento
        self.update_appointment_details(new_details)

        # Fecha a janela de diálogo
        self.dialog.destroy()

    def update_appointment_details(self, new_details):
        # Conecta-se ao banco de dados SQLite
        conn = sqlite3.connect('clinic_database.db')
        cursor = conn.cursor()

        try:
            # Executa a consulta SQL para atualizar os detalhes do agendamento
            cursor.execute("UPDATE agendamentos SET tutor_name=?, cpf=?, pet_name=?, species=?, breed=?, gender=?, time=?, appointment_date=? WHERE id=?", (*new_details[1:], self.appointment_details[0]))
            conn.commit()
            messagebox.showinfo("Editar Agendamento", "Agendamento editado com sucesso.")
            # Atualize a exibição dos agendamentos na tela principal, se necessário
            # Por exemplo, você pode chamar self.populate_treeview() da tela principal aqui
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Erro", f"Erro ao editar o agendamento: {e}")
        finally:
            conn.close()


class ViewAppointmentsScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizar Agendamentos por Tutor")
        self.root.geometry("800x400")

        # Defina o ícone da janela
        icon_path = "C:/Users/Ivo/Desktop/Projetos Prontos pra uso/Projeto Clinica movelpet/assets/dog.ico"
        self.root.iconbitmap(icon_path)

        self.create_widgets()

    def create_widgets(self):
        # Título
        title_label = tk.Label(self.root, text="Visualizar Agendamentos por Tutor", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=6, pady=20)

        # Combobox para seleção de datas
        date_label = tk.Label(self.root, text="Selecione a data:")
        date_label.grid(row=1, column=0)
        self.date_combobox = ttk.Combobox(self.root, state="readonly", width=12)
        self.date_combobox.grid(row=1, column=1)
        self.date_combobox.bind("<<ComboboxSelected>>", self.populate_treeview)

        # Tabela de agendamentos
        columns = ("ID", "Tutor", "CPF", "Pet", "Espécie", "Raça", "Gênero", "Horário", "Data")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)  # Defina a largura da coluna
        self.tree.grid(row=2, column=0, columnspan=6, sticky='nsew')  # Use sticky para preencher a célula
        self.tree.bind("<Double-1>", self.edit_appointment)

        # Botões de ação
        edit_button = tk.Button(self.root, text="Editar", command=self.edit_appointment)
        edit_button.grid(row=3, column=0)
        delete_button = tk.Button(self.root, text="Excluir", command=self.delete_appointment)
        delete_button.grid(row=3, column=1)

        # Botão de fechar
        close_button = tk.Button(self.root, text="Fechar", command=self.root.destroy)
        close_button.grid(row=3, column=2)

        # Botão de ação para gerar PDF
        pdf_button = tk.Button(self.root, text="Gerar PDF", command=self.generate_pdf)
        pdf_button.grid(row=3, column=3)

        # Botão de backup do banco de dados
        backup_button = tk.Button(self.root, text="Backup do Banco de Dados", command=self.backup_database)
        backup_button.grid(row=3, column=4)

        # Carregar as datas disponíveis
        self.populate_dates()

    def populate_dates(self):
        # Conecte-se ao banco de dados SQLite
        conn = sqlite3.connect('clinic_database.db')
        cursor = conn.cursor()

        # Obter datas únicas existentes no banco de dados
        cursor.execute('SELECT DISTINCT appointment_date FROM agendamentos')
        dates = cursor.fetchall()

        # Converter as datas em uma lista de strings
        date_options = [date[0] for date in dates]

        # Configurar opções do Combobox
        self.date_combobox["values"] = date_options

        # Fechar a conexão com o banco de dados
        conn.close()

    def populate_treeview(self, event=None):
        # Obtenha a data selecionada do Combobox
        selected_date = self.date_combobox.get()

        # Conecte-se ao banco de dados SQLite
        conn = sqlite3.connect('clinic_database.db')
        cursor = conn.cursor()

        # Busque os agendamentos para a data selecionada
        cursor.execute('SELECT id, tutor_name, cpf, pet_name, species, breed, gender, time, appointment_date FROM agendamentos WHERE appointment_date = ?', (selected_date,))
        appointments = cursor.fetchall()

        # Limpe os itens existentes na árvore
        for record in self.tree.get_children():
            self.tree.delete(record)

        # Preencha a árvore com os agendamentos recuperados
        for appointment in appointments:
            self.tree.insert("", "end", values=appointment)

        # Feche a conexão com o banco de dados
        conn.close()

    def edit_appointment(self, event=None):
        # Verifique se um agendamento foi selecionado
        if not self.tree.selection():
            messagebox.showwarning("Editar Agendamento", "Por favor, selecione um agendamento para editar.")
            return

        # Obtenha o item selecionado na árvore
        item = self.tree.selection()[0]
        # Obtenha os detalhes do agendamento selecionado
        appointment_details = self.tree.item(item, "values")

        # Abra uma janela de diálogo para editar o agendamento
        EditAppointmentDialog(self.root, appointment_details)

    def delete_appointment(self):
        # Verifique se um agendamento foi selecionado
        if not self.tree.selection():
            messagebox.showwarning("Excluir Agendamento", "Por favor, selecione um agendamento para excluir.")
            return

        # Solicite confirmação do usuário antes de excluir o agendamento
        confirm = messagebox.askyesno("Excluir Agendamento", "Tem certeza de que deseja excluir este agendamento?")
        if confirm:
            # Obtenha o item selecionado na árvore
            item = self.tree.selection()[0]
            # Obtenha o ID do agendamento selecionado
            appointment_id = self.tree.item(item, "values")[0]

            # Implemente a lógica para excluir o agendamento do banco de dados
            conn = sqlite3.connect('clinic_database.db')
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM agendamentos WHERE id = ?", (appointment_id,))
                conn.commit()
                # Atualize a exibição removendo o agendamento excluído da árvore
                self.tree.delete(item)
                messagebox.showinfo("Excluir Agendamento", "Agendamento excluído com sucesso.")
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Erro", f"Erro ao excluir o agendamento: {e}")
            finally:
                conn.close()

    def generate_pdf(self):
        # Obtém os dados da tabela
        data = [self.tree.item(item, "values") for item in self.tree.get_children()]
        # Gera o PDF
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            c = canvas.Canvas(file_path, pagesize=letter)
            width, height = letter
            y = height - 50
            for row in data:
                x = 50
                for item in row:
                    c.drawString(x, y, str(item))
                    x += 100
                y -= 20
            c.save()
            messagebox.showinfo("PDF Gerado", "PDF gerado com sucesso!")

    def backup_database(self):
        # Seleciona o local de destino para o backup do banco de dados
        backup_dir = filedialog.askdirectory()
        if backup_dir:
            # Copia o banco de dados para o diretório de backup
            try:
                shutil.copy("clinic_database.db", os.path.join(backup_dir, "clinic_database_backup.db"))
                messagebox.showinfo("Backup Concluído", "Backup do banco de dados realizado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao fazer o backup do banco de dados: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ViewAppointmentsScreen(root)
    root.mainloop()
