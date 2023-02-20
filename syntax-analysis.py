

def fileAnalysis(file):
    """Function that begins the file Analysis"""
    opened = open(file, 'r+')
    line = opened.readline()
    sub = 0
    printKeywords = 0
    while line is not None:
        if sub == 0:
            if line.__contains__('def'):
                    if line.__contains__('(') and line.__contains__(')') and line.__contains__(':'):
                        sub +=1
                        line = opened.readline()
                    elif line.find('(') == -1:
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
                printKeywords += line.count('print(')
                line = opened.readline()




def main():
    """Main function to be run when in standalone"""
    fileName = input('Please input the name of the file')
    fileAnalysis(fileName)