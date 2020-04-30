#!/usr/bin/env python
# the above line needs to be in any script that will run in your web app
import cgi, os, sys   #cgi allows your python scripts to run on the server. os and sys contain tools to deal with filenames, paths and directories
import json

from fpdf import FPDF
pdf = FPDF()


def makePDF(goal):
    # goal = int(input("What is your learning goal? "))
    # print("you chose learning goal " + str(goal))

    imagelist = ["images/octopus.png", "images/owl.png", "images/cat.png", "images/dog.png"]

    pdf.add_page()
    pdf.image(imagelist[goal],10,10) #you can add two more parameters here for width and height, but they mess up the aspect ratio
    pdf.output("yourfile.pdf", "F")


def extractRequestParameter(param):
   """
   Returns the value attached to the key within the query string
   of the request URL.  If, for instance, the query string is
   a=123&b=hello, then extractRequestParam("a") would return "123",
   extractRequestParam("b") would return "hello", and extractRequestParam("c")
   would return None
   """
   params = cgi.FieldStorage()
   if param not in params: return None
   return params[param].value

def handleRequest():
   """
   This function extracts the content of the "name" keyword,
   creates a dictionary called response, then populates that dictionary with "success" if the name parameter is a string,
   It rewrites the name
   Then it runs the shuffle_word function on name!
   It converts this whole dictionary to a json file and prints it as newWord.
   """
   learning = extractRequestParameter("learning")
   response = {}
   response["success"] = type(learning) == str
   if response["success"]:
       response["learning"] = int(learning)
       response["goal"] = makePDF(int(learning))

   newWord = json.dumps(response)
   print("Content-Length: " + str(len(newWord)))
   print("Content-Type: application/json")
   print()
   print(newWord)

handleRequest()
