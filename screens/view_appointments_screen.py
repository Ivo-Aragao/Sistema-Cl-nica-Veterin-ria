import sys
import os
import tempfile
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import shutil


class EditAppointmentDialog:
    def __init__(self, parent, appointment_details):
        self.parent = parent
        self.appointment_details = appointment_details

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Editar Agendamento")
        self.dialog.grab_set()

        icon_path = "./assets/dog.ico"
        self.dialog.iconbitmap(icon_path)

        self.create_widgets()

    def create_widgets(self):
        # Labels e campos de entrada para os detalhes do agendamento
        labels = ["Tutor", "Endereço", "Telefone", "Pet", "Espécie", "Raça", "Gênero", "Peso Estimado", "Idade", "Doença do Pet", "Localização", "Horário", "Tipo de Atendimento", "Veterinário", "Data"]
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
            cursor.execute("UPDATE agendamentos SET tutor_name=?, address=?, phone=?, pet_name=?, species=?, breed=?, gender=?, weight=?, age=?, pet_disease=?, location=?, time=?, service=?, vet=?, appointment_date=? WHERE id=?", (*new_details, self.appointment_details[-1]))
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
        self.root.geometry("1400x500")

        # Defina o ícone da janela
        icon_path = "./assets/dog.ico"
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
        columns = ("Tutor", "Endereço", "Telefone", "Pet", "Espécie", "Raça", "Gênero", "Peso Estimado", "Idade", "Doença do Pet", "Localização", "Horário", "Tipo de Atendimento", "Veterinário", "Data")
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

        # Botão de backup do banco de dados
        backup_button = tk.Button(self.root, text="Backup do Banco de Dados", command=self.backup_database)
        backup_button.grid(row=3, column=3)

        # Botão de ação para imprimir os agendamentos
        print_button = tk.Button(self.root, text="Imprimir", command=self.print_appointments)
        print_button.grid(row=3, column=4)

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
        cursor.execute('SELECT tutor_name, address, phone, pet_name, species, breed, gender, weight, age, pet_disease, location, time, service, vet, appointment_date FROM agendamentos WHERE appointment_date = ?', (selected_date,))
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
        # Obter o item selecionado na árvore
        selected_item = self.tree.selection()

        if selected_item:
            # Obter os detalhes do agendamento selecionado
            item_details = self.tree.item(selected_item)['values']

            # Abrir a janela de diálogo para editar o agendamento
            EditAppointmentDialog(self.root, item_details)
        else:
            messagebox.showwarning("Editar Agendamento", "Selecione um agendamento para editar.")

    def delete_appointment(self):
        # Obter o item selecionado na árvore
        selected_item = self.tree.selection()

        if selected_item:
            # Confirmar a exclusão do agendamento
            if messagebox.askyesno("Excluir Agendamento", "Tem certeza de que deseja excluir este agendamento?"):
                # Obter o ID do agendamento selecionado
                appointment_id = self.tree.item(selected_item)['values'][-1]

                # Conectar-se ao banco de dados SQLite
                conn = sqlite3.connect('clinic_database.db')
                cursor = conn.cursor()

                try:
                    # Executar a consulta SQL para excluir o agendamento
                    cursor.execute("DELETE FROM agendamentos WHERE id = ?", (appointment_id,))
                    conn.commit()
                    messagebox.showinfo("Excluir Agendamento", "Agendamento excluído com sucesso.")
                    # Atualize a exibição dos agendamentos na tela principal, se necessário
                    # Por exemplo, você pode chamar self.populate_treeview() da tela principal aqui
                except Exception as e:
                    conn.rollback()
                    messagebox.showerror("Erro", f"Erro ao excluir o agendamento: {e}")
                finally:
                    # Feche a conexão com o banco de dados
                    conn.close()

                # Remover o agendamento da árvore
                self.tree.delete(selected_item)
        else:
            messagebox.showwarning("Excluir Agendamento", "Selecione um agendamento para excluir.")


    def backup_database(self):
        # Selecionar o local do arquivo de backup
        backup_file = filedialog.asksaveasfilename(defaultextension=".dbbackup")

        if backup_file:
            try:
                # Copiar o banco de dados SQLite para o arquivo de backup
                shutil.copyfile("clinic_database.db", backup_file)
                messagebox.showinfo("Backup do Banco de Dados", "Backup do banco de dados concluído com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao fazer backup do banco de dados: {e}")

    def print_appointments(self):
        # Obter todos os agendamentos da árvore
        all_appointments = self.tree.get_children()

        # Criar uma string formatada com os detalhes dos agendamentos
        appointments_text = ""
        for appointment_id in all_appointments:
            appointment_details = self.tree.item(appointment_id)['values']
            appointments_text += "Agendamento:\n"
            appointments_text += f"Tutor: {appointment_details[0]}\n"
            appointments_text += f"Telefone: {appointment_details[2]}\n"
            appointments_text += f"Espécie: {appointment_details[4]}\n"
            appointments_text += f"Gênero: {appointment_details[6]}\n"
            appointments_text += f"Doença do Pet: {appointment_details[9]}\n"
            appointments_text += f"Localização: {appointment_details[10]}\n"
            appointments_text += f"Horário: {appointment_details[11]}\n"
            appointments_text += f"Veterinário: {appointment_details[13]}\n\n"

        # Criar um arquivo temporário para salvar os detalhes dos agendamentos
        temp_file = tempfile.mktemp(".txt")

        # Escrever os detalhes dos agendamentos no arquivo temporário
        with open(temp_file, "w") as file:
            file.write(appointments_text)

        # Abrir o arquivo temporário para impressão
        os.startfile(temp_file, "print")


def main():
    root = tk.Tk()
    app = ViewAppointmentsScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()
