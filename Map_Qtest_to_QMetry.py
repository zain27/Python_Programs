import pandas as pd
import os
from openpyxl import load_workbook

for file in os.listdir("input files dir"):
    fname = os.path.join("input files dir", file)
    print("Working on file "+file)
    
    df = pd.read_excel(fname,1,converters={'Name':str})    
    tempIds = df['Id'].dropna()
    tempName = df['Name'].dropna()
    tempDesc = df['Description'].dropna()
    tempPre = df['Precondition'].dropna()
    tempStepsDesc = df['Test Step Description'].dropna()
    tempStepExpectedResults = df['Test Step Expected Result'].dropna()

    linenum=[]
    ids = []
    names=[]
    steps=[]
    desc=[]
    precond= []
    stepsDesc =[]
    stepExpectedResults=[]


    numTestSteps = dict()
    namesDict = dict()
    descDict = dict()
    precondDict = dict()


    #converting id to a list
    for k,v in tempIds.items() :
        linenum.append(k)
        ids.append(v)

    #converting Name to a list
    for k,v in tempName.items():
        names.append(v)

    for k,v in tempDesc.items():
        desc.append(v)

    for k,v in tempPre.items():
        precond.append(v)

    for k,v in tempStepsDesc.items():
        stepsDesc.append(v)
    #print(stepsDesc)

    for k,v in tempStepExpectedResults.items():
        stepExpectedResults.append(v)

    #calculating the number of steps in each test case.
    for i in range(len(linenum)):
        if i+1 != len(linenum):
            steps.append(linenum[i+1]-linenum[i])
        else:
            steps.append(linenum[i]-linenum[i-1])

    #making the dictionaries mapped by the ids. 
    for i in range(len(ids)):
        numTestSteps[ids[i]] = steps[i]
        namesDict[ids[i]] = names[i]
        descDict[ids[i]] = desc[i]
        precondDict[ids[i]] = precond[i]

    print("Getting old values ... ")
    
    lower = 0
    upper = 0
    issueKey =0
    output = ""
    df2 = pd.DataFrame()
    
    print("Mapping values to new file ... ")
    
    for i in range(len(ids)):        
        issueKey += 1
        output += "[{issue key : " + str(issueKey) +" , "
        output += "issue type : " + "Test Case" +" , "
        output += "summary : " + namesDict[ids[i]] +" , "
        output += "description : "+ descDict[ids[i]] +" , "
        output += "expected result : "+ "none" +" , "
        output += "precondition : "+precondDict[ids[i]] + "},"        
        
        df2 = df2.append(pd.DataFrame({'Issue Key':issueKey,'Issue Type':"Test Case",'Summary':namesDict[ids[i]],'Description':descDict[ids[i]]+"\n"+precondDict[ids[i]],'Priority':"", 'Versions':"2.0", 'Components':"Account Information", 'Labels':"",	'Test Data':"",'Expected Result':"",'Platform':"", 'Automation Id 1':"", 'Automation Id 2' :"",'SubLevel' :"",'Attachment':"",'Task Type':"QA KB",'Affects Version/s':"2.0"},index=[issueKey]))
        df2 = df2[['Issue Key','Issue Type','Summary','Description','Priority','Versions','Components','Labels','Test Data','Expected Result','Platform','Automation Id 1','Automation Id 2','SubLevel','Attachment','Task Type','Affects Version/s']]
        writer = pd.ExcelWriter(os.path.join('output_path',"QM_"+file), engine='xlsxwriter')        
        df2.to_excel(writer, sheet_name='TEST AUTHORING',index=False)    
        
        lower = upper
        upper += numTestSteps[ids[i]]        
        j= lower
        while j < upper:
            #print (stepsDesc[j],stepExpectedResults[j])
            issueKey += 1
            output += "{issue key : " + str(issueKey) +" , "
            output += "issue type : " + "Test Step" +" , "
            output += "summary : " +stepsDesc[j] +" , "
            output += "description : "+ "none" +" , "
            output += "expected result : "+ stepExpectedResults[j] +" , "
            output += "precondition : "+"none" +" }, "        
            
            df2 = df2.append(pd.DataFrame({'Issue Key':issueKey,'Issue Type':"Test Step",'Summary':stepsDesc[j],'Description':"",'Priority':"", 'Versions':"", 'Components':"", 'Labels':"",'Test Data':"",'Expected Result':stepExpectedResults[j],'Platform':"", 'Automation Id 1':"", 'Automation Id 2' :"",'SubLevel' :"",'Attachment':"",'Task Type':"",'Affects Version/s':""},index=[issueKey]))
            df2 = df2[['Issue Key','Issue Type','Summary','Description','Priority','Versions','Components','Labels','Test Data','Expected Result','Platform','Automation Id 1','Automation Id 2','SubLevel','Attachment','Task Type','Affects Version/s']]
            writer = pd.ExcelWriter(os.path.join('output_path',"QM_"+file), engine='xlsxwriter')
            df2.to_excel(writer, sheet_name='TEST AUTHORING',index=False)
            j += 1
        output+= "]"  
        #print(output)
        output=""    
        writer.save()

    df3 = pd.DataFrame({'Test Run Key':"",'Story Key':"",'Test Scenario Key':"",'Test Case Key':"",'Test Step Id':"",'Result Status':"",'Comment':"",'Duration':"",'Error Name':"",'Message':"",'Stacktrace':"",'Error Metadata':"",'Error Message':"",'Actual Result':"",'Defect Key':""},index=[0])     
    df3 = df3[['Test Run Key','Story Key','Test Scenario Key','Test Case Key','Test Step Id','Result Status','Comment','Duration','Error Name','Message','Stacktrace','Error Metadata','Error Message','Actual Result','Defect Key']]

    df4 = pd.DataFrame({'Status':"Working",'Background Color':"#12A3A8",'Text Color':"#FFFFFF"},index=[0])
    df4=df4.append(pd.DataFrame({'Status':"Not Important",'Background Color':"#12A3A8",'Text Color':"#FFFFFF"},index=[0]))
    df4=df4.append(pd.DataFrame({'Status':"Pending",'Background Color':"#12A3A8",'Text Color':"#FFFFFF"},index=[0]))
    df4=df4[['Status','Background Color','Text Color']]

    book = load_workbook(os.path.join('output_path',"QM_"+file))
    with pd.ExcelWriter(os.path.join('output_path',"QM_"+file),engine='openpyxl') as writer:
        writer.book = book
        writer.sheets = dict((ws.title,ws) for ws in book.worksheets)
        df3.to_excel(writer,'TEST EXECUTION',index=False)
        df4.to_excel(writer,'STATUS MAPPING',index=False)
        writer.save()
    print("File mapping successful for "+ file)
    print ("\n=================================================\n")    
