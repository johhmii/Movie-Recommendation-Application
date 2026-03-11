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

#Switch Pages functions

def show_registration_page():

    search_page.pack_forget()
    registration_page.pack(fill = "both", expand = True)

def show_search_page():
    registration_page.pack_forget()
    search_page.pack(fill = "both", expand = True)


#Create frames forregistration pages
registration_page = tk.Frame(root, bg="#1e1e1e")

#Page Title
reg_title = tk.Label(
    registration_page,
    text="Create Your Account",
    font= ("Helvetica", 24, "bold"),
    bg="#1e1e1e",
    fg = "#cfcfcf",
    )
reg_title.pack(pady=(25, 10))

reg_subtitle = tk.Label(
    registration_page,
    text="Register Down Below",
    font = ("Helvetica", 12),
    bg = "#1e1e1e",
    fg = "#cfcfcf"
)
reg_subtitle.pack(pady=(0, 20))

#Container for registration form

form_frame = tk.Frame(registration_page, bg="#252525", padx = 25, pady = 25)
form_frame.pack(padx = 30, pady = 10)

#USername label
username_label = tk.Label(
    form_frame,
    text="Username:",
    font=("Helvetica", 12),
    bg="#252525",
    fg="white"
)
username_label.pack(anchor="w", pady=(5, 5))

#Username entry
username_entry = tk.Entry(
    form_frame,
    font=("Helvetica", 12),
    bg="#3a3a3a",
    fg="white",
    insertbackground="white",
    relief="flat"
)
username_entry.pack(fill = "x", ipady = 8)

#password label
password_label = tk.Label(
    form_frame,
    text="Password:",
    font=("Helvetica", 12),
    bg="#252525",
    fg="white"
)
password_label.pack(anchor="w", pady=(15, 5))

#password entry
password_entry = tk.Entry(
    form_frame,
    font=("Helvetica", 12),
    show = "*",
    bg="#3a3a3a",
    fg="white",
    insertbackground="white",
    relief="flat",
)
password_entry.pack(fill = "x", ipady = 8)

#confirm password label
confirm_password_label = tk.Label(
    form_frame,
    text="Confirm Password:",
    font=("Helvetica", 12),
    bg="#252525",
    fg="white"
)
confirm_password_label.pack(anchor="w", pady=(15, 5))

#confirm password entry
confirm_password_entry = tk.Entry(
    form_frame,
    font=("Helvetica", 12),
    show = "*",
    bg="#3a3a3a",
    fg="white",
    insertbackground="white",
    relief="flat",
)
confirm_password_entry.pack(fill = "x", ipady = 8)

#Email label
email_label = tk.Label(
    form_frame,
    text="Email:",
    font=("Helvetica", 12),
    bg="#252525",
    fg="white"
)
email_label.pack(anchor="w", pady=(15, 5))

#Email entry
email_entry = tk.Entry(
    form_frame,
    font=("Helvetica", 12),
    bg="#3a3a3a",
    fg="white",
    insertbackground="white",
    relief="flat",
)
email_entry.pack(fill = "x", ipady = 8)

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
    
    show_search_page()

#Search Page

search_page = tk.Frame(root, bg="#1e1e1e")

#search page title
search_title = tk.Label(
    search_page,
    text="Movie Recommendation App",
    font= ("Helvetica", 24, "bold"),
    bg="#1e1e1e",
    fg = "#cfcfcf",
    )
search_title.pack(pady=(20, 10))

search_subtitle = tk.Label(
    search_page,
    text="Search for your favorite movies",
    font = ("Helvetica", 12),
    bg = "#1e1e1e",
    fg = "#cfcfcf"
)
search_subtitle.pack(pady=(0, 20))

#seach frame
search_frame = tk.Frame(search_page, bg="#252525")
search_frame.pack(fill = "x", padx = 20, pady = 10)

#seach bar
search_bar = tk.Entry(
    search_page,
    font =  ("Helvetica", 18),
    bg= "#2b2b2b",
    fg = "white",
    insertbackground="white",
    relief = "flat"
)
search_bar.pack(side = "left", fill = "x", expand = True, ipady = 10)

#seach result label box
results_label = tk.Label(
    search_page,
    text="Search Results:",
    font = ("Helvetica", 14, "bold"),
    bg = "#1e1e1e",
    fg = "#cfcfcf"
)
results_label.pack(anchor = "w", padx = 20, pady = (15, 5))

#result listbox
search_results = tk.Listbox(
    search_page,
    font = ("Helvetica", 14),
    height= 12,
    bg = "#2b2b2b",
    fg = "white",
    selectbackground= "#4a09e2",
    selectforeground = "white",
    relief = "flat",
    highlightthickness= 0
)
search_results.pack(fill = tk.BOTH, expand = True, padx = 20, pady = (0,20))


#TEMP SAMPLE SEARCH FUNCTION
def sample_search():

    query = search_bar.get().strip()

    search_results.delete(0, tk.END)

    if not query:
        tk.messagebox.showerror("Error", "Please enter a title.")
        return

    #temp fake search results
    search_results.insert(tk.END, f"{query} (The Godfather)")
    search_results.insert(tk.END, f"{query} (The Dark Knight)")
    search_results.insert(tk.END, f"{query} (Pulp Fiction)")
    search_results.insert(tk.END, f"Reccomended Movies Similar to {query}")

search_button = tk.Button(
    search_frame,
    text="Search",
    font = ("Helvetica", 13, "bold"),
    bg = "#4a09e2",
    fg = "white",
    activebackground= "#357abd",
    activeforeground = "white",
    relief = "flat",
    command = sample_search
)
search_button.pack(side = "left", padx = (10, 0), ipady = 8)

#back button
back_button = tk.Button(
    search_frame,
    text="Back to Registration",
    font = ("Helvetica", 13, "bold"),
    bg = "#5a5a5a",
    fg = "white",
    activebackground= "#707070",
    activeforeground = "white",
    relief = "flat",
    command = show_registration_page
)
back_button.pack(pady = (0,20), ipadx = 10, ipady = 6)


search_page.pack(fill = "both", expand = True)


root.mainloop()




