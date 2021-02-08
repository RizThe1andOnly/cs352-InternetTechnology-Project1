"""
    Client code. Will read the input file and send each hostname as request to the root &/or top level servers.
    
    ------------------------

    Organized with the following methods:
        - readInputFile
        - setupClientSocket
        - sendRequest
        - clientFunctionalities
"""

# TODO: sendRequest function !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#imports
import socket

# constants (will use constants to define the address and port for rs and ts until clarification is obtained); these will be changed
RS_HOSTADDRESS = socket.gethostbyname(socket.gethostname())
RS_PORT = 50007
TS_HOSTADDRESS = socket.gethostbyname(socket.gethostname())
TS_PORT = 50008
NS_FLAG = "NS"
OUTPUT_FILE_PATH = './RESOLVED_2.txt' #this needs to be changed to just RESOLVED.txt

def readInputFile(filePath:str='./PROJI-HNS.txt'):
    r"""
        Read the input file line by line. Lines will be stored in a list and returned.

        -----------------
        
        @param
            filePath : path to the input file; the name given will be used

        ----------------

        @return : list - list of addresses to be requested from rs and ts
    """
    
    with open(filePath,'r') as inputfile:
        hostNameList = inputfile.readlines
    
    return hostNameList



def sendRequest(hostName:str,destination:tuple,clientSocket):
    r"""
        Sends a request to either the root server or the top level server based on the destination parameter.

        ---------------

        @param
            hostName : str - the hostname being requested of the servers
            destination : tuple - the (address,port) of the server that is being sent the request
        
        --------------

        @returns : str - the response from the server
    """
    pass


def clientFunctionalities():
    r"""
        First gets list of inputs (by calling readInputFile()). Then opens connection to root and if necessary top level
        server to request the addresses corresponding to hostnames from input files. Requests are made for each input.
        Finally writes to the output file the responses from the requests.
    """

    #setup the client socket:
    clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    #set destination details:
    rs_destination = (RS_HOSTADDRESS,RS_PORT)
    ts_destination = (TS_HOSTADDRESS,TS_PORT)
    
    hostNames = readInputFile() # get inputs
    resultList = [] # list of str's returned by the servers; will be written to the output file at the end

    # make requests for each hostName in the inputfile
    for hostName in hostNames:
        #make request to the root server:
        rootResponse = sendRequest(hostName,rs_destination,clientSocket)

        #check flag:
        if NS_FLAG not in rootResponse:
            resultList.append(rootResponse)
            continue

        # at this point we know we have to send request to the top level server because NS flag was given by root
        tsResponse = sendRequest(hostName,ts_destination,clientSocket)
        
        resultList.append(tsResponse)
    
    #write output to the RESOLVED.TXT
    with open(OUTPUT_FILE_PATH,'a') as outputFile:
        for res in resultList:
            outputFile.write(res)
    
