#!/usr/bin/python3.6

import os
import sys
from reaction import Reaction
from utilities import SetToString,SeqToString,SetFromList
from reaction_system import ReactionSystem
from interactive_process import InteractiveProcess

# define a reaction by providing the three sets as lists (it will be automatically converted in sets by the function)
# if the creation isn't right the function will return None
def MakeReaction(_name,_r,_i,_p):
    # pass the entities through lists data structure
    if type(_r) is not list or type(_i) is not list or type(_p) is not list:
        print(f'Please provide the sets as lists data type structure!')
        return None
    # NO ONE of the sets can be empty
    if (len(_r)==0 or len(_i)==0 or len(_p)==0):
        print(f'The reaction_{_name} cannot be created: some of the provided sets is empty')
        return None
    # construct the sets, being sure that each element is viewed as a string (if I would have converted directly
    # in this way: e.g. set([a,1]) the element 1 was been an int instead of a string '1')
    name = str(_name).lower()
    reactants = set()
    inhibitors = set()
    products = set()
    for r in _r:
        reactants.add(str(r).lower())
    for i in _i:
        inhibitors.add(str(i).lower())
    for p in _p:
        products.add(str(p).lower())
    # intersection between reactants and inhibitors must be empty
    if (not reactants.isdisjoint(inhibitors)): # true if the intersection IS NOT empty
        print(f'The reaction_{name} cannot be created: intersection between reactants and inhibitors is not empty')
        return None
    # create the reaction
    return Reaction(name,reactants,inhibitors,products)

# check if a reaction belong to a given nonempty set
def ReactionBelongTo(_r,_s):
    if type(_s) is not set:
        print(f"Please provide _s as a set data type! Can't tell you if the reaction_{_r.name} belong to _s")
        return False
    if len(_s)==0:
        print(f"You have given me an empty set, so the reaction_{_r.name} can't belong to _s")
        return False
    # be sure to consider the elements as string
    str_set = set()
    for elem in _s:
        str_set.add(str(elem))
    return _r.BelongTo(str_set)

# check if a reaction is enabled in a certain nonempty set
def ReactionEnabledBy(_r,_t):
    if type(_t) is not set:
        print(f"Please provide _t as a set data type! Can't tell you if the reaction_{_r.name} is enabled by _t")
        return False
    if len(_t)==0:
        print(f"You have given me an empty set, so the reaction_{_r.name} can't be enabled by _t")
        return False
    # be sure to consider the elements as string
    str_set = set()
    for elem in _t:
        str_set.add(str(elem))
    return _r.EnabledBy(str_set)

# Get the set result of reaction _r over the set _t
def GetResOfReaction(_r,_t):
    # be sure to consider the elements as string
    str_set = set()
    for elem in _t:
        str_set.add(str(elem).lower())
    if _r.EnabledBy(str_set):
        return _r.products
    else:
        return set()

# Get the result of a reaction system _rs over the set _t
def GetResOfReactionSystem(_rs,_t):
    # be sure to consider the elements as string
    str_set = set()
    for elem in _t:
        str_set.add(str(elem).lower())
    # firse check if _t is included into the BGSet
    if _rs.BGSetInclude(str_set):
        return SetToString(_rs.GetResOverT(str_set))
    else:
        return f"The set _s has entities not included in the reaction_system_{_rs.name}"

# Import a set of reactions from file
def LoadRSFromFile(_file):
    _file = open(_file)
    s = (_file.readline()[:-1]).split(',')
    reactions = []
    k = 1
    for line in _file:
        r = [line[:-1].split(';')[0]]
        r = r[0].split(',')
        i = [line[:-1].split(';')[1]]
        i = i[0].split(',')
        if line[-1]==f'\n':
            p = [line[:-1].split(';')[2]]
        else:
            p = [line.split(';')[2]]
        p = p[0].split(',')
        #print(r,i,p)
        reactions += [MakeReaction(k,r,i,p)]
        k += 1
    _file.close()
    return (s,reactions)

# return None if the creation of the rs isn't correct, provide the background set and the set of reactions
def MakeReactionSystem(_name,_bgset,_reactions):
    # pass the background set and the set of reactions as lists
    if type(_bgset) is not list or type(_reactions) is not list:
        print(f'Please provide the sets as lists data type structure!')
        return None
    # NO ONE of the sets can be empty
    if len(_bgset)==0 or len(_reactions)==0:
        print(f'The reaction_system_{_name} cannot be created: the provided background set and/or the set of reactions are empty')
        return None
    # construct the background set, being sure that each element is viewed as a string
    name = str(_name).lower()
    bgset = set()
    for e in _bgset:
        bgset.add(str(e).lower())
    # construct the set of reaction and check that it is included into the background set
    reactions = set()
    for reac in _reactions:
        if type(reac) is Reaction and reac != None:
            if not reac.BelongTo(bgset):
                print(f'some of reactions of the reaction system is not included into the backgroung set: rs definition violated!')
                return None
            else:
                reactions.add(reac) # note that Reaction type object has implemented the logic to prevent a duplicate in a set!
    # if there isn't been a return None, we can return the reaction system
    return ReactionSystem(name,bgset,reactions)

# return None if the creation of the interactive process isn't correct, provide the reaction system and the initial state
def MakeInteractiveProcess(_name,_rs,_c,_interactive_sequence=False):
    if type(_c) is not list:
        print(f'Please provide the context sequence as list of sets!')
        return None
    for s in _c:
        if type(s) is not set:
            print(f"Please provide the context sequence as list of sets!")
            return None
        if not _rs.BGSetInclude(s):
            print(f"Sorry a set of the context sequence do not belong to the background set of the reaction system")
            return None
    if len(_c)==0:
        print(f'The interactive_process_{_name} cannot be created: the provided initial state is empty')
        return None
    name = str(_name).lower()
    return InteractiveProcess(name,_rs,_c,_interactive_sequence)

# ---------------------------------------
# -----------------main------------------
# ---------------------------------------

# check to have provided the name of file in order to load the bgset and the reactions
if len(sys.argv)!=2:
    print("Please provide the name of the file to load the reaction system")
    sys.exit(0)

# build-up the reaction system from file specified by sys.argv[1]
s,reactions = LoadRSFromFile(sys.argv[1])
reaction_system_1 = MakeReactionSystem(1,s,reactions)

# do the choice between automatic and human-interactive
os.system("clear")
choice = -1
while choice!=1 and choice!=2 and choice!=0:
    print(reaction_system_1)
    choice = int(input(f"\nDo you want to do an interactive process with a human interaction? (type 1)\nOR\nDo you prefer to provide directly the entire context sequence? (type 2)\n(type 0 to exit)\n"))
if choice==0:
    sys.exit(0)

# automatic processation, give the initial state only or provide a full sequence of contexts
if choice == 2:
    # check for a correct input sequence
    c_in=""
    while c_in=="":
        c_in = input(f"\nInsert the context sequence C.\nPlease separe the entities with comma and the various step sets with semicolon, no spaces between them.\ne.g. if you want to insert a context sequence of two sets with the entities 1, 2 and 3 and the entities 4, 5 and 6 rispectively, type: 1,2,3;4,5,6\nnote: type '_' to insert an empty set\n")
        if c_in=="":
            print("INVALID INPUT")
    # split the input, separe sets and elements
    c_in = c_in.split(';')
    c = []
    for elem in c_in:
        if elem!='_':
            c += [SetFromList(elem.split(','))]
        else:
            c += [set()]
    # now just save the input context sequence into a string to print it correctly each iteration
    c_str = SeqToString(c) # otherwise each iter c is linked to c into the object
    # build the interactive process over the rs with the inserted context sequence
    interactive_process_1 = MakeInteractiveProcess(1,reaction_system_1,c)   
    # print the initial situation
    os.system("clear")
    print(reaction_system_1)
    print(f"\nThe interactive process over the reaction_system_{reaction_system_1.name} with the following context sequence: C = {c_str}\nis the following:\n")
    print(interactive_process_1)
    # begin the steps
    while interactive_process_1.terminated==False:
        choice = input("\nPress ENTER to go ahead, q to quit\n")
        if choice=='q':
            sys.exit(0)
        # the inner method of the class to update the status
        interactive_process_1.GoAheadOneStep()
        # clear the screen and update the situation
        os.system("clear")
        print(reaction_system_1)
        print(f"\nThe interactive process over the reaction_system_{reaction_system_1.name} with the following context sequence: C = {c_str}\nis the following:\n")
        print(interactive_process_1)

# human interaction, every step define the context set
if choice == 1:
    # check for a correct input sequence
    c_in=""
    while c_in=="":
        c_in = input(f"\nInsert the initial state C0.\nPlease separe the entities with comma, no spaces between them.\ne.g. if you want to insert the initial state with the entities 1, 2 and 3, type: 1,2,3\n")
        if c_in=="":
            print("INVALID INPUT")
    # split the input, separe the elements (in this case the user must provide only the initial context set c0)
    c = [SetFromList(c_in.split(','))]
    # build the interactive process over the rs with the inserted context sequence
    c_str = SeqToString(c) # otherwise each iter c is linked to c into the object
    # build the interactive process over the rs with the inserted context sequence
    interactive_process_1 = MakeInteractiveProcess(1,reaction_system_1,c,True) # True indicates that the process is human-interactive
    # print the initial situation
    os.system("clear")
    print(reaction_system_1)
    print(f"\nThe interactive process over the reaction_system_{reaction_system_1.name} with the following initial state: C0 = {c_str}\nis the following:\n")
    print(interactive_process_1)
    # begin the steps
    while interactive_process_1.terminated==False:
        # the inner method of the class here handles the logic to require the user to insert the next set to use as context set in the rs
        interactive_process_1.GoAheadOneStep()
        # clear the screen and update the situation
        os.system("clear")
        print(reaction_system_1)
        print(f"\nThe interactive process over the reaction_system_{reaction_system_1.name} with the following initial state: C0 = {c_str}\nis the following:\n")
        print(interactive_process_1)
