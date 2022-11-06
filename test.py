import os


a='send'

if os.access(a, os.R_OK):
  print('yess')
else:
  print("noooo")