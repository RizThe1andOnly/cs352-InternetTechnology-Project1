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
RS_HOSTADDRESS_LOCAL = socket.gethostbyname(sys.argv[1])
RS_PORT = sys.argv[2]
#TS_HOSTADDRESS_LOCAL = socket.gethostbyname(socket.gethostname())
TS_PORT = sys.argv[3]
NS_FLAG = "NS"
TS_RESPONSE_MARKER = 'NS'
OUTPUT_FILE_PATH = './RESOLVED.txt' #this needs to be changed to just RESOLVED.txt
BUFFER_SIZE = 200


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
    #print(hostName)

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

    #if tsAddress == 'localhost':
        #return TS_HOSTADDRESS_LOCAL

    return tsAddress

def clientFunctionalities(rsHostAddress,rsPort,tsPort):
    r"""
        First gets list of inputs (by calling readInputFile()). Then opens connection to root and if necessary top level
        server to request the addresses corresponding to hostnames from input files. Requests are made for each input.
        Finally writes to the output file the responses from the requests.
    """

    #setup the client socket:
    clientSocket_rs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    clientSocket_ts = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tsConnectionAcheived = False

    #   set destination details and create socket connections:
    if rsHostAddress == 'localhost':
        rsHostAddress = RS_HOSTADDRESS_LOCAL
    rs_destination = (rsHostAddress,rsPort)
    #print(rs_destination)
    clientSocket_rs.connect(rs_destination)

    
    hostNames = readInputFile() # get inputs
    resultList = [] # list of str's returned by the servers; will be written to the output file at the end

    # make requests for each hostName in the inputfile
    for hostName in hostNames:
        #print(hostName)
        #make request to the root server:
        hostName = hostName.lower().strip('\n')
        rsResponse = sendRequest(hostName,clientSocket_rs)

        #check flag:
        if NS_FLAG not in rsResponse:
            resultString = str(hostName + ' ' + rsResponse)
            resultList.append(resultString)
            continue

        # at this point we know we have to send request to the top level server because NS flag was given by 
        if not tsConnectionAcheived:
            ts_destination = (extractTSAddress(rsResponse),tsPort)
            clientSocket_ts.connect(ts_destination)
            tsConnectionAcheived = True
        
        tsResponse = sendRequest(hostName,clientSocket_ts)
        resultString = str(hostName + ' ' + tsResponse)
        resultList.append(resultString)
    
    
    clientSocket_ts.close()
    clientSocket_rs.close()
    
    #write output to the RESOLVED.TXT
    with open(OUTPUT_FILE_PATH,'a') as outputFile:
        for res in resultList:
            outputFile.write(res)
            outputFile.write('\n')
    



if __name__ == "__main__":
    print(os.getpid())

    # parse the command line arguments; the positions of the args are based on instructions:
    listOfArguments = sys.argv
    rsHostAddress = str(listOfArguments[1])
    rsPort = int(listOfArguments[2])
    tsPort = int(listOfArguments[3])

    clientFunctionalities(rsHostAddress,rsPort,tsPort)