# myLibrary 📚 
A network application that keep track of books for each account.

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## **General info** 
Network desktop application that keep track of books for each account. 
At first the user have to register with username and a password, after the user login, he can look for new books to  add. Each user have two tables:
"wishlist" - books that the user will want to read.
"booksRead" - books that the user already read.

Every-time the user search for book, the server will activate a bot to find the book from https://simania.co.il/ .
The project optimize for Hebrew books especially.
English books support will come soon.

***The project only work in Linux and Macos,
Currently the project have no support for Windows os.***

## **Technologies** 
The project created with:
* python 3.9
* kivy
* sqlite
* selenium 

## **Setup**
***Make sure you have python in your computer.***


In the project  directory run:
```python
$ virtualenv .env && source .env/bin/activate && pip install -r requirements.txt
```
Navigate to the Server folder and run:
```python
$ python Server.py
```

Navigate to the Client folder and Run the desktop application:
```python
$ python kivyapp.py 127.0.0.1
```

#### Keep in mind:
The IP address should point to the IP address of the server, If you run the Server in your local computer run the above IP, If you run the server in another computer find the ip for the server and replace 127.0.0.1 with the correct IP.
