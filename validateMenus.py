'''
    Created By: Maxime Ndutiye
    Validates a list of menus from an API endpoint by 
    checking whether the nodes in the menus contains 
    cyclical references to themselves
'''

import urllib2
import json

#url = "https://backend-challenge-summer-2018.herokuapp.com/challenges.json?id=1&page="

def getNumberOfPages(url):
    
    #request data from API & load it into python dict()
    response = urllib2.urlopen(url + str(1))
    responseData = json.load(response)   
    
    return responseData["pagination"]["total"]
        
def validateFromEndpoint(url):
    numberOfPages = getNumberOfPages(url)
    menuItemsList = []
    menus = {}
    
    for pageNumber in range(1,numberOfPages+1):
      
        #request data from API & load it into python dict()
        response = urllib2.urlopen(url + str(pageNumber))
        responseData = json.load(response)   
        
        currentMenu = responseData["menus"]
        menuItemsList += currentMenu

    return json.dumps(buildMenus(menuItemsList))
 
def traceSubNodes(currentNodeId, currentSubNodesList, menuNodesList, debth):
    nodesTracedList = []

    # max depth is 3, starting at 0
    if debth == 3:
        nodesTracedList += menuNodesList[currentNodeId-1].get("child_ids")
    else:
        for nodeId in currentSubNodesList:
            nodesTracedList += traceSubNodes(nodeId-1, menuNodesList[nodeId-1].get("child_ids"),
                                            menuNodesList, debth+1)
                    
    # return a list of the node ids instead of the indices
    # add the current node to the traversed nodes
    return nodesTracedList + [currentNodeId + 1]
        
def buildMenus(menuNodesList):
    nodeTraces = []

    for node in menuNodesList:
        nodeId = node.get("id")
        
        # -1 for the proper index 
        nodeTraces.append(traceSubNodes(nodeId-1, 
                      menuNodesList[nodeId-1].get("child_ids"), menuNodesList, 0))
    
    
    return validateMenus(nodeTraces)
    
def checkDuplicates(idList):
    temp = {}
    
    if len(idList) != len(set(idList)):
        return False
    
    return True

def validateMenus(tracedIdsList):
    validMenus = []
    invalidMenus = []

    for index in range(0, len(tracedIdsList)):
        
        if checkDuplicates(tracedIdsList[index]):
            validMenus.append({"root_id":index, "children":tracedIdsList[index]})
        else:
            invalidMenus.append({"root_id":index, "children":tracedIdsList[index]})
            
    return {"valid_menus":validMenus, "invalid_menus":invalidMenus}
        