import sys
import os
import tkinter as tk
from PIL import Image, ImageTk
from screens.login_screen import LoginScreen
from screens.options_screen import OptionsScreen
from screens.appointment_screen import AppointmentScreen
from screens.donation_registration_screen import DonationRegistrationScreen
from screens.view_appointments_screen import ViewAppointmentsScreen
from screens.view_donations_screen import ViewDonationsScreen
from screens.view_donations_screen import EditDonationScreen
from tkcalendar import DateEntry
from babel import numbers
import sqlite3
from tkinter import messagebox

def get_image_path(filename):
    # Obtém o diretório do script principal (main.py)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Constrói o caminho para a imagem usando o diretório do script
    image_path = os.path.join(script_dir, 'assets', filename)

    # Se o arquivo não for encontrado, tente outra abordagem
    if not os.path.exists(image_path):
        image_path = os.path.join(os.path.abspath('assets'), filename)

    return image_path

# Caminho das imagens de ícones
icone_path = get_image_path("icone.png")
icone4_path = get_image_path("icone4.png")
icone2_path = get_image_path("icone2.png")
icone7_path = get_image_path("icone7.png")

# Chame as funções conforme necessário para usar os caminhos das imagens

def show_login_screen():
    image = Image.open(get_image_path("clini2.jpeg"))
    background_image = ImageTk.PhotoImage(image)
    login_root = tk.Toplevel()
    login_app = LoginScreen(login_root, background_image)
    login_root.mainloop()

def show_options_screen():
    image_path = get_image_path("clini3.jpeg")
    background_image = Image.open(image_path)
    background_image_tk = ImageTk.PhotoImage(background_image)
    options_root = tk.Toplevel()
    options_app = OptionsScreen(options_root, background_image_tk, get_image_path)
    options_root.mainloop()

def show_appointment_screen():
    appointment_root = tk.Toplevel()
    appointment_app = AppointmentScreen(appointment_root)
    appointment_root.mainloop()

def show_donation_registration_screen():
    donation_root = tk.Toplevel()
    donation_app = DonationRegistrationScreen(donation_root)
    donation_root.mainloop()

def show_view_appointments_screen():
    view_appointments_root = tk.Tk()
    view_appointments_app = ViewAppointmentsScreen(view_appointments_root)
    view_appointments_root.mainloop()

def show_view_donations_screen():
    view_donations_root = tk.Tk()
    view_donations_app = ViewDonationsScreen(view_donations_root)
    view_donations_root.mainloop()
    
if __name__ == "__main__":
    root = tk.Tk()
    login_app = LoginScreen(root, lambda: show_options_screen(), get_image_path)
    root.protocol("WM_DELETE_WINDOW", lambda: root.quit())  # Adicione esta linha
    root.mainloop()
