"""
    Root server code.

    ------------------

    Will use a dictionary to store the DNS data.
        - The dictionary will be formatted in the following way:
            - key : hostname (the url)
            - value: tuple -> (ip address, A/NS)
    
    ----------------

    The rs code will be organized several methods and the main section that calls the methods. The methods are:
        - getDNSEntries
        - processDNSQuery (check if hostname exists in the server dictionary)
        - server
"""

import os
import socket
import threading
import time



TOP_LEVEL_SERVER = "TopLevelServer"
MAX_REQUEST_SIZE = 200

def getDNSEntries(filePath = "./PROJI-DNSRS.txt"):
    r"""
        Will read the "PROJI-DNSRS.txt" file to obtain the DNS entries to be stored for the 
        server. Will go through each line and put the entries in a dictionary as described above.
        Will return the dictionary as a result.

        ---------------

        @params:
            - filePath : path to the file; default set to given input in the same directory

        ----------------

        @return:
            dict : ip address and flag as value with hostname as key
    """
    
    #initiate the dictionary:
    dnsEntryDict = {}

    #read file and populate dictionary
    with open(filePath,mode='r') as entryFile:
        for entryLine in entryFile.readlines():
            entryComponents = entryLine.split()
            if "NS" in entryComponents:
                #the ns entry in the input only has address and flag so...
                hostName = TOP_LEVEL_SERVER # static name i came up with myself as a place holder
                address = entryComponents[0]
                flag = entryComponents[2] # not 1 since there is a '-' in the line

                dnsEntryDict[hostName]  = (address,flag)
            else:
                hostName = entryComponents[0]
                address = entryComponents[1]
                flag = entryComponents[2]

                dnsEntryDict[hostName]  = (address,flag)
    
    return dnsEntryDict


def getItemFromDict(itemKey:str,dnsDict:dict):
    r"""
        Returns item from the dictionary containing the dns information. This was implemented
        because the get() method for dictionaries was not working for our case.

        --------------------

        @param:
            itemKey : the hostname being queried
            dnsDict : the dictionary with dns data
    """
    for key in dnsDict.keys():
        #print(itemKey,len(itemKey),key,len(key))
        if itemKey == key:
            return dnsDict[key]
    return dnsDict[TOP_LEVEL_SERVER]


def processDNSQuery(queriedHostname:str,dnsDict:dict):
    r"""
        Searches the dns dictionary for the queried hostname. If it exists then it returns the
        address and flag associated with it in the dictionary. 
        
        --------------------

        @param:
            
            queriedHostname : the hostname to be looked up, supplied by the client
            dnsDict : data structure holding the dns mappings; generated by getDNSEntries()
        
        --------------------

        @return:
            
            str :  the address and flag associated with the provided hostname if it exists. If it does not then this method returns the top level server and "NS".
        
        ---------------------

        Uses the get() method of the dns dictionary where if the key does not exist then the 
        top level server data will be returned. The key of the dictionary will be the host name/
        domain name.
    """
    
    # get the (hostname,flag) tuple that will be the response to the client request; dnsDict.get(queriedHostname,dnsDict.get(TOP_LEVEL_SERVER)) ;getItemFromDict(queriedHostname,dnsDict)
    #print(queriedHostname)
    queryResponseEntry = dnsDict.get(queriedHostname,dnsDict.get(TOP_LEVEL_SERVER))
    #print(queryResponseEntry)

    # turn the response entry to a string (so it can be sent back through socket stream)
    toBeReturned = ''
    toBeReturned = queryResponseEntry[0] + " " + queryResponseEntry[1]

    return toBeReturned



def server():
    r"""
        Method to set up server and keep it running. Based on project zero code.

        ---------------------

        Will receive requests from the client and check the dns dictionary 
        (which will be set up at the start of this method) to see if the hostname
        exists. If it does then its corresponding details will be returned, if not then
        the top level server details will be returned.

        ------------------------

        For now will bind server to localhost and test on same machine for all scripts.
        Will change this later to include capabilities to run on multiple machines.

        ...

        ***Note !!!!! ***
        Also currently this code is written so that the server closes after one client request is served.
        I do not know yet if this is right or how to do it in another way. We can test and look up how to 
        do it the best way going forward. Sorry for leaving it incomplete.

        ...

        ***Note !***
        The code for ts.py will be very similar to this if not identical.
    """
    
    # set the host address or port based on project requirements here
    hostAddress = ''
    hostPort = 50007

    #setup dns data structure:
    dnsDict = getDNSEntries()

    #create the server socket and initiate it:
    try:
        serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except:
        exit()
    
    serverBindingDetails = (hostAddress,hostPort)
    serverSocket.bind(serverBindingDetails)
    serverSocket.listen()

    #wait for client request and process the request:
    clientSocketId, clientAddress = serverSocket.accept()

    # loop so that multiple requests can be received:
    while(1):
        try:
            #print("waiting")

            #   extract data from client socket:
            clientDataReceived_bytes = clientSocketId.recv(MAX_REQUEST_SIZE)
            clientDataReceived = clientDataReceived_bytes.decode('utf-8').strip()

            #   check if hostname is in the root dns server:
            toBeSentBackToClient = processDNSQuery(clientDataReceived,dnsDict)
            #print(toBeSentBackToClient)

            #   return the results to the client:
            clientSocketId.send(toBeSentBackToClient.encode('utf-8'))
        except:
            break
    

    serverSocket.close()
    exit()



if __name__ == "__main__":
    print(os.getpid())
    serverThread = threading.Thread(name='serverThread',target=server)
    serverThread.start()
    print("Server Thread Started")