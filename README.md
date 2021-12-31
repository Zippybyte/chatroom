# Chatroom
#### Video Demo:  https://youtu.be/v6q_u79D94E
#### Description:
  
  I made a simple chatroom website. 
  Chatroom is a simple... well chatroom website.
  _I'm not creative with names._
  You can create rooms by just imputting a room name and people can connect to the room with that same room name.
  
#### How to run
  
  It runs on flask-socketio so it is run via python. Install the dependencies in `requirements.txt` first.
  Run in the terminal `python -m app`

#### File Descriptions:
  - ##### app.py
  The main application, it's made with python, flask, and flask-socketio.
  It has almost all of the server-side code and serves pages and handles the communication with socketio.
  
  - ##### helpers.py
  Has the function `error` which renders a page for errors. I had planned to use this for more but most of the code ended up being simple enough to not need it.
  
  - ##### requirements.txt
  `requirements.txt` has all of the required packages for the venv so that stuff doesn't update so they can't break.
  
  - ##### .gitignore
  It stops git from including useless files like the .venv or pycache.
  
  - ##### README.md
  _Hey, that's me!_
  
  
  #### static
  - ##### styles.css
  Contains a tiny amount of css because I was mostly using bootstrap for most css problems.
  
  
  #### templates
  - ##### lobby.html
  It contains some text about what to do and
  you can create a room by inputting a word, name, or just random characters.
  People can then connect to that room by putting in that same name or by using the same url.
  
  - ##### username.html
  Prompts you for your username/name and sends it to the server for validation. 
  If the username is invalid it will render `error.html` and list the error. Although it should only render `error.html` if the user messes with the code.
  It also checks if the name you're inputting is already in the room that you're connecting to and if it is it will render `username_taken.html`. 
  But if it goes through then you will be able to join the room with your entered username.
  Also using `localStorage` it will automatically remember and enter your username.
  
  - ##### username_taken.html
  This only appears if the user trys to set their name as a name that is already in the room. It is mostly the same as `username.html` but it doesn't automatically enter your username. It's here because the client can't tell when it shouldn't use the name stored in `localStorage`, _and because it's the easiest solution._
  
  - ##### room.html
  The main chat page.
  You can send and recieve messages from the other people in the room. There is a user list and a way to change your name. There is a lot of javascript for recieving and sending messages via socketio as well as some for updating the userlist and the chatlog.
  
  - ##### error.html
  A simple webpage just to display an error message and its error code.
  
  - ##### layout.html
  The flask layout page for everything, it contains the script links to socketio and bootstrap, and the stylesheets to `styles.css` and bootstrap.
 
#### Descisions Descisions...
  - Why a browser based chatroom?
  I was planning to create an online game for the card game speed but because of time constraints I ended up doing this. I do feel it's a bit cheap to do this but I kind of just want to finish the project before 2022.
  
  - Why use websocket?
  I was planning to have more realtime interaction and I looked into AJAX but that didn't seem good enough for something realtime.
  
  - Why did you decide not to allow duplicate user names?
  I decided not to allow duplicate users in the same room because I would have to code around the duplicates and having to implement something probably an id system to know who is who.
 
#### Stuff I'd change if I did this again
  I definitely should have spent more time on this and I didn't have the time constraint. I didn't do almost any alt or aria attributes on my html which is something I probably should have done but didn't have time to do. Also probably shouldn't store a global variable in `app.py` but I'm not sure if there is a better way to do that other than _maybe_ a database
