#Movie Recommendation App
#Contributors:
#Marco Guirguis
#Eric Luu
#Johnny Rivera
#David Ulloa
#Andy Vu

import tkinter as tk

# Creates main window
root = tk.Tk()

#Sets the title of the window (Need name for app)
root.title("Movie Recommendation App")

#Sets the size of the window
root.geometry("700x500")

#Sets the background color of the window
root.configure(bg="#1e1e1e")

# Create search bar
search_bar = tk.Entry(root, font=("Helvetica", 20), width = 28)
search_bar.pack(pady=20, padx=20)

#Title Section

title_label = tk.Label(
    root,
    text="Movie Recommendation App",
    font=("Helvetica", 24, "bold"),
    bg = "#1e1e1e",
    fg = "white"
)
title_label.pack(pady=(20, 10))

#Add small subttitle under the main title
subtitle_label = tk.Label(
    root,
    text="Find your next favorite movie and manage your account",
    font=("Helvetica", 12),
    bg="#1e1e1e",
    fg="#cfcfcf"
)
subtitle_label.pack(pady=(0, 20))

searchResults = tk.Listbox(root, font=("Helvetica", 20), height = 20)
searchResults.pack(fill=tk.BOTH, expand = True, padx = 20, pady = 20)

def open_registration():
    reg_window = tk.Toplevel(root)
    reg_window.title("User Registration")
    reg_window.geometry("400x300")

    tk.Label(reg_window, text="Username:", font=("Helvetica", 14)).pack(pady=10)
    username_entry = tk.Entry(reg_window, font=("Helvetica", 14))
    username_entry.pack()

    tk.Label(reg_window, text="Password:", font=("Helvetica", 14)).pack(pady=10)
    password_entry = tk.Entry(reg_window, font=("Helvetica", 14), show="*")
    password_entry.pack()
    
    tk.Label(reg_window, text = "Confirm Password:", font = ("Helvetica", 14)).pack(pady = 10)
    confirm_password_entry = tk.Entry(reg_window, font = ("Helvetica", 14), show = "*")
    confirm_password_entry.pack()

    tk.Label(reg_window, text = "Email:", font = ("Helvetica", 14)).pack(pady = 10)
    email_entry = tk.Entry(reg_window, font = ("Helvetica", 14))
    email_entry.pack()

    def register_user():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        confirm_password = confirm_password_entry.get().strip()
        email = email_entry.get().strip()
        if not username or not password or not confirm_password or not email:
            tk.messagebox.showerror("Error", "All fields are required.")
            return
        
        if "@" not in email or "." not in email:
            tk.messagebox.showerror("Error", "Invalid email format.")
            return
        
        if password != confirm_password:
            tk.messagebox.showerror("Error", "Passwords do not match.")
            return
        
        #Need to add code here to sav username and password to database


        tk.messagebox.showinfo("Success", "Registration successful!")
        reg_window.destroy()

    tk.Button(
        reg_window
        , text="Register"
        , font=("Helvetica", 14)
        , command=register_user
    ).pack(pady=20)

register_button = tk.Button(root, text="Register", font=("Helvetica", 14), command=open_registration)
register_button.pack(pady=10)






root.mainloop()




