#!/usr/bin/python3.6

class Reaction:
    # the sets of reactants, inhibitors and products of the reaction
    name = None
    reactants = set()
    inhibitors = set()
    products = set() 

    # the creation of a reaction is made through the called of a function in which all the controls are performed, so we can
    # assume that reactants, inhibitors and products arrives to this initialization already as sets, and we can
    # assume moreover that the checks of correctness of the reaction is already been done
    def __init__(self,_name,_reactants,_inhibitors,_products):
        self.name = _name
        self.reactants = _reactants
        self.inhibitors = _inhibitors
        self.products = _products

    # special method to print easily a reaction
    def __str__(self):
        # put in string the reactants
        rappresentation = "({"
        for r in self.reactants:
            rappresentation += r + ','
        rappresentation = rappresentation[:-1] # remove the ,
        # put in string the inhibitors
        rappresentation += "},{"
        for i in self.inhibitors:
            rappresentation += i + ','
        rappresentation = rappresentation[:-1] # remove the ,
        # put in string the products
        rappresentation += "},{"
        for p in self.products:
            rappresentation += p + ','
        rappresentation = rappresentation[:-1] # remove the ,
        rappresentation += "})"
        return 'reaction_' + self.name + ' = ' + rappresentation

    # check if a reaction belong to a given nonempty set
    def BelongTo(self,s):
        return self.reactants.issubset(s) and self.inhibitors.issubset(s) and self.products.issubset(s)

    # check if a reaction is enabled by a given nonempty set
    def EnabledBy(self,t):
        return self.reactants.issubset(t) and self.inhibitors.isdisjoint(t)

    # special method to permit a list of reactions to map into a set
    def __hash__(self):
        return 0

    # special method to check if two reactions are equals
    def __eq__(self,other):
        if isinstance(other,Reaction):
            return self.reactants == other.reactants and self.products == other.products and self.inhibitors == other.inhibitors
        return NotImplemented
