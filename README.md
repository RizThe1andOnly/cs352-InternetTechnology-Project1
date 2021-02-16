# CS352: Internet Technology - Project 1

0 - Rizwan Chowdhury (rzc2) and Mihir Desai (put netid here)

1 - We implemented the client function by using loops for both the client and the two servers. The client used a for loop to go through each line (hostname)
    and send a req to the appropriate server for a response using the send() method for sockets. The root and top-level servers implement a while loop that 
    repeatedly accept incoming requests. Each of these servers call listen() and accept() once to establish a connection with the client process. Once the
    connection is established, the servers await for requests from the client using recv() method. The recv() method is in the while loop so that the servers
    can continue to receive requests from the client while the connection continues to be established.

2 - As far as we are aware there are currently no known issues with our code.

3 - While developing this code we faced a few minor problems. The first had to do with setting up rs.py and ts.py to listen to multiple requests from the client.
    We looked up that using a loop would handle that issue but we had to experiment with which statements should or should not be inside of the loop. At first we
    included the serverSocket.accept() method within the loop which was erroneous, we then moved it outside the loop and acheived proper functionality. Another minor
    issue was related the strings that were sent through the network. These strings had an additional whitespace that led to errors when trying use them as keys for
    getting values from the dictionary data structure. We resolved this issue by using the strip() method, in the servers, to the string received from the client.
    This got rid of the whitespace which led to proper results in getting values from the dictionary data structure.

4 - While doing this project we learned a few interesting and cool things. The first was how to use loops and socket methods to accept more than one set of data from the
    client. The other things was how to log onto and use the iLab machines using ssh. This was a brand new experience and we got to learn how to log on using ssh and transfer files
    using scp.

