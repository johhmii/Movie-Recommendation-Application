# Movie Recommendation App
# Contributors:
# Marco Guirguis
# Eric Luu
# Johnny Rivera
# David Ulloa
# Andy Vu

import sqlite3 #Python's built in database, Sufficient for our needs and easy to set up, no external dependencies required
import tkinter as tk
from tkinter import ttk, messagebox
from wrapper import search_movies, get_movie
import requests
import sv_ttk


# -----------------------------
# MAIN WINDOW SETUP
# -----------------------------

# Create the main window
root = tk.Tk()

# Set the title of the application window
root.title("Movie Recommendation App")

# Set the starting size of the window
root.geometry("950x650")

# Prevent the window from becoming too small
root.minsize(850, 550)

# Apply the Sun Valley dark theme
sv_ttk.set_theme("dark")


# -----------------------------
# PAGE SWITCHING FUNCTIONS
# -----------------------------

def show_registration_page():
    """Hide the search page and show the registration page."""
    search_page.pack_forget()
    registration_page.pack(fill="both", expand=True)


def show_search_page():
    """Hide the registration page and show the search page."""
    registration_page.pack_forget()
    search_page.pack(fill="both", expand=True)


# -----------------------------
# SQLITE3 DATABASE SETUP
# -----------------------------

def setup_database():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       username TEXT NOT NULL UNIQUE,
                       password TEXT NOT NULL,
                       email TEXT NOT NULL UNIQUE
                   )
                   """)

    connection.commit()
    connection.close()

# -----------------------------
# REGISTRATION PAGE
# -----------------------------

# Main frame for the registration page
registration_page = ttk.Frame(root, padding=20)

# Wrapper frame helps center the registration card
reg_wrapper = ttk.Frame(registration_page)
reg_wrapper.pack(fill="both", expand=True)

# Card-style frame for the registration form
reg_card = ttk.Frame(reg_wrapper, padding=30)
reg_card.place(relx=0.5, rely=0.5, anchor="center")

# Registration page title
reg_title = ttk.Label(
    reg_card,
    text="Create Your Account",
    font=("Helvetica", 24, "bold")
)
reg_title.pack(pady=(0, 10))

# Registration page subtitle
reg_subtitle = ttk.Label(
    reg_card,
    text="Register Down Below",
    font=("Helvetica", 12)
)
reg_subtitle.pack(pady=(0, 20))

# Form container
form_frame = ttk.Frame(reg_card)
form_frame.pack(fill="x")

# Username label
username_label = ttk.Label(
    form_frame,
    text="Username:",
    font=("Helvetica", 12)
)
username_label.pack(anchor="w", pady=(5, 5))

# Username entry
username_entry = ttk.Entry(
    form_frame,
    font=("Helvetica", 12),
    width=35
)
username_entry.pack(fill="x", ipady=6)

# Password label
password_label = ttk.Label(
    form_frame,
    text="Password:",
    font=("Helvetica", 12)
)
password_label.pack(anchor="w", pady=(15, 5))

# Password entry
password_entry = ttk.Entry(
    form_frame,
    font=("Helvetica", 12),
    width=35,
    show="*"
)
password_entry.pack(fill="x", ipady=6)

# Confirm password label
confirm_password_label = ttk.Label(
    form_frame,
    text="Confirm Password:",
    font=("Helvetica", 12)
)
confirm_password_label.pack(anchor="w", pady=(15, 5))

# Confirm password entry
confirm_password_entry = ttk.Entry(
    form_frame,
    font=("Helvetica", 12),
    width=35,
    show="*"
)
confirm_password_entry.pack(fill="x", ipady=6)

# Email label
email_label = ttk.Label(
    form_frame,
    text="Email:",
    font=("Helvetica", 12)
)
email_label.pack(anchor="w", pady=(15, 5))

# Email entry
email_entry = ttk.Entry(
    form_frame,
    font=("Helvetica", 12),
    width=35
)
email_entry.pack(fill="x", ipady=6, pady=(0, 20))


def register_user():
    """Validate registration form and switch to the search page if valid."""
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    confirm_password = confirm_password_entry.get().strip()
    email = email_entry.get().strip()

    # Make sure all fields are filled out
    if not username or not password or not confirm_password or not email:
        messagebox.showerror("Error", "All fields are required.")
        return

    # Basic email validation
    if "@" not in email or "." not in email:
        messagebox.showerror("Error", "Invalid email format.")
        return

    # Confirm both password fields match
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match.")
        return


    # Save username, password, and email as plain text in the database, may need to hash later

    try:
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                       (username, password, email))
        connection.commit()
        connection.close()

        messagebox.showinfo("Success", "Registration successful!")
        show_search_page()

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username or email already exists.")



# Registration page buttons
register_button = ttk.Button(
    reg_card,
    text="Register",
    command=register_user
)
register_button.pack(fill="x", ipady=8, pady=(0, 10))

continue_button = ttk.Button(
    reg_card,
    text="Continue to App",
    command=show_search_page
)
continue_button.pack(fill="x", ipady=8)


# -----------------------------
# SEARCH PAGE
# -----------------------------

# Main frame for the search page
search_page = ttk.Frame(root, padding=25)

# Header section
header_frame = ttk.Frame(search_page)
header_frame.pack(fill="x", pady=(0, 20))

# Search page title
search_title = ttk.Label(
    header_frame,
    text="Movie Recommendation App",
    font=("Helvetica", 24, "bold")
)
search_title.pack(anchor="w")

# Search page subtitle
search_subtitle = ttk.Label(
    header_frame,
    text="Search for your favorite movies",
    font=("Helvetica", 12)
)
search_subtitle.pack(anchor="w", pady=(5, 0))

# Search card
search_card = ttk.Frame(search_page, padding=20)
search_card.pack(fill="x", pady=(0, 18))

# Search section title
search_label = ttk.Label(
    search_card,
    text="Search",
    font=("Helvetica", 14, "bold")
)
search_label.pack(anchor="w", pady=(0, 12))

# Row for search bar and buttons
search_row = ttk.Frame(search_card)
search_row.pack(fill="x")

# Search bar
search_bar = ttk.Entry(
    search_row,
    font=("Helvetica", 14)
)
search_bar.pack(side="left", fill="x", expand=True, ipady=6)

# Optional manual search button
search_button = ttk.Button(
    search_row,
    text="Search",
    command=lambda: sample_search()
)
search_button.pack(side="left", padx=(10, 0), ipady=6)

# Back button
back_button = ttk.Button(
    search_row,
    text="Back to Registration",
    command=show_registration_page
)
back_button.pack(side="left", padx=(10, 0), ipady=6)

# Results card
results_card = ttk.Frame(search_page, padding=20)
results_card.pack(fill="both", expand=True)

# Results label
results_label = ttk.Label(
    results_card,
    text="Search Results:",
    font=("Helvetica", 14, "bold")
)
results_label.pack(anchor="w", pady=(0, 12))

# Frame to hold the listbox and scrollbar
listbox_frame = ttk.Frame(results_card)
listbox_frame.pack(fill="both", expand=True)

# Scrollbar for the results list
scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical")
scrollbar.pack(side="right", fill="y")

# Listbox for displaying movie results
# This stays as tk.Listbox because ttk does not provide a Listbox widget
search_results = tk.Listbox(
    listbox_frame,
    font=("Helvetica", 14),
    height=12,
    bg="#2b2b2b",
    fg="white",
    selectbackground="#4a90e2",
    selectforeground="white",
    relief="flat",
    highlightthickness=0,
    yscrollcommand=scrollbar.set
)
search_results.pack(fill="both", expand=True)

# Connect scrollbar to listbox
scrollbar.config(command=search_results.yview)


#Keystroke search function, 
search_delay = None                                  #Initialize to 0
def on_keyrelease(event):                            #Function runs after each keystroke
    global search_delay  
    if search_delay:                                 #If search_delay is already running cancel it
        root.after_cancel(search_delay)
    search_delay = root.after(300, sample_search)    #Start a 300ms delay as to not overwhelm API with calls
search_bar.bind("<KeyRelease>", on_keyrelease)       #Bind function to searchbar

#TEMP SAMPLE SEARCH FUNCTION
def sample_search():

    query = search_bar.get().strip()
    search_results.delete(0, tk.END)

    movies = search_movies(query)

    if not movies:
            search_results.insert(tk.END, "No results.")
            return
    for movie in movies:
        title = movie.get("title", "Unknown")
        year = movie.get("release_date", "")[:4]
        search_results.insert(tk.END, f"{title} ({year})")


# -----------------------------
# START APP
# -----------------------------

# Start on the registration page
registration_page.pack(fill="both", expand=True)


#Set up database before starting the app
setup_database()

# Start the Tkinter event loop
root.mainloop()