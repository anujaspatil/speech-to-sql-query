def printed(msg):
  msg[1] = '("'+str(msg[1])
  msg[-1] = str(msg[-1])+'")'
  str1 = " "
  return (str1.join(msg))

def createfunction(msg):
  nameposition = msg.index("name")
  nameposition = nameposition + 1
  functionname = msg[nameposition]
  return("def " +str(functionname) + '();')

def forloop(msg):
  startposition = msg.index("from")
  startposition = startposition + 1
  start = msg[startposition]
  end = msg[startposition + 2]
  return("for i in range(" + str(start) + "," + str(end) + "):")

def createwhile(msg):
  return("while( ):")

def inivariable(msg):
  if "name" in msg:
    position = msg.index("name")
    position = position + 1
    variablename = msg[position]
    if msg[position + 2].isnumeric():
      value = msg[position+2]
      return(str(variablename) + "=" + str(value))
    else:
      value = msg[position + 2]
      return(str(variablename) + "=" + '"'+str(value)+'"')
  else:
    position = msg.index("variable")
    position = position + 1
    variablename = msg[position]
    if msg[position + 2].isnumeric():
      value = msg[position+2]
      return(str(variablename) + "=" + str(value))
    else:
      value = msg[position + 2]
      return(str(variablename) + "=" + '"'+str(value)+'"')


msg = "initialize variable name country to india"
msg = list(msg.split(" "))

#print logic

if msg[0] == "print":
 ans = printed(msg)

#function logic

elif "function" in msg:
  ans = createfunction(msg)

#forloop

elif "for" in msg:
  if "loop" in msg:
    ans = forloop(msg)

#whileloop

elif "while" in msg:
  ans = createwhile(msg) 

#initialize variable 

elif "initialize" in msg:
  if "variable" in msg:
    ans = inivariable(msg)

print(ans)

