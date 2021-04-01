0. Mihir Desai (mvd67) and Rizwan Chowdhury(...)

1. Our LS has many features I  will briefly describe them below. First, when the client sends a query to the LS the LS then forwards it to both the TS servers at the same time. To avoid the return message error we made sure only the correct TS replied meaning the one with the answer stored on it. If the TS doesn't have an answer for the query it doesn't reply but keeps the ports active. When TS replies the LS then forwards that answer to the client, but if there is no response from TS we have set a 5 seconds timeout period on the LS after which the LS will reply with an error message. This error message is then forwarded to the client.

2. We have extensively tested our project since we got a bad grade on the last one. So far we did not find any errors and we hope it works fine when tested by the TAs.

3. We did not face any major significant problems. The only thing that challenged us was the load balancing part of the project it was tricky at first but we figured it out in a way that was beneficial for our project.

4. We learned a lot from this project, first the important load balancing technique and how it is being implemented in the real world. Second, we learned important skills by working in teams we hope these skills and experience will help us in our professional life.
