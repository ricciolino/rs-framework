#!/usr/bin/python3.6

import sys
from reaction_system import ReactionSystem
from utilities import SetToString,SetToBin

class InteractiveProcessBinary:
    # An interactive Process need a rs and an initial state (at least, otherwise also the full context sequence)
    name = None # the ID name
    rs = None # the reaction system in which the interactive process lives
    c = None # context sequence: passsed in init
    d = [set()] # result sequence initially set empty
    w = None # state sequence updated every step
    n_bits = 0
    binarySeq=[]
    i = 0 # step counter
    terminated = False
    context_indip = False
    interactive_context=False

    # the type of interactive process depends on the variable _c
    # assume that _rs is a reaction system, and c is a list of sets with all the elements belonging to the background set of the rs!
    def __init__(self,_name,_rs,_c,_n_bits,_interactive_context=False):
        self.name = str(_name).lower()
        self.interactive_context = _interactive_context
        self.rs = _rs
        self.c = _c
        if len(_c)==1 and self.interactive_context==False: # for sure a context indipendent interactive process
            self.context_indip = True
        if self.interactive_context==True: # ask every step the entities to insert
            self.c = [self.c[0]] # keep only the first set (initial state)
        self.w = [self.c[0].union(self.d[0])] # w0 = c0 initial state
        self.n_bits = _n_bits
        self.binarySeq += [SetToBin(self.w[self.i],self.n_bits)] # initializa binarySeq

    # special method to print the interactive process
    def __str__(self):
        string = "\tC\t\t\t\t\tD\n"
        for k,c_elem,d_elem in zip(range(0,len(self.c)),self.c,self.d):
            string += f"\n{k}\t"
            string += "{0:<40}".format(SetToString(c_elem))
            string += "{0:<16}".format(SetToString(d_elem))
            string += f"{self.binarySeq[k]}"
        if self.terminated==True:
            string += f"\n\nThe interactive_process_{self.name} is terminated."
            if self.context_indip==False:
                string += f"\nIt is not context-indipendent!\n"
            else:
                string += f"\nIt is context-indipendent!\n"
        return string


    def GoAheadOneStep(self):
        if self.terminated==False:
            self.i += 1
            self.d += [self.rs.GetResOverT(self.d[self.i-1].union(self.c[self.i-1]))] # new result Di
            self.binarySeq += [SetToBin(self.d[self.i],self.n_bits)]
            if len(self.c)==self.i and self.interactive_context==False:
                self.w += [self.d[self.i]]
                self.c += [set()] # from now on every Ci would be empty
            elif self.interactive_context==False:
                self.w += [self.d[self.i].union(self.c[self.i])]
            else: # then here interactive_context would be True
                new_entities=""
                while new_entities=="":
                    new_entities = input(f"\nInsert the new context entities knowing that the next result is Di = {self.d[self.i]}\nPlease separe the entities with comma and no spaces (e.g. if you insert the entities 1, 2 and 3 type: 1,2,3)\nnote: type '_' to add an empty set , type q to quit\n")
                    if new_entities=="":
                        print("INVALID INPUT")
                    if new_entities=='q':
                        sys.exit(0)
                if new_entities=='_':
                    new_entities = set()
                else:
                    new_entities = set(new_entities.split(','))
                self.c += [new_entities]
                self.w += [self.d[self.i].union(self.c[self.i])]
            # stop if Wi is empty
            print(self.w[self.i])
            if self.w[self.i] == set():
                self.terminated = True
                # check if it is context-indipendent
                if self.context_indip==False:
                    for (elem1,elem2) in zip(self.c[1:],self.d[1:]):
                        if not elem1.issubset(elem2):
                            break
                    else:
                        self.context_indip = True
                



