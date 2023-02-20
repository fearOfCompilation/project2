

def fileAnalysis(file):
    """Function that begins the file Analysis"""
    opened = open(file, 'r+') # opens the file for reading and writing
    line = opened.readline()
    sub = 0 # checks the sublevel of a function (whether def or if has been called yet and indentation is needed)
    printKeywords = 0 # holds the number of times the print function is called
    while line is not None:
        if sub == 0:
            if line.__contains__('def'):
                    if line.__contains__('(') and line.__contains__(')') and line.__contains__(':'):
                        sub +=1
                        line = opened.readline()
                    elif line.find('(') == -1: # this denotes the the first paraenthesis for the def function is missing
                        # since strings are immutatable have to make a new string with the missing piece and then overwrite that line of the file
                        line = line[:line.find('def') + 3] + '(' + line[line.find('def') + 3:]
                        opened.write(line)
                        opened.truncate()
                        opened.readline()
                    elif line.find(')') == -1:
                        line = line[:line.find(':')] + ')' + line[line.find(':'):]
                        opened.write(line)
                        opened.truncate()
                        opened.readline()
                    else:
                        line = line + ':'
                        opened.write(line)
                        opened.truncate()
                        opened.readline()
            elif line.__contains__('if'):
                if line.__contains__(':'):
                    sub +=1
                    line = opened.readline()
                else:
                    line = line + ':'
                    opened.write(line)
                    opened.truncate()
                    opened.readline()
            else:
                printKeywords += line.count('print(') # Checking for the first paraenthesis since only function calls are wanted, not the actual word
                line = opened.readline()




def main():
    """Main function to be run when in standalone"""
    fileName = input('Please input the name of the file')
    fileAnalysis(fileName)