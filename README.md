# Regular-expression-to-Thompson-NFA
This repository contains my code for changing regular expression to Thompson NFA

How it works?

It takes as an input ! line which is the regular expression and it outputs 5 lines. The first line should contain the states separated by comma and space for example Q0, Q1, Q2 .
The second line should contain alphabet separated by comma and space for example a, b, , s
The third line should have the start state for example Q0
The fourth line should have the accept state for example Q8
The fifth line should contain the transitions in the following form :
( Q0 , a , [Q1] ) , ( Q1 , b , [Q2] )
