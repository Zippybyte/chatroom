# Chatroom
#### Video Demo:  <URL HERE>
#### Description:
  
  I made a simple chatroom website. 
  Chatroom is a simple... well chatroom website.
  You can create rooms by just imputting a room name and people can connect to the room with the room name.
  
#### How to run
  
  It runs on flask-socketio so it is run via python.
  Run in the terminal `python -m app`

#### File Descriptions:
  ###### app.py
  The main application, it's made with python, flask, and flask-socketio.
  It has all of the server-side code and serves pages and handles the communication with socketio.
  
  ###### helpers.py
  Only has the function error which displays the error.html page when an error happens.
  
  ###### requirements.txt
  `requirements.txt` has all of the required packages so that the venv doesn't break whenever something updates.
  
  ###### .gitignore
  It stops git from including useless files like the .venv or pycache.
  
  ###### README.md
  Hey, that's me!
  
  
  ##### static
  - ###### styles.css
  Contains a tiny amount of css because I was mostly using bootstrap for most css problems.
  
  
  ##### templates
  - ###### lobby.html
  You can create a room by inputting a word, name, or just random words.
  People can then connect to that room by putting in that same name or connect via a link. 
  
  - ###### username.html
  Prompts you for your username/name and sends it to the server for validation. 
  If the username is invalid it will render `error.html` and list the error. Although it should only render `error.html` if the user messes with the code.
  It also checks if the name you're inputting is already in the room that you're connecting to and if so it will render `username_taken.html`. 
  But if it goes through then you will be able to join the room with your entered username. 
  Using `localStorage` it automatically will remember and enter your username.
  
  - ###### username_taken.html
  This only appears if the user trys to set their name as a name that is already in the room. It is mostly the same as `username.html` but it doesn't automatically enter your username. It's here because the client can't tell when it shouldn't use the name stored in `localStorage`.
  
  - ###### room.html
  The main chat page.
  You can send and recieve messages from the other people in the room. There is a user list and a way to change your name. There is a lot of javascript for recieving and sending messages via socketio as well as some for updating the userlist and the chatlog. One of the problems I realised early on is that I need to make sure that the message are safe from Cross site scripting so I couldn't use `Innerhtml` so I figured out that you could use nodes to make and insert elements and the text into the html.
  
  - ###### error.html
  A simple webpage just to display an error message and its error code.
  
  - ###### layout.html
  The flask layout page for everything, it contains the script links to socketio and bootstrap, and the stylesheets to `styles.css` and bootstrap.
 
#### Descisions Descisions...:  
  - Why use websocket?
  I was planning to make something with more realtime interaction and I looked into AJAX but that didn't seem good enough for something rea time. Although because of time constraints I had to scrap the idea.
  
  - 
  
  
#### Problems and what I wish I did
  I definitely had a lot of difficulty with this
  
  ###### How do you bring a 
  
  
  
  
  
  
  
  
