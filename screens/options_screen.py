import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from screens.appointment_screen import AppointmentScreen
from screens.view_appointments_screen import ViewAppointmentsScreen
from screens.donation_registration_screen import DonationRegistrationScreen
from screens.view_donations_screen import ViewDonationsScreen
import os

class OptionsScreen:
    def __init__(self, root, background_image, get_image_path_func):
        self.root = root
        self.root.title("Opções")
        self.root.geometry("1350x800")

        background_label = tk.Label(self.root, image=background_image)
        background_label.place(relx=0.5, rely=0.5, anchor='center')

        self.get_image_path = get_image_path_func
        self.create_widgets(get_image_path_func)  # Adicione a chamada correta aqui

    # Defina o ícone da janela
        icon_path = get_image_path_func("dog.ico")
        self.root.iconbitmap(icon_path)

         # Defina o título da janela
        root.title("Opções")


    def create_widgets(self, get_image_path_func):
        # Carregar ícone para o botão de agendamento
        icon_path = get_image_path_func("icone.png")
        icon = Image.open(icon_path)
        new_size = (100, 100)  # Escolha o tamanho desejado para o ícone
        icon = icon.resize(new_size, Image.BICUBIC)
        icon = ImageTk.PhotoImage(icon)

        # Centralizar os botões horizontalmente
        x_start = 0.45
        y_start = 0.40
        y_step = 0.25  # Ajuste o espaçamento vertical

        # Estilo para botões sem borda
        style = ttk.Style()
        style.configure("TButton", relief="flat", borderwidth=0)

        # Opção 1: Agendamento com ícone
        appointment_button = ttk.Button(self.root, command=self.open_appointment_screen, image=icon, style="TButton")
        appointment_button.image = icon  # Mantenha uma referência ao objeto PhotoImage
        appointment_button.place(relx=x_start - 0.01, rely=y_start, anchor='center')

        # Legenda 1: Agendar
        label_appointment = tk.Label(self.root, text="Agendar", font=("Helvetica", 12), bg="white")
        label_appointment.place(relx=x_start - 0.01, rely=y_start + 0.1, anchor='center')

       # Ícone de Visualizar Agenda
        view_appointments_icon = Image.open(get_image_path_func("icone4.png"))
        view_appointments_icon = view_appointments_icon.resize(new_size, Image.BICUBIC)
        view_appointments_icon = ImageTk.PhotoImage(view_appointments_icon)
        view_appointments_button = ttk.Button(self.root, command=self.open_view_appointments_screen, image=view_appointments_icon, style="TButton")
        view_appointments_button.image = view_appointments_icon
        view_appointments_button.place(relx=0.575, rely=0.40, anchor='center')

        # Legenda de Visualizar Agenda
        label_view_appointments = tk.Label(self.root, text="Visualizar Agenda", font=("Helvetica", 12), bg="white")
        label_view_appointments.place(relx=0.575, rely=0.50, anchor='center')

        # Ícone de Cadastrar Doação
        donation_registration_icon = Image.open(get_image_path_func("icone2.png"))
        donation_registration_icon = donation_registration_icon.resize(new_size, Image.BICUBIC)
        donation_registration_icon = ImageTk.PhotoImage(donation_registration_icon)
        donation_registration_button = ttk.Button(self.root, command=self.open_donation_registration_screen, image=donation_registration_icon, style="TButton")
        donation_registration_button.image = donation_registration_icon
        donation_registration_button.place(relx=0.440, rely=0.65, anchor='center')

        # Legenda de Cadastrar Doação
        label_donation_registration = tk.Label(self.root, text="Cadastrar Doação", font=("Helvetica", 12), bg="white")
        label_donation_registration.place(relx=0.440, rely=0.75, anchor='center')

        # Ícone de Visualizar Doações
        view_donations_icon = Image.open(get_image_path_func("icone7.png"))
        view_donations_icon = view_donations_icon.resize(new_size, Image.BICUBIC)
        view_donations_icon = ImageTk.PhotoImage(view_donations_icon)
        view_donations_button = ttk.Button(self.root, command=self.open_view_donations_screen, image=view_donations_icon, style="TButton")
        view_donations_button.image = view_donations_icon
        view_donations_button.place(relx=0.575, rely=0.65, anchor='center')

        # Legenda de Visualizar Doações
        label_view_donations = tk.Label(self.root, text="Visualizar Doações", font=("Helvetica", 12), bg="white")
        label_view_donations.place(relx=0.575, rely=0.75, anchor='center')

        # Botão Ajuda
        help_button = ttk.Button(self.root, text="Ajuda?", command=self.show_help_dialog, width=20)
        help_button.place(relx=0.95, rely=0.05, anchor='center')

         # Botão Sair
        exit_button = ttk.Button(self.root, text="Sair", command=self.root.destroy, width=20)
        exit_button.place(relx=0.5, rely=0.85, anchor='center')

    def show_help_dialog(self):
        help_text = (
            "Ajuda:\n"
            "Ícone 1: Agendar - Use este botão para agendar compromissos.\n"
            "Ícone 2: Visualizar Agenda - Visualize seus compromissos agendados.\n"
            "Ícone 3: Cadastrar Doação - Cadastre uma nova doação.\n"
            "Ícone 4: Visualizar Doações - Visualize as doações cadastradas.\n"
        )
        messagebox.showinfo("Ajuda", help_text)
        
    def open_appointment_screen(self):
        appointment_root = tk.Toplevel()
        app = AppointmentScreen(appointment_root)

    def open_view_appointments_screen(self):
        view_appointments_root = tk.Toplevel()
        app = ViewAppointmentsScreen(view_appointments_root)

    def open_donation_registration_screen(self):
        donation_registration_root = tk.Toplevel()
        app = DonationRegistrationScreen(donation_registration_root)

    def open_view_donations_screen(self):
        view_donations_root = tk.Toplevel()
        app = ViewDonationsScreen(view_donations_root)
        

if __name__ == "__main__":
    root = tk.Tk()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, 'clini3.jpeg')
    background_image = Image.open(image_path)
    background_photo = ImageTk.PhotoImage(background_image)
    app = OptionsScreen(root, background_photo)
    root.mainloop()
