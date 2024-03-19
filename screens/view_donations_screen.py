import os
import shutil
import sqlite3
import tkinter as tk
from tkinter import messagebox, filedialog
from tkcalendar import DateEntry
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class ViewDonationsScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizar Doações")
        self.root.geometry("600x500")
        self.root.grid_columnconfigure(0, weight=1)
       
        self.view_screen_instance = self
       
       # Defina o ícone da janela
        icon_path = "C:/Users/Ivo/Desktop/Projetos Prontos pra uso/Projeto Clinica movelpet/assets/dog.ico"  # Substitua pelo caminho real do ícone
        self.root.iconbitmap(icon_path)


        self.create_widgets()

    def refresh_list(self):
        # Atualiza a lista de doações
        self.load_donations()

    def open_edit_screen(self):
        # Abrir a tela de edição com a doação selecionada
        selected_index = self.donations_listbox.curselection()

        if selected_index:
            try:
                selected_item = self.donations_listbox.get(selected_index[0])
                selected_id = self.extract_id_from_list_item(selected_item, True)

                if selected_id is not None:
                    # Abrir a tela de edição com o ID selecionado
                    root = tk.Tk()
                    edit_screen = EditDonationScreen(root, selected_id, self)
                    root.mainloop()
                else:
                    messagebox.showerror("Erro", "Não foi possível extrair o ID da doação.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao abrir a tela de edição: {str(e)}")
        else:
            messagebox.showerror("Erro", "Nenhuma doação selecionada para edição.")


    def delete_donation(self):
        # Excluir uma doação selecionada na lista
        selected_index = self.donations_listbox.curselection()

        if selected_index and selected_index[0] < self.donations_listbox.size():
            selected_item = self.donations_listbox.get(selected_index[0])
            selected_id = self.extract_id_from_list_item(selected_item)

            if selected_id is not None:
                confirmation = messagebox.askyesno("Confirmação de Exclusão", "Tem certeza que deseja excluir esta doação?")
                if confirmation:
                    try:
                        conn = sqlite3.connect('doacoes.db')
                        cursor = conn.cursor()
                        cursor.execute('DELETE FROM doacoes WHERE id = ?', (selected_id,))
                        conn.commit()
                        conn.close()

                        self.refresh_list()  # Atualiza a lista após excluir

                    except sqlite3.Error as e:
                        messagebox.showerror("Erro no Banco de Dados", str(e))
            else:
                messagebox.showerror("Erro", "Não foi possível extrair o ID da doação.")
        else:
            messagebox.showerror("Erro", "Nenhuma doação selecionada para exclusão.")        

    def check_doacoes_table_exists(self):
        try:
            conn = sqlite3.connect('doacoes.db')
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='doacoes'")
            table_exists = cursor.fetchone() is not None
            conn.close()

            if not table_exists:
                raise Exception("A tabela 'doacoes' não foi encontrada no banco de dados.")

        except Exception as e:
            messagebox.showerror("Erro no Banco de Dados", str(e))
            self.root.destroy()

    def extract_id_from_list_item(self, list_item, is_filtered=False):
        try:
            if is_filtered:
                # Quando a lista é filtrada, o formato da string é diferente
                selected_id = int(list_item.split("ID: ")[1].split(",")[0].strip())
            else:
                selected_id = int(list_item.split("ID: ")[1].split(",")[0])
            return selected_id
        except (ValueError, IndexError) as e:
            print(f"Erro ao extrair ID: {e}")
            print(f"Lista: {list_item}")
            return None



    def create_widgets(self):
        title_label = tk.Label(self.root, text="Visualizar Doações", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=5, pady=(20, 10))

        start_date_label = tk.Label(self.root, text="Data de Início:")
        start_date_label.grid(row=1, column=0)
        self.start_date_entry = DateEntry(self.root, date_pattern="dd/mm/yyyy")
        self.start_date_entry.grid(row=1, column=1)

        end_date_label = tk.Label(self.root, text="Data de Fim:")
        end_date_label.grid(row=1, column=2)
        self.end_date_entry = DateEntry(self.root, date_pattern="dd/mm/yyyy")
        self.end_date_entry.grid(row=1, column=3)

        filter_button = tk.Button(self.root, text="Filtrar por Data", command=self.filter_by_date)
        filter_button.grid(row=1, column=4, padx=10)

        self.donations_listbox = tk.Listbox(self.root, width=50, height=15)
        self.donations_listbox.grid(row=2, column=0, columnspan=5, padx=10, pady=(0, 10), sticky="nsew")

        edit_button = tk.Button(self.root, text="Editar Doação", command=self.open_edit_screen)
        edit_button.grid(row=3, column=0, pady=10)

        delete_button = tk.Button(self.root, text="Excluir Doação", command=self.delete_donation)
        delete_button.grid(row=3, column=1, pady=10)

        generate_report_button = tk.Button(self.root, text="Gerar Relatório Mensal", command=self.generate_monthly_report)
        generate_report_button.grid(row=3, column=2, pady=10)

        backup_button = tk.Button(self.root, text="Backup do Banco de Dados", command=self.backup_database)
        backup_button.grid(row=3, column=3, pady=10)


        close_button = tk.Button(self.root, text="Fechar", command=self.root.destroy)
        close_button.grid(row=3, column=4, pady=10)
        
        self.root.grid_rowconfigure(2, weight=1)

        self.load_donations()

    def backup_database(self):
        backup_destination_folder = filedialog.askdirectory(title="Escolha a Pasta de Destino para o Backup")
        if backup_destination_folder:
            backup_path = os.path.join(backup_destination_folder, 'doacoes_backup.db')
            try:
                shutil.copy2('doacoes.db', backup_path)
                messagebox.showinfo("Backup", "Backup do banco de dados realizado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao fazer backup do banco de dados: {str(e)}")

    def filter_by_date(self):
        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()

        try:
            conn = sqlite3.connect('doacoes.db')
            cursor = conn.cursor()
            cursor.execute('SELECT id, donor_name, donation_type, donation_description, donation_date FROM doacoes WHERE donation_date BETWEEN ? AND ?', (start_date.strftime("%d/%m/%Y"), end_date.strftime("%d/%m/%Y")))
            donations = cursor.fetchall()
            conn.close()

            self.donations_listbox.delete(0, tk.END)

            if not donations:
                messagebox.showinfo("Sem Doações", "Não há doações no período selecionado.")
                return

            for donation in donations:
                donation_info = f"ID: {donation[0]}, Nome: {donation[1]}, Tipo: {donation[2]}, Descrição: {donation[3]}, Data: {donation[4]}"
                self.donations_listbox.insert(tk.END, donation_info)

        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", str(e))


    def load_donations(self):
        try:
            conn = sqlite3.connect('doacoes.db')
            cursor = conn.cursor()
            cursor.execute('SELECT id, donor_name, donation_type, donation_description, donation_date FROM doacoes')
            donations = cursor.fetchall()
            conn.close()

            if not donations:
                messagebox.showinfo("Nenhuma Doação", "Não há doações no banco de dados.")
                return

            self.donations_listbox.delete(0, tk.END)

            for donation in donations:
                donation_info = f"ID: {donation[0]}, Nome: {donation[1]}, Tipo: {donation[2]}, Descrição: {donation[3]}, Data: {donation[4]}"
                self.donations_listbox.insert(tk.END, donation_info)

        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", str(e))


    def generate_monthly_report(self):
        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()

        try:
            conn = sqlite3.connect('doacoes.db')
            cursor = conn.cursor()
            cursor.execute('SELECT donor_name, donation_type, donation_description, donation_date FROM doacoes WHERE donation_date BETWEEN ? AND ?', (start_date.strftime("%d/%m/%Y"), end_date.strftime("%d/%m/%Y")))
            donations = cursor.fetchall()
            conn.close()

            report_destination_folder = filedialog.askdirectory(title="Escolha a Pasta de Destino para o Relatório")
            if report_destination_folder:
                report_path = os.path.join(report_destination_folder, 'Relatorio_mensal_doacoes.pdf')
                try:
                    c = canvas.Canvas(report_path, pagesize=letter)
                    c.setFont("Helvetica", 12)
                    c.drawString(100, 750, "Relatório Mensal de Doações")
                    c.drawString(100, 730, f"Período: {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}")
                    c.drawString(100, 710, "------------------------------------------------------------")

                    y = 680
                    for donation in donations:
                        donation_info = f"Nome: {donation[0]}, Tipo: {donation[1]}, Descrição: {donation[2]}, Data: {donation[3]}"
                        c.drawString(100, y, donation_info)
                        y -= 20

                    c.save()

                    messagebox.showinfo("Relatório Gerado", f"O relatório mensal foi gerado com sucesso como {report_path}")

                except sqlite3.Error as e:
                    messagebox.showerror("Erro no Banco de Dados", str(e))

            else:
                messagebox.showinfo("Operação Cancelada", "A geração do relatório foi cancelada pelo usuário.")

        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", str(e))

class EditDonationScreen:
    def __init__(self, root, donation_id, view_screen_instance):
        self.root = root
        self.root.title("Editar Doação")
        self.root.geometry("400x200")
        self.root.grid_columnconfigure(1, weight=1)  # Configura a coluna 1 para expandir

        self.donation_id = donation_id
        self.view_screen_instance = view_screen_instance  # Salva a instância da ViewDonationsScreen
        self.create_widgets()
        self.load_donation_details()

         # Defina o ícone da janela de edição
        icon_path = "C:/Users/Ivo/Desktop/Projetos Prontos pra uso/Projeto Clinica movelpet/assets/dog.ico"  # Substitua pelo caminho real do ícone
        self.root.iconbitmap(icon_path)

    def show(self):
        self.root.mainloop()


    def create_widgets(self):
        donor_name_label = tk.Label(self.root, text="Nome do Doador:")
        donor_name_label.grid(row=0, column=0, sticky="w")
        self.donor_name_entry = tk.Entry(self.root)
        self.donor_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        donation_type_label = tk.Label(self.root, text="Tipo de Doação:")
        donation_type_label.grid(row=1, column=0, sticky="w")
        self.donation_type_entry = tk.Entry(self.root)
        self.donation_type_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        donation_description_label = tk.Label(self.root, text="Descrição da Doação:")
        donation_description_label.grid(row=2, column=0, sticky="w")
        self.donation_description_entry = tk.Entry(self.root)
        self.donation_description_entry.grid(row=2, column=1, padx=10, pady=5, sticky="we")

        donation_date_label = tk.Label(self.root, text="Data da Doação (DD-MM-YYYY):")
        donation_date_label.grid(row=3, column=0, sticky="w")
        self.donation_date_entry = DateEntry(self.root, date_pattern="dd/mm/yyyy")
        self.donation_date_entry.grid(row=3, column=1, padx=10, pady=5, sticky="we")

        save_button = tk.Button(self.root, text="Salvar Alterações", command=self.save_changes)
        save_button.grid(row=4, column=0, columnspan=1, pady=10)

        # Botão para fechar a janela de edição
        close_button = tk.Button(self.root, text="Fechar", command=self.root.destroy)
        close_button.grid(row=4, column=1, columnspan=2, pady=10)

    def load_donation_details(self):
        try:
            conn = sqlite3.connect('doacoes.db')
            cursor = conn.cursor()
            cursor.execute('SELECT donor_name, donation_type, donation_description, donation_date FROM doacoes WHERE id = ?', (self.donation_id,))
            donation_details = cursor.fetchone()
            conn.close()

            if donation_details:
                self.donor_name_entry.insert(0, donation_details[0])
                self.donation_type_entry.insert(0, donation_details[1])
                self.donation_description_entry.insert(0, donation_details[2])
                self.donation_date_entry.set_date(donation_details[3])
            else:
                messagebox.showerror("Erro", "Doação não encontrada.")
                self.root.destroy()

        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", str(e))
            self.root.destroy()

    def save_changes(self):
        donor_name = self.donor_name_entry.get()
        donation_type = self.donation_type_entry.get()
        donation_description = self.donation_description_entry.get()
        donation_date = self.donation_date_entry.get_date().strftime("%d/%m/%Y")

        try:
            conn = sqlite3.connect('doacoes.db')
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE doacoes
                SET donor_name = ?, donation_type = ?, donation_description = ?, donation_date = ?
                WHERE id = ?
            ''', (donor_name, donation_type, donation_description, donation_date, self.donation_id))
            conn.commit()
            conn.close()

            # Obtemos a instância da ViewDonationsScreen
            view_screen = self.root.master

            # Verificamos se a instância é válida antes de chamar o método
            if self.view_screen_instance:
                self.view_screen_instance.load_donations()

            messagebox.showinfo("Alterações Salvas", "As alterações foram salvas com sucesso.")
            self.root.destroy()


        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = ViewDonationsScreen(root)
    root.mainloop()
