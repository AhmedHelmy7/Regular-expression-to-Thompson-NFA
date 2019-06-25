
# coding: utf-8

# In[27]:

import argparse
import re
from collections import OrderedDict

counter=0;
class Transition:
      def __init__(self,State1,State2,Symb):
          self.State1=State1
          self.State2=State2
          self.Symb=Symb
      def __str__(self):
          return '('+self.State1.strip()+', '+self.Symb+', ['+self.State2.strip()+'])'
          
class NFA:
  def __init__(self,States,Symbols,StartState,AcceptState,Transitions):
    self.States=States
    self.Symbols=Symbols
    self.StartState=StartState
    self.AcceptState=AcceptState
    self.Transitions=Transitions.copy()

def makeStateSym(a):
    global counter
    State1=' q{}'.format(counter)
    counter+=1
    State2=' q{}'.format(counter)
    counter+=1
    tran=[]
    tran.append(Transition(State1,State2,a))
    result=NFA(''+State1+','+State2,''+a,State1,State2,tran)
    #a.StartState=StartState+State1+''
    #a.AcceptStates=AcceptStates+State2+''    
    #a.Symbols+=a+','
    #a.Transitions+='('+State1+','+a+',['+State2+']),'
    return result

def concat(a,b):
    trans=[]
    oldStates=a.States.split(',')
    newStates=''
    removedState=a.AcceptState
    for i in range(0,len(oldStates)):
        if oldStates[i]!=removedState:
            newStates+=oldStates[i]+','
    for i in range(0,len(a.Transitions)):
        if(a.Transitions[i].State2==removedState):
            a.Transitions[i].State2=b.StartState
    
    
    newSymbols=a.Symbols+b.Symbols
    newSymbols="".join(OrderedDict.fromkeys(newSymbols))
    result=NFA(newStates+b.States,newSymbols,a.StartState,b.AcceptState,a.Transitions+b.Transitions)
    return result


def union(a,b):
    global counter
    State1=' q{}'.format(counter)
    counter+=1
    State2=' q{}'.format(counter)
    counter+=1
    trans=[]
    trans.append(Transition(State1,a.StartState,' '))
    trans.append(Transition(State1,b.StartState,' '))
    trans.append(Transition(a.AcceptState,State2,' '))
    trans.append(Transition(b.AcceptState,State2,' '))
    newSymbols=a.Symbols+b.Symbols+' '
    newSymbols="".join(OrderedDict.fromkeys(newSymbols))
    result=NFA(State1+','+State2+','+a.States+','+b.States,newSymbols,State1,State2,trans+a.Transitions+b.Transitions)
    return result
def kleeneStar(a):
    global counter
    State1=' q{}'.format(counter)
    counter+=1
    State2=' q{}'.format(counter)
    counter+=1
    trans=[]
    trans.append(Transition(State1,a.StartState,' '))
    trans.append(Transition(a.AcceptState,State2,' '))
    trans.append(Transition(State1,State2,' '))
    trans.append(Transition(a.AcceptState,a.StartState,' '))
    newSymbols=a.Symbols+' '
    newSymbols="".join(OrderedDict.fromkeys(newSymbols))
    result=NFA(State1+','+State2+','+a.States,newSymbols,State1,State2,trans+a.Transitions)
    return result

def questionMark(a):
    trans=[]
    trans.append(Transition(a.StartState,a.AcceptState,' '))
    newSymbols=a.Symbols+' '
    newSymbols="".join(OrderedDict.fromkeys(newSymbols))
    result=NFA(a.States,newSymbols,a.StartState,a.AcceptState,trans+a.Transitions)
    return result

def plus(a):
    global counter
    State1=' q{}'.format(counter)
    counter+=1
    State2=' q{}'.format(counter)
    counter+=1
    trans=[]
    trans.append(Transition(State1,a.StartState,' '))
    trans.append(Transition(a.AcceptState,State2,' '))
    trans.append(Transition(a.AcceptState,a.StartState,' '))
    newSymbols=a.Symbols+' '
    newSymbols="".join(OrderedDict.fromkeys(newSymbols))
    result=NFA(State1+','+State2+','+a.States,newSymbols,State1,State2,trans+a.Transitions)
    return result 

def infixToPostfix(expression):
    operatorStack=[]
    postfix=[]
    expressionList=list(expression)
    concatFlag=0
    for i in range(0,len(expressionList)):
        if expressionList[i] in 'abcdefghijklmnopqrstuvwxyz ' or expressionList[i] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' or expressionList[i] in '0123456789' :
            postfix.append(expressionList[i])
            if(i<(len(expressionList)-1) and (expressionList[i+1] in 'abcdefghijklmnopqrstuvwxyz' or expressionList[i+1] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' or expressionList[i+1] in '0123456789' or expressionList[i+1] == '(')):
                concatFlag=1
                
        elif expressionList[i] == '(':
            operatorStack.append(expressionList[i])
        elif expressionList[i] == ')':
            topToken = operatorStack.pop()
            while topToken != '(':
                postfix.append(topToken)
                topToken = operatorStack.pop()
            if(i<(len(expressionList)-1) and (expressionList[i+1] in 'abcdefghijklmnopqrstuvwxyz ' or expressionList[i+1] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' or expressionList[i+1] in '0123456789')):
                concatFlag=1

        elif expressionList[i]=='*' or expressionList[i]=='+' or expressionList[i]=='?':
            postfix.append(expressionList[i])
            if(i<(len(expressionList)-1) and (expressionList[i+1] in 'abcdefghijklmnopqrstuvwxyz ' or expressionList[i+1] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' or expressionList[i+1] in '0123456789' or expressionList[i+1] == '(')):
                concatFlag=1
        else:
            operatorStack.append(expressionList[i])

        if concatFlag==1:
            operatorStack.append('.')
        concatFlag=0

    while not len(operatorStack)==0:
        postfix.append(operatorStack.pop())
    return "".join(postfix)


def operate(postfix):
    postfixList=list(postfix)
    stack=[]
    for i in range(0,len(postfixList)):
        if postfixList[i] in 'abcdefghijklmnopqrstuvwxyz ' or postfixList[i] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' or postfixList[i] in '0123456789' :
            r=makeStateSym(postfix[i])
            stack.append(r)
        elif postfixList[i]=='|':
            b=stack.pop()
            a=stack.pop()
            r=union(a,b)
            stack.append(r)
        elif postfixList[i]=='*':
            a=stack.pop()
            r=kleeneStar(a)
            stack.append(r)
        elif postfixList[i]=='+':
            a=stack.pop()
            r=plus(a)
            stack.append(r)
        elif postfixList[i]=='?':
            a=stack.pop()
            r=questionMark(a)
            stack.append(r)
        elif postfixList[i]=='.':
            b=stack.pop()
            a=stack.pop()

            r=concat(a,b)
            stack.append(r)
    return r
            
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?",
                        metavar="file")

    args = parser.parse_args()

    file1 = open(args.file, 'r',encoding='utf-8') 
    f = file1.read()
    file1.close()
    
 
    file2 = open("Task_2_result.txt","w+")   
    
    #for match in RegExp:
    #   s+=match+'.'
    #regex='((E|a)b?)*'
    regex=f
    regex=regex.replace('ε',' ')
    #regex=''      IF YOU NEED TO ASSIGN A REGEX DIRECTLY
    #result='Regular expression is "'+regex+'"\n'
    #result+='The postfix of the expression is "'+infixToPostfix(regex)+'"\n'
    result=''
    r4=operate(infixToPostfix(regex))
    
    result+=''+r4.States+'\n'
    result=result[1:]
    #print(r4.Symbols)#Symbols[:-1]
    symb=', '.join(r4.Symbols)
    result+=''+symb+'\n'
    result+=''+r4.StartState[1:]+'\n'
    result+=''+r4.AcceptState[1:]+'\n'
    for k in range(len(r4.Transitions)) :
        result+=Transition.__str__((r4.Transitions[k]))+', '
        
    result=result[:-2]
    print(result)
    file2.write(result)
        
    file2.close()

