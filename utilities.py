#!/usr/bin/python3.6

# this function is simply to provide a set with string elements strarting from generic list
def SetFromList(_l):
    s = set()
    for elem in _l:
        s.add(str(elem).lower())
    return s

# this function is simply to remove the quotes of the strings in a set (to print)
def SetToString(_s):
    if _s==set():
        return "{}"
    string = '{'
    for elem in _s:
        string += str(elem) + ','
    string = string[:-1]
    string += '}'
    return string

# this function is simply to convert a sequence of sets into a well formatted string to print
def SeqToString(_l):
    if _l==[]:
        return "[{}]"
    string = '{'
    for elem in _l:
        string += SetToString(elem) + ','
    string = string[:-1]
    string += '}'
    return string

# use this function to map the sets into the correspondent binary number (case of the binary counter example)
def SetToBin(_s,_n):
    num=""
    for i in range(0,_n):
        num+='0'
    for elem in _s:
        num=list(num)
        num[_n-1-int(elem[1])]='1'
        num="".join(num)
    return num


