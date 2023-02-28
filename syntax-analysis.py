def fileAnalysis(file):
    """Function that begins the file Analysis"""
    def indentationCheck(line, sub):
        """Function to check the amount of indentation a line has, assuming the rest of the function has been corrected"""
        line = line.rstrip('    ') # removes tabs from end of line (just to protect against edge case "\t *line* \t")
        indents = line.count('    ')
        if indents == sub and not line.__contains__('print('):
            return line, sub + 1
        elif line.__contains__('print('): # Don't want to increase a sub-level from a print function 
            while indents < sub: # Add as many indents as needed to match the current sub-level
                line = '    ' + line
                indents += 1
            return line, sub
        else: 
            while indents < sub: 
                line = '    ' + line
                indents += 1
            return line, sub + 1
        
    opened = open(file, 'r', encoding = 'utf8') # opens the file for reading and writing
    out = open('Updated.txt', 'w') # open a new file for appending the gather data
    lines = opened.readlines()

    for line in lines: # function for re-writing the original file to the new file
        out.write(line)

    endlines = ['\n', '\n---End of original code, fixed follows---\n', '\n']
    out.writelines(endlines)
    opened.seek(0)
    line = opened.readline()
    sub = 0 # checks the sublevel of a function (whether def or if has been called yet and indentation is needed)
    printKeywords = 0 # holds the number of times the print function is called
    while not line == '':
        if sub == 0:
            if line.__contains__('def'):
                    if not line.__contains__('def '):
                        line = line[:line.find('def') + 3] + ' ' + line[line.find('def') + 3:]
                    if line.find('(') == -1: # this denotes the the first paraenthesis for the def function is missing
                        # since strings are immutatable have to make a new string with the missing piece and then overwrite that line of the file
                        line = line[:line.find('def') + 3] + '(' + line[line.find('def') + 3:]
                    if line.find(')') == -1:
                        line = line[:line.find(':')] + ')' + line[line.find(':'):]
                    if line.find(':') == -1:
                        line = line[:len(line) - 1] + ':\n'
                    sub += 1
                    out.write(line)
                    line = opened.readline()
            elif line.__contains__('if '):
                if line.__contains__(':'):
                    sub +=1
                    out.write(line)
                    line = opened.readline()
                else:
                    line = line + ':'
                    out.write(line)
                    line = opened.readline()
            elif line.__contains__('while '):
                if line.__contains__(':'):
                    sub += 1
                    out.write(line) # write line to out file
                    line = opened.readline() # Reading next line for next check
                else:
                    line = line + ':' # EX: "while <condition> " we add in the missing ":"
                    sub += 1
                    out.write(line) # write line to out file
                    line = opened.readline() # Reading next line for next check
            elif line.__contains__('for ') and not line.__contains__('#'):
                if line.__contains__(':') and line.__contains__(' in '):
                    sub += 1
                    out.write(line) # write line to out file
                    line = opened.readline() # Reading next line for next check
                elif line.find(':') == -1 and line.find(' in ') != -1:
                    line = line + ":"
                    sub += 1
                    out.write(line) # write line to out file
                    line = opened.readline() # Reading next line for next check
                elif line.find(':') != -1 and line.find(' in ') == -1:
                    first_space = line.find(' ')
                    second_space = line.find(' ', first_space) # index of second space
                    line = line[:second_space] + 'in ' + line[second_space:] # add in the in key word and a space
                    sub += 1
                    out.write(line) # write line to out file
                    line = opened.readline() # Reading next line for next check
                else:
                    first_space = line.find(' ')
                    second_space = line.find(' ', first_space) # index of second space
                    line = line[:second_space] + 'in ' + line[second_space:] # add in the in key word and a space
                    line = line + ":" #add to the end of the line
                    sub += 1
                    out.write(line) # write line to out file
                    line = opened.readline() # Reading next line for next check
            elif line == '\n' or line.__contains__('#the'):
                sub = 0
                out.write(line)
                line = opened.readline()
            else:
                out.write(line)
                printKeywords += line.count('print(') # Checking for the first paraenthesis since only function calls are wanted, not the actual word
                line = opened.readline()
        else:
            if line.__contains__('def '):
                if line.find('(') == -1: 
                    line = line[:line.find('def') + 3] + '(' + line[line.find('def') + 3:]
                if line.find(')') == -1:
                    line = line[:line.find(':')] + ')' + line[line.find(':'):]
                if line.find(':') == -1:
                    line = line + ':'
                line, sub = indentationCheck(line, sub)
                out.write(line)
                line = opened.readline()
            elif line.__contains__('if '):
                if line.__contains__(':'):
                    line, sub = indentationCheck(line, sub)
                    out.write(line)
                    line = opened.readline()
                else:
                    line = line + ':'
                    line, sub = indentationCheck(line, sub)
                    out.write(line)
                    line = opened.readline()
            elif line.__contains__('while '):
                if line.__contains__(':'):
                    line, sub = indentationCheck(line, sub) # call function to add correct  # indents
                    out.write(line)
                    line = opened.readline()
                else:
                    line = line + ':'
                    line, sub = indentationCheck(line, sub)
                    out.write(line) # write line to out file
                    line = opened.readline() # Reading next line for next check
            elif line.__contains__('for ') and not line.__contains__('#'):
                if line.__contains__(':') and line.__contains__(' in '):
                    line, sub = indentationCheck(line, sub) # call function to add correct  # indents
                    out.write(line)
                    line = opened.readline()
                elif line.find(':') == -1 and line.find(' in ') != -1:
                    line = line + ":"
                    line, sub = indentationCheck(line, sub)
                    out.write(line)
                    line = opened.readline()
                elif line.find(':') != -1 and line.find(' in ') == -1:
                    first_space = line.find(' ')
                    second_space = line.find(' ', first_space)
                    line = line[:second_space] + 'in ' + line[second_space:]
                    line, sub = indentationCheck(line, sub)
                    out.write(line)
                    line = opened.readline()
                else:
                    first_space = line.find(' ')
                    second_space = line.find(' ', first_space)
                    line = line[:second_space] + 'in ' + line[second_space:]
                    line = line + ":"
                    line, sub = indentationCheck(line, sub)
                    out.write(line)
                    line = opened.readline()
            elif line == '\n':
                sub = 0
                out.write(line)
                line = opened.readline()
            else:
                line, sub = indentationCheck(line, sub)
                printKeywords += line.count('print(')
                out.write(line)
                line = opened.readline()
    out.write('\n\n')
    out.write('Count for print keywords: ' + str(printKeywords))
    opened.close()
    out.close()


def main():
    """Main function to be run when in standalone"""
    fileName = input('Please input the name of the file\n')
    fileAnalysis(fileName)
    print('Analysis has finished!')


if __name__ == '__main__':
    main()
