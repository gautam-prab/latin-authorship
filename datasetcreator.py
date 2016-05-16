outfile = input("Dataset Filename: ")
outf = open(outfile, "w")
while (True):
    infile = input("Filename: ")
    if (infile is None or infile is ""):
        print("Thanks! Exiting")
        outf.close()
        break
    inf = open(infile+".lat", "r")
    count = 1
    classification = input("Class: ")
    outline = str(classification)+" "
    for line in inf.readlines():
        line = line[:-1]
        outline = outline + str(count) + ":" + line + " "
        count = count + 1
    print(outline, file=outf)
