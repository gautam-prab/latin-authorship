f = open('word-list.txt', 'r')
txt = f.read()
f.close()
newtxt = ""
for c in txt:
    if (not str.isnumeric(c) and c is not ' ' and c is not '.'):
        newtxt = newtxt + c
f1 = open('words.txt', 'w')
f1.write(newtxt)
f1.close()
