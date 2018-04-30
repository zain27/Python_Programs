from jira.client import JIRA
from zenpy import Zenpy
from pprint import pprint
import logging
import json
import requests



#connects to JIRA - do not edit. 
def connect_jira(log, jira_server, jira_user, jira_password):
    '''
    Connect to JIRA. Return None on error
    '''
    try:
        log.info("Connecting to JIRA: %s" % jira_server)
        jira_options = {'server': jira_server}
        jira = JIRA(options=jira_options, basic_auth=(jira_user, jira_password))
                                        # ^--- Note the tuple
        print("Connection Successful")
        return jira
    except Exception as e:
        log.error("Failed to connect to JIRA: %s" % e)
        return None

# method to handle doing the same thing for different views. 
def custom_printer(view,url,zdDict):
    user = 'user_name'
    pwd = 'password'
    #print('############### '+ view +' #################')
    r = requests.get(url, auth=(user, pwd))
    resp = r.json()
    for ticket in resp['tickets']:        
        raw_severity = ticket['custom_fields'][1]['value']
        severity = raw_severity[raw_severity.rfind('_')+1:]
        if severity == 'normal' :
            severity = 'medium'
        #print(str(ticket['id'])+","+ticket['raw_subject']+","+severity)            
        #zdDict[str(ticket['id'])] = str(ticket['id'])+","+str(ticket['raw_subject']).replace(',','')+","+severity
        zdDict[str(ticket['id'])] = severity

def main():
    print("Starting ... ")
    ############################ JIRA stuff ############################
    log = logging.getLogger(__name__)
    # create a connection object, jc
    jc = connect_jira(log, "https://your_domain.atlassian.net", "user_name", "password")
    # get all tickets from prod support board.
    issues_in_proj = jc.search_issues('your JQL query',maxResults=50000)
    
    jiraDict = dict() # will store all the issue details with zendesk ticket as the key. 
    jiraSeverityDict = dict() # will store zd ticket number and, severity as key value. 
    jiraTicketDict = dict()    # will store zd ticket and jira as key value. 
    for issue in issues_in_proj:        
        jiraId = "No Id" # default values
        jiraSeverity = "No Severity"
        zdId = "No Zendesk"   
        if issue.key is not None :
            jiraId = issue.key
        if hasattr(issue.fields, 'customfield_10102') :  # if ticket has the severity parameter. 
            jiraSeverity = issue.fields.customfield_10102.value
        if issue.fields.customfield_12203 is not None :# if ticket has the zendesk parameter.
            zdId = issue.fields.customfield_12203
            if ',' in zdId: # if jira is linked to multiple Zendesk tickets. 
                multipleZd = str(issue.fields.customfield_12203).split(',')
                for id in multipleZd:
                    jiraTicketDict[id] = jiraId
                    jiraSeverityDict[id] = jiraSeverity.lower()
            else :
                jiraTicketDict[zdId]=jiraId
                jiraSeverityDict[zdId] = jiraSeverity.lower()

        jiraDict[zdId] = jiraId+","+jiraSeverity+","+zdId      # master dictionary. 
        
    
    #for key,value in jiraDict.items():
    #    print(key+" <==========> "+value)    
    #for key,value in jiraTicketDict.items():
    #    print(key+" <======> "+ value+" <======> "+ jiraSeverityDict[key])
    
    ############################ Zendesk stuff ############################
    
    url_claims = 'https://your_domain.zendesk.com/api/v2/views/49660086/tickets.json?sort_by=subject' 
    url_underwriting = 'https://your_domain.zendesk.com/api/v2/views/54412163/tickets.json?sort_by=subject'  
    url_accounting = 'https://your_domain.zendesk.com/api/v2/views/55575483/tickets.json?sort_by=subject'
    url_billing = 'https://your_domain.zendesk.com/api/v2/views/48901943/tickets.json?sort_by=subject'

    zdDict = dict() # will store all the issues from Zendesk with zd ticket number as key. 

    custom_printer("Claims",url_claims,zdDict)
    custom_printer("Underwriting",url_underwriting,zdDict)
    custom_printer("Accounting",url_accounting,zdDict)
    custom_printer("Billing",url_billing,zdDict)

    #for key,value in zdDict.items():
    #    print(key+" <==========> "+value)
    #print(len(zdDict))
    
    mismatchDict = dict();

    for key,value in zdDict.items():
        if key in jiraTicketDict:
            if str(zdDict[key]).lower() != str(jiraSeverityDict[key]).lower() : # printing only the mismatched severity.
                print(key+","+zdDict[key] +"," + jiraTicketDict[key] +","+ jiraSeverityDict[key]) #prints the needed values.
                mismatchDict[jiraTicketDict[key]] = zdDict[key] # storing the correct values in mismatch dict. 
            #print(key+","+zdDict[key] +"," + jiraTicketDict[key] +","+ jiraSeverityDict[key])            
    
    
    # once all the mismatches are identified, update the jira tickets. 
    
    for key,value in mismatchDict.items():        
        if value.lower() != "no severity":
            issue_result = jc.issue(key,fields='customfield_10102')        
            print('######## Before ########')
            print(key,issue_result.fields.customfield_10102.value)
            issue_result.update(fields={'customfield_10102':{'value':value.title()}})   # we use title() here because jira has the severity defined with the first letter as caps in a drop down list. If whe we set it does not match one of the options perfectly then it will throw an 'id' cannot be null error.
            print('######## After ########')
            print(key,issue_result.fields.customfield_10102.value)
            print()
    
    if len(mismatchDict) == 0:
        print('No mismatched tickets found :D !!!')


if __name__ == "__main__":
    main()
