def main():
    with open("input file path") as f: # opening the main file 
        content = f.readlines() 
    content = [x.strip() for x in content] # remove whitespace characters at the end of each line
    
    i=0  # loop variable and file name variable 
    splitter=0; # takes care of splitting every 2000 iterations, since each command is 2 line long and we need 1000 commands change splitter to the number of lines you need to run 
    sub=[] # sub list to store the split text

    while i  < len(content):        
        if splitter != 1000:    
            
            sub.append(content[i])  # append each line to list sub till count of splitter reaches 2000
            i+=1
            splitter+=1
        else:    # when count of splitter reaches above 2000 write the contents of sub to file and reset values of sub and splitter for next batch
            createWrite(sub,i)            
            sub=[]
            splitter=0
    createWrite(sub,i) # to write remaining content in sub when it is below 2000 rows. 

            
# function to create and write contents of list to a file.             
def createWrite(sub,i):
    filename="output file path"+str(i/2)+".sql"    
    output=open(filename,"w")
    for line in sub:    # writing each line in sub to the file.
        output.write(line+"\n") 
    output.close()


main()
print("finished ... ")
