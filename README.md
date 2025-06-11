CS Quiz Master

Overview:

CS Quiz Master is a web application designed to help users improve their computer science knowledge through quizzes, games, and achievements. The app features categories like Networking, Security, Development, System Engineering, and Databases, with different levels of difficulty. Users can compete on a leaderboard, unlock achievements, and even play a Hangman game with CS terms.

---

Why These Technologies Were Chosen:

Backend:
- Python Flask: Flask is what we were supposed to use for backend, and it runs very smoothly with Vue.js.
- SQLite: Chosen for its simplicity and ease of setup, SQLite is perfect for small-scale applications like this one.


Frontend:
- Vue.js: Vue is a progressive JavaScript framework that simplifies building dynamic and interactive user interfaces. Its component-based architecture makes it easy to manage and scale the application.
- Bootstrap: Made styling very easy to implement and easy to configure within the different files
- JavaScript: Essential for client-side interactivity.

Other Tools
- Node.js: Used for managing dependencies and running the Vue development server.
- CORS: Enables secure communication between the frontend and backend during development.


---

 How to Run the App:

Prerequisites:

1. Install [Python](https://www.python.org/downloads/) (version 3.8 or higher).
2. Install [Node.js](https://nodejs.org/) (version 14 or higher).
3. Install [SQLite](https://www.sqlite.org/download.html) (optional, included with Python).

 Backend Setup
1. Navigate to the `cs-quiz-master/backend` directory.
2. Install dependencies:
    ```bash
    pip install flask flask-cors werkzeug
    ```
3. Initialize the database:
    ```bash
    python _db_.py
    ```
4. Start the Flask server:
    ```bash
    python app.py
    ```
    The backend will run on `http://localhost:5001`.

Frontend Setup : 
1. Navigate to the `cs-quiz-master/frontend` directory.
2. Install dependencies:
    ```bash
    npm install
    ```
3. Start the development server:
    ```bash
    npm run serve
    ```
    The frontend will run on `http://localhost:8080`.

---

How to Use the App:

Sign Up : 
1. Navigate to `http://localhost:8080`.
2. Click "Sign Up" and fill in your details.
3. After signing up, you will be automatically logged in.

Login : 
1. If you already have an account, click "Login" on the homepage.
2. Enter your username and password.

Play Quizzes :
1. Click "Play" in the navigation bar.
2. Select a category and level, or leave them blank for random questions.
3. Answer questions to earn points and climb the leaderboard.

View Leaderboard :
1. Click "Leaderboard" in the navigation bar.
2. See the top players and their scores.

Play Hangman : 
1. Click "Hangman" in the navigation bar.
2. Guess CS terms before running out of tries.

Profile : 
1. Click "Profile" in the navigation bar.
2. View your achievements, upload a profile picture, and check your score.



Admin Features : 
Admins can:
- Add, edit, and delete quiz questions.
- Manage categories and levels.

To access the admin panel, log in with an admin account and click "Admin" in the navigation bar.

There is a seeded admin account with the login :
username : quiz_master
password : test123

Parts of this projects Hangman game, including images and code logic, are based on resources from CodingNepal. Full credit goes to the original creator for their work and tutorial.




