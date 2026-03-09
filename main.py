#Movie Recommendation App
#Contributors:
#Marco Guirguis
#Eric Luu
#Johnny Rivera
#David Ulloa
#Andy Vu

import tkinter as tk
KEY = "8b3549b6ca7e044a906dea4d61a34125"

#Creates main window
root = tk.Tk()
#Sets the title of the window (Need name for app)
root.title("Movie Recommendation App")
root.geometry("600x400")

# Create search bar
search_bar = tk.Entry(root, font=("Helvetica", 20), width = 28)
search_bar.pack(pady=20, padx=20)

searchResults = tk.Listbox(root, font=("Helvetica", 20), height = 20)
searchResults.pack(fill=tk.BOTH, expand = True, padx = 20, pady = 20)



root.mainloop()




