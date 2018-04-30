from jira.client import JIRA
from zenpy import Zenpy
import logging
import json

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

def main():
    # create logger
    log = logging.getLogger(__name__)

    # NOTE: You put your login details in the function call connect_jira(..) below!

    # create a connection object, jc
    jc = connect_jira(log, "https://your_domain.atlassian.net", "your_username", "your_password")

    # print names of all projects
    #issues_in_proj = jc.search_issues('your_query_here',maxResults=50000)

    issue_result = jc.issue('UEAW-8219',fields='customfield_10102')
    print(vars(issue_result))
    print(issue_result.fields.customfield_10102.value)
    #issue_result.fields.customfield_10102.value = 'showstopper'
    issue_result.update(fields={'customfield_10102':{'value':'Showstopper'}})
    print(issue_result.fields.customfield_10102.value)


    
    
    





if __name__ == "__main__":
    main()
