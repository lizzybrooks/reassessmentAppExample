#!/usr/bin/env python
# the above line needs to be in any script that will run in your web app
import cgi
import os
import sys   #cgi allows your python scripts to run on the server. os and sys contain tools to deal with filenames, paths and directories
import json
from random import shuffle

def shuffle_word(word):
   word = list(word)
   shuffle(word)
   return ''.join(word)

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
   name = extractRequestParameter("name")
   response = {}
   response["success"] = type(name) == str
   if response["success"]:
       response["name"] = str(name)
       response["scrambled"] = shuffle_word(str(name))

   newWord = json.dumps(response)
   print("Content-Length: " + str(len(newWord)))
   print("Content-Type: application/json")
   print()
   print(newWord)

handleRequest()

#  Make sure to get rid of the unnecessary things in the above lines of code!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


import base64
import mimetypes
import os
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from googleapiclient import errors


def create_message_with_attachment(
    sender, to, subject, message_text, file):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file: The path to the file to be attached.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEMultipart()
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  msg = MIMEText(message_text)
  message.attach(msg)

  content_type, encoding = mimetypes.guess_type(file)

  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'
  main_type, sub_type = content_type.split('/', 1)
  if main_type == 'text':
    fp = open(file, 'rb')
    msg = MIMEText(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'image':
    fp = open(file, 'rb')
    msg = MIMEImage(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'audio':
    fp = open(file, 'rb')
    msg = MIMEAudio(fp.read(), _subtype=sub_type)
    fp.close()
  else:
    fp = open(file, 'rb')
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(fp.read())
    fp.close()
  filename = os.path.basename(file)
  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  message.attach(msg)

  return {'raw': str(base64.urlsafe_b64encode(message.as_bytes()), 'utf-8')}

def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Message Id: %s' % message['id'])
    return message
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']

def main():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = None
  # The file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
      creds = pickle.load(token)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
      pickle.dump(creds, token)

  service = build('gmail', 'v1', credentials=creds)

  message = create_message_with_attachment('jeffreymartinez1225@gmail.com', 'jeffreymartinez1225@gmail.com',
                                           'Reassessment',
                                           'Hello, world! This is an email sent by Python.',
                                           'owl.png')
  send_message(service, 'me', message)

if __name__ == '__main__':
  print(os.getcwd())
  main()
