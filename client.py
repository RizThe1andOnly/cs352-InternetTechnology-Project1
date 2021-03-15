"""
    Client code. Will read the input file and send each hostname as request to the root &/or top level servers.
    
    ------------------------

    Organized with the following methods:
        - readInputFile
        - setupClientSocket
        - sendRequest
        - clientFunctionalities
"""



#imports
import socket
import os
import sys

# constants (will use constants to define the address and port for rs and ts until clarification is obtained); these will be changed
RS_HOSTADDRESS_LOCAL = socket.gethostbyname(socket.gethostname())
TS_HOSTADDRESS_LOCAL = socket.gethostbyname(socket.gethostname())
NS_FLAG = "NS"
TS_RESPONSE_MARKER = 'NS'
OUTPUT_FILE_PATH = './RESOLVED.txt' #this needs to be changed to just RESOLVED.txt
BUFFER_SIZE = 200
RESULT_STRING_DELIMITER = '\n'


def readInputFile(filePath='./PROJI-HNS.txt'):
    r"""
        Read the input file line by line. Lines will be stored in a list and returned.

        -----------------
        
        @param
            filePath : path to the input file; the name given will be used

        ----------------

        @return : list - list of addresses to be requested from rs and ts
    """
    
    with open(filePath,'r') as inputfile:
        hostNameList = inputfile.readlines()
    
    return hostNameList



def sendRequest(hostName,clientSocket):
    r"""
        Sends a request to either the root server or the top level server based on the destination parameter.

        ---------------

        @param
            hostName : str - the hostname being requested of the servers
            destination : tuple - the (address,port) of the server that is being sent the request
        
        --------------

        @returns : str - the response from the server
    """

    #send server the hostname:
    clientSocket.send(hostName.encode('utf-8'))

    #wait for response from server:
    dataFromServer = clientSocket.recv(BUFFER_SIZE).decode('utf-8')

    return dataFromServer


def extractTSAddress(rsResponse):
    r"""
        Used when a call to the Top Level server is required. Will extract the ts address from the
        rs response.

        ---------------------

        @param:
            rsResponse : the string received from the rs
        
        ---------------------

        returns : ip address of the top level server
    """
    
    nsIndex = rsResponse.index(TS_RESPONSE_MARKER) # index of where the "NS" flag appears; this will help isolate the address for the top level server
    tsAddress = rsResponse[:nsIndex].strip()

    if tsAddress == 'localhost':
        return TS_HOSTADDRESS_LOCAL

    return tsAddress

def clientFunctionalities(rsHostName,rsPort,tsPort):
    r"""
        First gets list of inputs (by calling readInputFile()). Then opens connection to root and if necessary top level
        server to request the addresses corresponding to hostnames from input files. Requests are made for each input.
        Finally writes to the output file the responses from the requests.
    """

    # get host address from provided hostname
    #rsHostName = '' if rsHostName == 'localhost' else rsHostName
    rsHostAddress = socket.gethostbyname(rsHostName)
    
    #setup the client socket:
    clientSocket_rs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    clientSocket_ts = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tsConnectionAcheived = False

    #   set destination details and create socket connections:
    if rsHostName == 'localhost':
        rsHostAddress = RS_HOSTADDRESS_LOCAL
    rs_destination = (rsHostAddress,rsPort)
    clientSocket_rs.connect(rs_destination)

    
    hostNames = readInputFile() # get inputs
    aggResString = ''

    # make requests for each hostName in the inputfile
    for hostName in hostNames:
        #make request to the root server:
        hostName = hostName.lower().strip('\n')
        hostName = hostName.strip()
        rsResponse = sendRequest(hostName,clientSocket_rs).strip()

        #check flag:
        if NS_FLAG not in rsResponse:
            resultString = hostName + ' ' + rsResponse
            aggResString += resultString + RESULT_STRING_DELIMITER
            continue

        # at this point we know we have to send request to the top level server because NS flag was given by 
        if not tsConnectionAcheived:
            ts_destination = (socket.gethostbyname(extractTSAddress(rsResponse)),tsPort)
            clientSocket_ts.connect(ts_destination)
            tsConnectionAcheived = True
        
        
        tsResponse = sendRequest(hostName,clientSocket_ts).strip()
        resultString = hostName + ' ' + tsResponse
        aggResString += resultString + RESULT_STRING_DELIMITER
    
    
    clientSocket_ts.close()
    clientSocket_rs.close()
    
    #write output to the RESOLVED.TXT
    with open(OUTPUT_FILE_PATH,'a') as outputFile:
        outputFile.write(aggResString)
        
    



if __name__ == "__main__":
    
    # parse the command line arguments; the positions of the args are based on instructions:
    listOfArguments = sys.argv
    rsHostAddress = str(listOfArguments[1])
    rsPort = int(listOfArguments[2])
    tsPort = int(listOfArguments[3])

    clientFunctionalities(rsHostAddress,rsPort,tsPort)