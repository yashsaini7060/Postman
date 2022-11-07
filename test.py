import os

x='60000\n'
if x.endswith("\n"):
  print('yo')
  print(x)
  x=x[:-1]
  server_port=int(x)