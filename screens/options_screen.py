import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

# Importe as outras telas
from screens.appointment_screen import AppointmentScreen
from screens.view_appointments_screen import ViewAppointmentsScreen
from screens.donation_registration_screen import DonationRegistrationScreen
from screens.view_donations_screen import ViewDonationsScreen
from screens.vet_registration_screen import VetRegistrationScreen
from screens.availability_management_screen import AvailabilityManagementScreen

class OptionsScreen:
    def __init__(self, root, background_image, get_image_path_func):
        self.root = root
        self.root.title("Opções")
        self.root.geometry("1350x800")

        background_label = tk.Label(self.root, image=background_image)
        background_label.place(relx=0.5, rely=0.5, anchor='center')

        self.get_image_path = get_image_path_func
        self.create_widgets(get_image_path_func)  

        icon_path = get_image_path_func("dog.ico")
        self.root.iconbitmap(icon_path)

    def create_widgets(self, get_image_path_func):
        new_size = (100, 100)  

        x_start = 0.45
        y_start = 0.40
        y_step = 0.25  

        style = ttk.Style()
        style.configure("TButton", relief="flat", borderwidth=0)

        appointment_icon = Image.open(get_image_path_func("icone.png"))
        appointment_icon = appointment_icon.resize(new_size, Image.BICUBIC)
        appointment_icon = ImageTk.PhotoImage(appointment_icon)

        appointment_button = ttk.Button(self.root, command=self.open_appointment_screen, image=appointment_icon, style="TButton")
        appointment_button.image = appointment_icon  
        appointment_button.place(relx=x_start - 0.01, rely=y_start, anchor='center')

        label_appointment = tk.Label(self.root, text="Agendar", font=("Helvetica", 12), bg="white")
        label_appointment.place(relx=x_start - 0.01, rely=y_start + 0.1, anchor='center')

        view_appointments_icon = Image.open(get_image_path_func("icone4.png"))
        view_appointments_icon = view_appointments_icon.resize(new_size, Image.BICUBIC)
        view_appointments_icon = ImageTk.PhotoImage(view_appointments_icon)
        view_appointments_button = ttk.Button(self.root, command=self.open_view_appointments_screen, image=view_appointments_icon, style="TButton")
        view_appointments_button.image = view_appointments_icon
        view_appointments_button.place(relx=0.575, rely=0.40, anchor='center')

        label_view_appointments = tk.Label(self.root, text="Visualizar Agenda", font=("Helvetica", 12), bg="white")
        label_view_appointments.place(relx=0.575, rely=0.50, anchor='center')

        donation_registration_icon = Image.open(get_image_path_func("icone2.png"))
        donation_registration_icon = donation_registration_icon.resize(new_size, Image.BICUBIC)
        donation_registration_icon = ImageTk.PhotoImage(donation_registration_icon)
        donation_registration_button = ttk.Button(self.root, command=self.open_donation_registration_screen, image=donation_registration_icon, style="TButton")
        donation_registration_button.image = donation_registration_icon
        donation_registration_button.place(relx=0.440, rely=0.65, anchor='center')

        label_donation_registration = tk.Label(self.root, text="Cadastrar Doação", font=("Helvetica", 12), bg="white")
        label_donation_registration.place(relx=0.440, rely=0.75, anchor='center')

        view_donations_icon = Image.open(get_image_path_func("icone7.png"))
        view_donations_icon = view_donations_icon.resize(new_size, Image.BICUBIC)
        view_donations_icon = ImageTk.PhotoImage(view_donations_icon)
        view_donations_button = ttk.Button(self.root, command=self.open_view_donations_screen, image=view_donations_icon, style="TButton")
        view_donations_button.image = view_donations_icon
        view_donations_button.place(relx=0.575, rely=0.65, anchor='center')

        label_view_donations = tk.Label(self.root, text="Visualizar Doações", font=("Helvetica", 12), bg="white")
        label_view_donations.place(relx=0.575, rely=0.75, anchor='center')

        vet_registration_icon = Image.open(get_image_path_func("icone3.png"))
        vet_registration_icon = vet_registration_icon.resize(new_size, Image.BICUBIC)
        vet_registration_icon = ImageTk.PhotoImage(vet_registration_icon)
        vet_registration_button = ttk.Button(self.root, command=self.open_vet_registration_screen, image=vet_registration_icon, style="TButton")
        vet_registration_button.image = vet_registration_icon
        vet_registration_button.place(relx=0.40, rely=0.1, anchor='nw')

        label_vet_registration = tk.Label(self.root, text="Cadastro de Veterinário", font=("Helvetica", 12), bg="white")
        label_vet_registration.place(relx=0.37, rely=0.26, anchor='nw')


        availability_management_icon = Image.open(get_image_path_func("icone5.png"))
        availability_management_icon = availability_management_icon.resize(new_size, Image.BICUBIC)
        availability_management_icon = ImageTk.PhotoImage(availability_management_icon)
        availability_management_button = ttk.Button(self.root, command=self.open_availability_management_screen, image=availability_management_icon, style="TButton")
        availability_management_button.image = availability_management_icon
        availability_management_button.place(relx=0.57, rely= 0.176, anchor='center')

        label_availability_management = tk.Label(self.root, text="Gerenciar Disponibilidade", font=("Helvetica", 12), bg="white")
        label_availability_management.place(relx=0.57, rely=0.276, anchor='center')

        exit_button = ttk.Button(self.root, text="Sair", command=self.root.destroy, width=20)
        exit_button.place(relx=0.5, rely=0.85, anchor='center')

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

    def open_vet_registration_screen(self):
        vet_registration_root = tk.Toplevel()
        app = VetRegistrationScreen(vet_registration_root)

    def open_availability_management_screen(self):
        availability_management_root = tk.Toplevel()
        app = AvailabilityManagementScreen(availability_management_root)

if __name__ == "__main__":
    root = tk.Tk()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, 'clini3.jpeg')
    background_image = Image.open(image_path)
    background_photo = ImageTk.PhotoImage(background_image)
    app = OptionsScreen(root, background_photo)
    root.mainloop()
