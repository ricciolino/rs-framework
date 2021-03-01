#!/usr/bin/python3.6

from utilities import SetToString
from reaction import Reaction

class ReactionSystem:
    # the pair background set and set of reactiona of the rs
    s = set() # background set of the rs (its elements are called entities)
    a = set() # the set of reaction of the rs
    name = None

    # as for reactions we assume _s and _a sets such that their composition satisfy the definition of rs
    def __init__(self,_name,_s,_a):
        self.name = _name
        self.s = _s
        self.a = _a

    # special method to print the reaction system
    def __str__(self):
        string = ""
        string += f"The reaction_system_{self.name} has the following background set\n\t{SetToString(self.s)}\n"
        string += f"and the following sets of reactions are defined"
        for reac in self.a:
            string += f"\n\t{reac}"
        return string

    # to check if a set of entities is included into the background set
    def BGSetInclude(self,_s):
        return _s.issubset(self.s)

    # Get the result of a rs in a given set (the union of the results of the single reactions), assume that _t is included in _s
    def GetResOverT(self,_t):
        res = set()
        for reac in self.a:
            single_res = set()
            if reac.EnabledBy(_t):
                single_res = reac.products
            res = res.union(single_res)
        return res
