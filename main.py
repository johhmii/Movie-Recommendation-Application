# Movie Recommendation App
# Contributors:
# Marco Guirguis
# Eric Luu
# Johnny Rivera
# David Ulloa
# Andy Vu

import sqlite3 #Python's built in database, Sufficient for our needs and easy to set up, no external dependencies required
import tkinter as tk
import requests
import sv_ttk

from tkinter import ttk, messagebox
from wrapper import search_movies, get_movie
from PIL import Image, ImageTk
from io import BytesIO

current_user_id = None  # Global variable to store the currently logged-in user's information
search_results_data = []  # Global variable to store the data of the movies currently displayed in the search results

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

def initialize_database():
    with sqlite3.connect("users.db", timeout=10) as connection:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                movie_id TEXT NOT NULL,
                movie_title TEXT NOT NULL,
                movie_year TEXT,
                UNIQUE(user_id, movie_id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
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

    global current_user_id

    username = username_entry.get().strip()
    password = password_entry.get().strip()
    confirm_password = confirm_password_entry.get().strip()
    email = email_entry.get().strip()

    if not username or not password or not confirm_password or not email:
        messagebox.showerror("Error", "All fields are required.")
        return

    if "@" not in email or "." not in email:
        messagebox.showerror("Error", "Invalid email format.")
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match.")
        return

    try:
        with sqlite3.connect("users.db", timeout=10) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                (username, password, email)
            )
            current_user_id = cursor.lastrowid

        messagebox.showinfo("Success", "Registration successful!")
        load_favorites()
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

def add_to_favorites():
    global current_user_id

    if current_user_id is None:
        messagebox.showerror("Error", "You must be logged in to add favorites.")
        return

    selected_index = search_results.curselection()

    if not selected_index:
        messagebox.showerror("Error", "Please select a movie to add to favorites.")
        return

    selected_index = selected_index[0]
    movie = search_results_data[selected_index]

    try:
        with sqlite3.connect("users.db", timeout=10) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO favorites (user_id, movie_id, movie_title, movie_year)
                VALUES (?, ?, ?, ?)
            """, (
                current_user_id,
                movie["id"],
                movie["title"],
                movie["year"]
            ))

        messagebox.showinfo("Success", f"{movie['title']} has been added to your favorites!")
        load_favorites()

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "This movie is already in your favorites.")


def load_favorites():
    global current_user_id

    favorites_list.delete(0, tk.END)

    if current_user_id is None:
        return

    with sqlite3.connect("users.db", timeout=10) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT movie_title, movie_year FROM favorites WHERE user_id = ?",
            (current_user_id,)
        )
        rows = cursor.fetchall()

    for title, year in rows:
        favorites_list.insert(tk.END, f"{title} ({year})")



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

# Add to Favorites button
favorites_button = ttk.Button(
    search_row,
    text="Add to Favorites",
    command = add_to_favorites
)
favorites_button.pack(side="left", padx=(10, 0), ipady=6)

favorites_label = ttk.Label(
    results_card,
    text="Your Favorites:",
    font=("Helvetica", 14, "bold")
)
favorites_label.pack(anchor="w", pady=(15, 8))

favorites_list = tk.Listbox(
    results_card,
    font=("Helvetica", 14),
    height=8,
    bg="#2b2b2b",
    fg="white",
    selectbackground="#4a90e2",
    selectforeground="white",
    relief="flat",
    highlightthickness=0
)
favorites_list.pack(fill="both", expand=True, pady=(0, 10))


#Keystroke search function, 
search_delay = None                                  #Initialize to 0
def on_keyrelease(event):                            #Function runs after each keystroke
    global search_delay  
    if search_delay:                                 #If search_delay is already running cancel it
        root.after_cancel(search_delay)
    search_delay = root.after(300, sample_search)    #Start a 300ms delay as to not overwhelm API with calls
search_bar.bind("<KeyRelease>", on_keyrelease)       #Bind function to searchbar

#TEMP SAMPLE SEARCH FUNCTION
search_results_data = []; 

def sample_search():
    global search_results_data

    query = search_bar.get().strip()
    search_results.delete(0, tk.END)
    search_results_data = []  # Clear previous search results data

    movies = search_movies(query)

    if not movies:
            search_results.insert(tk.END, "No results.")
            return
    
    for movie in movies:
        title = movie.get("title", "Unknown")
        year = movie.get("release_date", "")[:4]
        movie_id = movie.get("id", "")

        search_results.insert(tk.END, f"{title} ({year})")
        search_results_data.append({
            "id": movie_id,
            "title": title,
            "year": year
        })

def show_movie_details(events = None):
    selected_index = search_results.curselection()

    if not selected_index:
        return

    selected_index = selected_index[0]
    movie = search_results_data[selected_index]

    details = get_movie(movie["id"])

    if details is None:
        messagebox.showerror("Error", "Failed to retrieve movie details.")
        return
    
    #create popup with movie details, including title, release year, overview, and rating
    details_window = tk.Toplevel(root)
    details_window.title(details.get("title", "Movie Details"))
    details_window.geometry("700x600")
    details_window.minsize(600, 500)

    #main container
    container = ttk.Frame(details_window, padding=20)
    container.pack(fill="both", expand=True)

    #top section for poster and basic info
    top_frame = ttk.Frame(container)
    top_frame.pack(fill="x", pady=(0, 15))

    #poster label 
    poster_label = ttk.Label(top_frame)
    poster_label.pack(side="left", padx=(0, 20))

    #right side info
    info_frame = ttk.Frame(top_frame)
    info_frame.pack(side="left", fill="both", expand=True)

    #title label
    ttk.Label(
        info_frame,
        text=details.get("title", "Unknown"),
        font=("Helvetica", 20, "bold")
    ).pack(anchor="w", pady = (0, 10))

    #basic details
    release_date = details.get("release_date", "Unknown")
    rating = details.get("vote_average", "N/A")
    runtime = details.get("runtime", "Unknown")

    genres = details.get("genres", [])
    genre_names = ", ".join(g["name"] for g in genres) if genres else "Unknown"

    ttk.Label(
        info_frame,
        text=f"Release Date: {release_date}",
        font=("Helvetica", 11)
    ).pack(anchor="w", pady = 2)

    ttk.Label(
        info_frame,
        text=f"Rating: {rating}",
        font=("Helvetica", 11)
    ).pack(anchor="w", pady = 2)

    ttk.Label(
        info_frame,
        text=f"Runtime: {runtime} minutes",
        font=("Helvetica", 11)
    ).pack(anchor="w", pady = 2)

    ttk.Label(
        info_frame,
        text=f"Genres: {genre_names}",
        font=("Helvetica", 11)
    ).pack(anchor="w", pady = 2)

    ttk.Label(
        container,
        text = "Synopsis",
        font = ("Helvetica", 14, "bold")
    ).pack(anchor="w", pady=(10, 5))

    overview_text = tk.Text(
        container,
        font=("Helvetica", 11),
        wrap="word",
        height=8,
        bg="#2b2b2b",
        fg="white",
        relief="flat",
    )
    overview_text.pack(fill = "x", pady = (0, 15))

    overview = details.get("overview", "No synopsis available.")
    overview_text.insert("1.0", overview)
    overview_text.config(state="disabled")

    #actors section

    cast_names = "Unknown"
    if "credits" in details and "cast" in details:
        cast_list = details["credits"]["cast"][:5]  # Get top 5 cast members
        cast_names = ", ".join(actor["name"] for actor in cast_list) if cast_list else "Unknown"

    ttk.Label(
        container,
        text=f"Top Cast:",
        font=("Helvetica", 14, "bold")
    ).pack(anchor="w", pady = (5, 5))

    ttk.Label(
        container,
        text=cast_names,
        font=("Helvetica", 11),
        wraplength = 620,
        justify = "left",
    ).pack(anchor="w", pady = (0, 15))

    #load poster image

    poster_path = details.get("poster_path")
    if poster_path:
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        try:
            response = requests.get(poster_url, timeout=10)
            image_data = Image.open(BytesIO(response.content))
            image_data = image_data.resize((200, 300))
            poster_image = ImageTk.PhotoImage(image_data)

            poster_label.config(image=poster_image)
            poster_label.image = poster_image  # Keep a reference to prevent garbage collection

        except Exception:
            poster_label.config(text = "Poster not Available")
    
    else:
        poster_label.config(text = "Poster not Available")

#show movie details on double click
search_results.bind("<Double-Button-1>", show_movie_details)

# -----------------------------
# START APP
# -----------------------------

# Start on the registration page
registration_page.pack(fill="both", expand=True)


#Set up database before starting the app
initialize_database()

# Start the Tkinter event loop
root.mainloop()