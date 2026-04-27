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
import random

from tkinter import ttk, messagebox
from wrapper import search_movies, get_movie, get_genres, get_final_recommendation
from PIL import Image, ImageTk
from io import BytesIO
from quotes import quotes

current_user_id = None  # Global variable to store the currently logged-in user's information
search_results_data = []  # Global variable to store the data of the movies currently displayed in the search results
favorites_data = []  # Global variable to store the data of the movies currently in the user's favorites list
all_genres = get_genres() #Global variable that initializes genres
# -----------------------------
# MAIN WINDOW SETUP
# -----------------------------

# Create the main window
root = tk.Tk()

# Set the title of the application window
root.title("Movie Recommendation App")

# Set the starting size of the window
root.geometry("1100x800")

# Prevent the window from becoming too small
root.minsize(850, 550)

# Apply the Sun Valley dark theme
sv_ttk.set_theme("dark")


# -----------------------------
# PAGE SWITCHING FUNCTIONS
# -----------------------------

def show_registration_page():
    search_page.pack_forget()
    login_page.pack_forget()
    clear_login_fields()
    registration_page.pack(fill="both", expand=True)


def show_search_page():
    registration_page.pack_forget()
    login_page.pack_forget()
    search_page.pack(fill="both", expand=True)


def show_login_page():
    registration_page.pack_forget()
    search_page.pack_forget()
    clear_registration_fields()
    login_page.pack(fill="both", expand=True)

def show_recommendations_page():
    search_page.pack_forget()
    login_page.pack_forget()
    registration_page.pack_forget()
    load_recommendation_posters()
    recommendations_page.pack(fill="both", expand = True)

def show_search_from_recommendations():
    recommendations_page.pack_forget()
    search_page.pack(fill = "both", expand = True)

def logout_user():
    global current_user_id
    current_user_id = None
    favorites_list.delete(0, tk.END)
    show_login_page()


# -----------------------------
# CLEAR FIELDS FUNCTIONS
# -----------------------------


def clear_login_fields():
    login_username_entry.delete(0, tk.END)
    login_password_entry.delete(0, tk.END)

def clear_registration_fields():
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    confirm_password_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)


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
                rating INTEGER,
                UNIQUE(user_id, movie_id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS not_interested (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                movie_id TEXT NOT NULL,
                UNIQUE(user_id, movie_id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        try:
            cursor.execute("ALTER TABLE favorites ADD COLUMN rating INTEGER")
        except sqlite3.OperationalError:
            pass  # Column already exists

# -----------------------------
# LOGIN PAGE
# -----------------------------

login_page = ttk.Frame(root, padding=20)

login_wrapper = ttk.Frame(login_page)
login_wrapper.pack(fill="both", expand=True)

login_card = ttk.Frame(login_wrapper, padding=30)
login_card.place(relx=0.5, rely=0.5, anchor="center")

login_title = ttk.Label(
    login_card,
    text="Welcome Back!",
    font=("Segeo UI", 24, "bold")
)
login_title.pack(pady=(0, 10))

login_subtitle = ttk.Label(
    login_card,
    text="Your next favorite movie is waiting.",
    font=("Segeo UI", 12)
)
login_subtitle.pack(pady=(0, 20))

login_form_frame = ttk.Frame(login_card)
login_form_frame.pack(fill="x")

login_username_label = ttk.Label(
    login_form_frame,
    text="Username:",
    font=("Segeo UI", 12)
)
login_username_label.pack(anchor="w", pady=(5, 5))

login_username_entry = ttk.Entry(
    login_form_frame,
    font=("Segeo UI", 12),
    width=35
)
login_username_entry.pack(fill="x", ipady=6)

login_password_label = ttk.Label(
    login_form_frame,
    text="Password:",
    font=("Segeo UI", 12)
)
login_password_label.pack(anchor="w", pady=(15, 5))

login_password_entry = ttk.Entry(
    login_form_frame,
    font=("Segeo UI", 12),
    width=35,
    show="*"
)
login_password_entry.pack(fill="x", ipady=6, pady=(0, 20))

def login_user():
    global current_user_id

    username = login_username_entry.get().strip()
    password = login_password_entry.get().strip()

    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return

    with sqlite3.connect("users.db", timeout=10) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id FROM users WHERE username = ? AND password = ?",
            (username, password)
        )
        user = cursor.fetchone()

    if user:
        current_user_id = user[0]
        messagebox.showinfo("Success", f"Welcome back, {username}!")
        clear_login_fields()
        load_favorites()
        show_search_page()
    else:
        messagebox.showerror("Error", "Invalid username or password.")

login_button = ttk.Button(
    login_card,
    text="Login",
    command=login_user
)
login_button.pack(fill="x", ipady=8, pady=(0, 10))

go_to_register_button = ttk.Button(
    login_card,
    text="Create Account",
    command=show_registration_page
)
go_to_register_button.pack(fill="x", ipady=8)


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
    font=("Segeo UI", 24, "bold")
)
reg_title.pack(pady=(0, 10))

# Registration page subtitle
reg_subtitle = ttk.Label(
    reg_card,
    text="Register Down Below",
    font=("Segeo UI", 12)
)
reg_subtitle.pack(pady=(0, 20))

# Form container
form_frame = ttk.Frame(reg_card)
form_frame.pack(fill="x")

# Username label
username_label = ttk.Label(
    form_frame,
    text="Username:",
    font=("Segeo UI", 12)
)
username_label.pack(anchor="w", pady=(5, 5))

# Username entry
username_entry = ttk.Entry(
    form_frame,
    font=("Segeo UI", 12),
    width=35
)
username_entry.pack(fill="x", ipady=6)

# Password label
password_label = ttk.Label(
    form_frame,
    text="Password:",
    font=("Segeo UI", 12)
)
password_label.pack(anchor="w", pady=(15, 5))

# Password entry
password_entry = ttk.Entry(
    form_frame,
    font=("Segeo UI", 12),
    width=35,
    show="*"
)
password_entry.pack(fill="x", ipady=6)

# Confirm password label
confirm_password_label = ttk.Label(
    form_frame,
    text="Confirm Password:",
    font=("Segeo UI", 12)
)
confirm_password_label.pack(anchor="w", pady=(15, 5))

# Confirm password entry
confirm_password_entry = ttk.Entry(
    form_frame,
    font=("Segeo UI", 12),
    width=35,
    show="*"
)
confirm_password_entry.pack(fill="x", ipady=6)

# Email label
email_label = ttk.Label(
    form_frame,
    text="Email:",
    font=("Segeo UI", 12)
)
email_label.pack(anchor="w", pady=(15, 5))

# Email entry
email_entry = ttk.Entry(
    form_frame,
    font=("Segeo UI", 12),
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

back_to_login_button = ttk.Button(
    reg_card,
    text="Back to Login",
    command=show_login_page
)
back_to_login_button.pack(fill="x", ipady=8, pady=(0, 10))


continue_button = ttk.Button(
    reg_card,
    text="Continue to App",
    command=show_search_page
)
continue_button.pack(fill="x", ipady=8)


# -----------------------------
# SEARCH PAGE
# -----------------------------

def get_rating_from_user(movie_title):
    rating_result = [None]

    dialog = tk.Toplevel(root)
    dialog.title("Rate this Movie")
    dialog.geometry("340x180")
    dialog.resizable(False, False)
    dialog.grab_set()

    ttk.Label(
        dialog,
        text=f"Rate \"{movie_title}\"",
        font=("Segeo UI", 13, "bold"),
        wraplength=300,
        justify="center"
    ).pack(pady=(20, 5))

    ttk.Label(dialog, text="Select a rating (1–10):", font=("Segeo UI", 11)).pack()

    rating_var = tk.IntVar(value=7)
    scale = ttk.Scale(dialog, from_=1, to=10, orient="horizontal", variable=rating_var, length=220)
    scale.pack(pady=(8, 0))

    scale_label = ttk.Label(dialog, text="7", font=("Segeo UI", 12, "bold"))
    scale_label.pack()

    def update_label(e=None):
        scale_label.config(text=str(int(rating_var.get())))
    scale.bind("<Motion>", update_label)
    scale.bind("<ButtonRelease-1>", update_label)

    def confirm():
        rating_result[0] = int(rating_var.get())
        dialog.destroy()

    ttk.Button(dialog, text="Add to Favorites", command=confirm).pack(pady=(10, 0), ipady=5)
    root.wait_window(dialog)
    return rating_result[0]


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

    rating = get_rating_from_user(movie["title"])
    if rating is None:
        return  # User closed the dialog without rating

    try:
        with sqlite3.connect("users.db", timeout=10) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO favorites (user_id, movie_id, movie_title, movie_year, rating)
                VALUES (?, ?, ?, ?, ?)
            """, (
                current_user_id,
                movie["id"],
                movie["title"],
                movie["year"],
                rating
            ))

        load_favorites()

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "This movie is already in your favorites.")


def load_favorites():
    global current_user_id, favorites_data

    favorites_list.delete(0, tk.END)
    favorites_data = []  # Clear previous favorites data

    if current_user_id is None:
        return

    with sqlite3.connect("users.db", timeout=10) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, movie_id, movie_title, movie_year, rating FROM favorites WHERE user_id = ?",
            (current_user_id,)
        )
        rows = cursor.fetchall()

    rows = sorted(rows, key=lambda r: r[4] if r[4] is not None else 0, reverse=True)

    for favorite_id, movie_id, title, year, rating in rows:
        rating_str = f"  ★ {rating}/10" if rating is not None else ""
        favorites_list.insert(tk.END, f"{title} ({year}){rating_str}")
        favorites_data.append({
            "id": favorite_id,
            "movie_id": movie_id,
            "title": title,
            "year": year,
            "rating": rating
        })

def edit_favorite_rating():
    global current_user_id, favorites_data

    if current_user_id is None:
        messagebox.showerror("Error", "You must be logged in.")
        return

    selected_index = favorites_list.curselection()

    if not selected_index:
        messagebox.showerror("Error", "Please select a favorite movie to edit.")
        return

    selected_index = selected_index[0]
    favorite = favorites_data[selected_index]

    new_rating = get_rating_from_user(favorite["title"])
    if new_rating is None:
        return

    with sqlite3.connect("users.db", timeout=10) as connection:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE favorites SET rating = ?
            WHERE id = ? AND user_id = ?
        """, (new_rating, favorite["id"], current_user_id))

    load_favorites()


def remove_from_favorites():
    global current_user_id, favorites_data

    if current_user_id is None:
        messagebox.showerror("Error", "You must be logged in.")
        return

    selected_index = favorites_list.curselection()

    if not selected_index:
        messagebox.showerror("Error", "Please select a favorite movie to remove.")
        return

    selected_index = selected_index[0]
    favorite = favorites_data[selected_index]

    with sqlite3.connect("users.db", timeout=10) as connection:
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM favorites
            WHERE id = ? AND user_id = ?
        """, (favorite["id"], current_user_id))


    load_favorites()


# Main frame for the search page
search_page = ttk.Frame(root, padding=25)

# Header section
header_frame = ttk.Frame(search_page)
header_frame.pack(fill="x", pady=(0, 20))

# Search page title
search_title = ttk.Label(
    header_frame,
    text="Movie Recommendation App",
    font=("Segeo UI", 24, "bold")
)
search_title.pack(anchor="w")

#Movie quotes
quote_label = ttk.Label(
    header_frame,
    text = random.choice(quotes),
    font = ("Segeo UI", 16)
)
quote_label.pack(anchor="w", pady=(5,0))

def rotate_quote():
    quote_label.config(text = random.choice(quotes))
    root.after(15000, rotate_quote)
root.after(15000, rotate_quote)

# Search card
search_card = ttk.Frame(search_page, padding=20)
search_card.pack(fill="x", pady=(0, 18))

# Search section title
search_label = ttk.Label(
    search_card,
    text="Search",
    font=("Segeo UI", 14, "bold")
)
search_label.pack(anchor="w", pady=(0, 12))

# Row for search bar and buttons
search_row = ttk.Frame(search_card)
search_row.pack(fill="x")

# Search bar
search_bar = ttk.Entry(
    search_row,
    font=("Segeo UI", 14)
)
search_bar.pack(side="left", fill="x", expand=True, ipady=6)

# Add to Favorites button
favorites_button = ttk.Button(
    search_row,
    text="Add to Favorites",
    command=add_to_favorites
)
favorites_button.pack(side="left", padx=(10, 0), ipady=6)

# Remove Favorite button
remove_favorite_button = ttk.Button(
    search_row,
    text="Remove Favorite",
    command=remove_from_favorites
)
remove_favorite_button.pack(side="left", padx=(10, 0), ipady=6)

# Edit Rating button
edit_rating_button = ttk.Button(
    search_row,
    text="Edit Rating",
    command=edit_favorite_rating
)
edit_rating_button.pack(side="left", padx=(10, 0), ipady=6)

# Get Recommendations button
recommendations_button = ttk.Button(
    search_row,
    text="Get Recommendations",
    command=show_recommendations_page
)
recommendations_button.pack(side="left", padx=(10, 0), ipady=6)

# Logout button
logout_button = ttk.Button(
    search_row,
    text="Logout",
    command=logout_user
)
logout_button.pack(side="left", padx=(10, 0), ipady=6)

# Results card
results_card = ttk.Frame(search_page, padding=20)
results_card.pack(fill="both", expand=True)

# Results label
results_label = ttk.Label(
    results_card,
    text="Search Results:",
    font=("Segeo UI", 14, "bold")
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
    font=("Segeo UI", 14),
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


favorites_label = ttk.Label(
    results_card,
    text="Your Favorites:",
    font=("Segeo UI", 14, "bold")
)
favorites_label.pack(anchor="w", pady=(15, 8))

favorites_list = tk.Listbox(
    results_card,
    font=("Segeo UI", 14),
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

def sample_search():
    global search_results_data

    query = search_bar.get().strip()
    search_results.delete(0, tk.END)
    search_results_data = []

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

    if not search_results_data:
        search_results.insert(tk.END, "No results.")

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
        font=("Segeo UI", 20, "bold")
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
        font=("Segeo UI", 11)
    ).pack(anchor="w", pady = 2)

    ttk.Label(
        info_frame,
        text=f"Rating: {rating}",
        font=("Segeo UI", 11)
    ).pack(anchor="w", pady = 2)

    ttk.Label(
        info_frame,
        text=f"Runtime: {runtime} minutes",
        font=("Segeo UI", 11)
    ).pack(anchor="w", pady = 2)

    ttk.Label(
        info_frame,
        text=f"Genres: {genre_names}",
        font=("Segeo UI", 11)
    ).pack(anchor="w", pady = 2)

    ttk.Label(
        container,
        text = "Synopsis",
        font = ("Segeo UI", 14, "bold")
    ).pack(anchor="w", pady=(10, 5))

    overview_text = tk.Text(
        container,
        font=("Segeo UI", 11),
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
        font=("Segeo UI", 14, "bold")
    ).pack(anchor="w", pady = (5, 5))

    ttk.Label(
        container,
        text=cast_names,
        font=("Segeo UI", 11),
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
# RECOMMENDATIONS PAGE
# -----------------------------

recommendations_page = ttk.Frame(root, padding = 25)

#Header
rec_header_frame = ttk.Frame(recommendations_page)
rec_header_frame.pack (fill = "x", pady=(0,20))

rec_title = ttk.Label(
    rec_header_frame,
    text = "Your Recommendations",
    font=("Segeo UI", 24, "bold")
)
rec_title.pack(anchor="w")

#Back Button
rec_back_button = ttk.Button(
    recommendations_page,
    text= "Back",
    command = show_search_from_recommendations
)
rec_back_button.pack(anchor = "w", pady = (0,15))

rec_grid_frame = ttk.Frame(recommendations_page, padding=10)
rec_grid_frame.pack(fill="both", expand=True)

poster_images = []

def load_recommendation_posters():
    global poster_images
    poster_images = []

    for widget in rec_grid_frame.winfo_children():
        widget.destroy()

    if not favorites_data:
        ttk.Label(
            rec_grid_frame,
            text="Add movies to your favorites to get recommendations.",
            font=("Helvetica", 12)
        ).grid(row=0, column=0)
        return

    favorite_ids = [str(f["movie_id"]) for f in favorites_data]
    recommended = get_final_recommendation(favorite_ids)

    #get hidden movies
    with sqlite3.connect("users.db", timeout=10) as connection:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT movie_id FROM not_interested WHERE user_id = ?",
            (current_user_id,)
        )

        hidden_ids = {str(row[0]) for row in cursor.fetchall()}

    #filter recommended
    recommended = [
        m for m in recommended
        if str(m.get("id")) not in hidden_ids
    ]

    if not recommended:
        ttk.Label(
            rec_grid_frame,
            text="No recommendations available.",
            font=("Segeo UI", 12)
        ).grid(row=0, column=0)
        return

    # continue normally
    for index, movie in enumerate(recommended):
        row = index // 5
        col = index % 5

    for index, movie in enumerate(recommended):
        row = index // 5
        col = index % 5

        movie_frame = ttk.Frame(rec_grid_frame, padding=5)
        movie_frame.grid(row=row, column=col, padx=10, pady=10)

        movie_id = movie.get("id")

        not_interested_btn = ttk.Button(
            movie_frame,
            text="Not Interested",
            command=lambda m_id=movie_id, f=movie_frame: mark_not_interested_recommendation(m_id, f)
        )
        not_interested_btn.pack(pady=(5, 0))

        poster_label = ttk.Label(movie_frame)
        poster_label.pack()

        title = movie.get("title", "Unknown")
        year = movie.get("release_date", "")[:4]

        ttk.Label(
            movie_frame,
            text=f"{title} ({year})",
            font=("Helvetica", 9),
            wraplength=100,
            justify="center"
        ).pack(pady=(5, 0))

        poster_path = movie.get("poster_path")
        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w200{poster_path}"
            response = requests.get(poster_url, timeout=10)
            image_data = Image.open(BytesIO(response.content))
            image_data = image_data.resize((100, 150))
            poster_image = ImageTk.PhotoImage(image_data)
            poster_label.config(image=poster_image)
            poster_label.image = poster_image
            poster_images.append(poster_image)
        else:
            poster_label.config(text="No Poster")

#Not Interested
def mark_not_interested_recommendation(movie_id, frame):
    global current_user_id

    if current_user_id is None:
        return

    try:
        with sqlite3.connect("users.db", timeout=10) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO not_interested (user_id, movie_id)
                VALUES (?, ?)
            """, (current_user_id, movie_id))

    #Remove movie visually from the grid
    except sqlite3.IntegrityError:
        frame.destroy()

# -----------------------------
# START APP
# -----------------------------

#Set up database before starting the app
initialize_database()

# Start the Tkinter event loop
show_login_page()
root.mainloop()
