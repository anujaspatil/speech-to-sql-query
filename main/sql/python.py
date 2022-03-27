def printed(msg3):
  msg3[1] = '("'+str(msg3[1])
  msg3[-1] = str(msg3[-1])+'")'
  str1 = " "
  return (str1.join(msg3))

def createfunction(msg3):
  nameposition = msg3.index("name")
  nameposition = nameposition + 1
  functionname = msg3[nameposition]
  return("def " +str(functionname) + '();')

def forloop(msg3):
  startposition = msg3.index("from")
  startposition = startposition + 1
  start = msg3[startposition]
  end = msg3[startposition + 2]
  return("for i in range(" + str(start) + "," + str(end) + "):")

def createwhile(msg3):
  return("while( ):")

def inivariable(msg3):
  if "name" in msg3:
    position = msg3.index("name")
    position = position + 1
    variablename = msg3[position]
    if msg3[position + 2].isnumeric():
      value = msg3[position+2]
      return(str(variablename) + "=" + str(value))
    else:
      value = msg3[position + 2]
      return(str(variablename) + "=" + '"'+str(value)+'"')
  else:
    position = msg3.index("variable")
    position = position + 1
    variablename = msg3[position]
    if msg3[position + 2].isnumeric():
      value = msg3[position+2]
      return(str(variablename) + "=" + str(value))
    else:
      value = msg3[position + 2]
      return(str(variablename) + "=" + '"'+str(value)+'"')

def finalans(msg3):
  msg3 = list(msg3.split(" "))
  ans= ""
  #print logic

  if msg3[0] == "print":
    ans = printed(msg3)

  #function logic

  elif "function" in msg3:
    ans = createfunction(msg3)

  #forloop

  elif "for" in msg3:
    if "loop" in msg3:
      ans = forloop(msg3)

  #whileloop

  elif "while" in msg3:
    ans = createwhile(msg3) 

  #initialize variable 

  elif "initialize" in msg3:
    if "variable" in msg3:
      ans = inivariable(msg3)

  return ans

