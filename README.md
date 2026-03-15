
# Movie Recommendation App

Group 7's submission for Computer Science 362 , Section ?

# Team 7's Information

* Name: David Ulloa
* Email: davidulloamontesinos@csu.fullerton.edu
* Name: Johnny Rivera
* Email: johnnyr.97@csu.fullerton.edu
* Name: Andy Vu
* Email: andyvu3@csu.fullerton.edu
* Name: Marco Guirguis
* Email: mguirguis535@csu.fullerton.edu
* Name: Eric Luu
* Email: eluu03@csu.fullerton.edu

---

# Before you Run

1.) Make sure you have Python 3.14 installed on your device from https://www.python.org/downloads/   
2.) Once you have python installed on your console, download the following packages in your terminal.
```console
py -m pip install requests pillow sv-ttk
```
3.) Download the repository from github and place it in a destination of your choosing.


# How to Run

1.) Put both repository in same folder in location of your choosing.  
2.) Cd into that file from terminal.  
3.) Run python main.py.  

Example: Repository is located in file movie_app in path /Documents/movie_app
```console
cd Documents/movie_app
python3 main.py
```

---
# How to Use the Program

## 1. Create an Account

When the application starts, you will see the **Login Page**.

If you do not already have an account:

1. Click **Create Account**
2. Enter the following information:
   - Username
   - Email
   - Password
   - Confirm Password
3. Click **Register**

Your account information will be stored locally in the SQLite database (`users.db`).

After registering successfully, you will be automatically logged in and taken to the movie search page.

---

## 2. Log In

If you already have an account:

1. Enter your username
2. Enter your password
3. Click **Login**

If the credentials match a user in the database, you will be logged in and redirected to the movie search page.


## 3. Search for Movies

Use the search bar to look up movies.

As you type, the application automatically queries the **TMDB API** and displays matching results.

Each result appears in the following format:


Search results update dynamically as you type.


## 4. View Movie Details

To see more information about a movie:

1. Double-click a movie from the search results list.

A new window will open displaying:

- Movie poster
- Title
- Release date
- Rating
- Runtime
- Genres
- Synopsis
- Top cast members


## 5. Add Movies to Favorites

To save a movie to your favorites list:

1. Click a movie in the search results.
2. Press the **Add to Favorites** button.

The selected movie will be added to your personal favorites list.

If the movie is already saved, the application will display an error message.


## 6. View Your Favorites

Your saved movies will appear in the **Favorites** section below the search results.

Favorites are tied to your user account and stored in the local database.

When you log in again, your favorites will automatically load.


## 7. Log Out

Click the **Logout** button to return to the login screen.

Logging out will:
- Clear the current user session
- Return the application to the login page

Your saved favorites will remain stored in the database for future sessions.


## Database Storage

The application automatically creates a local SQLite database file:
