#code to add string 'GO' at end of each line. 

def main():
    string_to_add = 'GO'  # string to add between each line 
    inputFile ="put input file here"
    outputFile = inputFile[:-4]+"_modified"+inputFile[-4:]   # vnaming output file as inputfilename_modified.ext
    
    with open(inputFile) as f: # opening the input file 
        content = f.readlines()         
    content = ['\n'.join([x.strip(),string_to_add]) for x in content ] # remove whitespace characters at the end of each line and add the string to add while reading.
    
    output = open(outputFile, 'w')  # open output file.
    for item in content:
        output.write("%s\n" % item) # write to output file.   

main()
print("finished ... ")
