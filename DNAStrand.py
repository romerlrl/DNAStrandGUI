#!/usr/bin/env python
# coding: UTF-8
#
## @package DNAStrand
#
#   Playing with string matching.
#
#   @author Paulo Roma
#   @studant Lucas Romer Leão
#   @since 15/12/2019
#   @see https://www.sciencedirect.com/topics/medicine-and-dentistry/dna-strand
#
import sys

class DNAStrand:

    ## Valid DNA symbols.
    symbols = 'ATCG'

    ##
     # Constructs a DNAStrand with the given string of data, 
     # normally consisting of characters 'A', 'C', 'G', and 'T'.
     # Raises a ValueError exception, in case of an invalid givenData strand.
     #
     # @param givenData string of characters for this DNAStrand.
     #
    def __init__(self, givenData):
        ## Strand of this DNA, in upper case.
        try:
            self.strand = str(givenData).upper()
            self.len=len(self.strand)
            raise self.isValid()
        except:
            pass
        # ...


    ## Returns a string representing the strand data of this DNAStrand.
        ##Completo
    def __str__(self):
        return self.strand
    ## return len(self.strand) when len(DNAStrand) demmand
    def __len__(self):
        return len(self.strand)
    ##
     # Returns a new DNAStrand that is the complement of this one,
     # that is, 'A' is replaced with 'T' and so on.
     #
     # @return complement of this DNA.
     #
     #   Feito, mas poderá ser removido mais adiante
     # Um efeito colateral do createComplement é denunciar que a fita é ou não válida.
    def createComplement(self):
        complement = ""
        manual= "TCAGTC"
        for i in self.strand:
            bar=manual.index(i)+2
            complement+=manual[bar]
        return DNAStrand(complement)
    

    def Move(self, other, shift=0):
        str_fita1=self.strand
        str_fita2=other.strand
        if shift>-1:
            str_fita2='-'*shift+str_fita2
        else:
            str_fita1='-'*abs(shift)+str_fita1
        str_fita2+='-'*len(str_fita1)
        str_fita1d=str()
        str_fita2d=str()
        for k in range(len(str_fita1)):
            x, y = str_fita1[k], str_fita2[k]
            if not(self.matches(x, y)):
                x=x.lower()
                y=y.lower()
            str_fita1d+=x
            str_fita2d+=y
        str_fita2d+=str_fita2[k+1:].lower()
        print(str_fita1d)
        print(str_fita2d)
        str_fita1d=str_fita1d.replace("-", "")
        str_fita2d=str_fita2d.replace("-", "")
        return str_fita1d, str_fita2d
            
        
        
    ##
     # Returns a string showing which characters in this strand are matched
     #  with 'other', when shifted left by the given amount.
     #
     # @param other given DNAStrand.
     # @param shift number of positions to shift other to the left.
     # @return a copy of this strand, where matched characters are upper case 
     #         and unmatched, lower case.
     
    def MoveToLeft(self, other, shift):
        nova=other.strand[shift:]
        if len(nova)<self.len:
            nova+='-'*self.len
        print(self)
        print(nova)

        return self.Compare(nova)
    
    ##
     # Returns a string showing which characters in this strand are matched
     #  with 'other', when shifted right by the given amount.
     #
     # @param other given DNAStrand.
     # @param shift number of positions to shift other to the left.
     # @return the Compare of a copy of this strand, where matched characters are upper case 
     #         and unmatched, lower case.
    def MoveToRight(self, other, shift):
        nova='-'*shift+other.strand
        print(nova)
        print(nova)
        if len(nova)<self.len:
            nova+='-'*self.len
        return self.Compare(nova)

    ##
     # Retorna uma tupla contendo um valor numérico com o total de
     # de matches encontrados e a string formada.
     # @param outra fita de DNA previamente formato na família MoveGo

    def Compare(self, STRother):
        if type(STRother)==DNAStrand:
            STRother=STRother.strand
        INTtotal=int()
        STRresultado=str()
        for k in range(0, self.len):
            string=self.strand[k]+STRother[k]
            string=string.lower()
            if string in "ata:gcg":
                INTtotal+=1
                string=string.upper()
            STRresultado+=string[0]
        return (INTtotal, STRresultado)

        


    ##
     # Returns the maximum possible number of matching base pairs,
     # when the given sequence is shifted left or right by any amount.
     #
     # @param other given DNAStrand to be matched with this one.
     # @return maximum number of matching pairs.
     #
    def findMaxPossibleMatches(self, other):
        COUNT=[0, 0]
        COUNTpai=[COUNT, 0]
        for k in range(1, len(other)):
            x=self.MoveToLeft(other, k)
            if x[0]>COUNT[0]:
                COUNT=x
                COUNTpai=[COUNT, -k]
        for k in range(0, len(self)+1):
            x=self.MoveToRight(other, k)
            if x[0]>COUNT[0]:
                COUNT=x
                COUNTpai=[COUNT, k]
        return COUNTpai


    ##
     # Determines whether all characters in this strand 
     # are valid ('A', 'G', 'C', or 'T').
     #
     # @return True if valid, and False otherwise.
     #
    def isValid(self):
        valid = set(self.strand) <= {"G", "A", "T", "C"}
        valid = valid and bool(self.strand)
        return valid
    

    ##
     # Counts the number of occurrences of the given character in this strand.
     # Utiliza o método ".count()" padrão de strings e listas
     #
     # @param ch given character.
     # @return number of occurrences of ch.
     #
    def letterCount(self,ch):
        count = self.strand.count(ch)
        return count
    

    ##
     # Returns True if the two characters form a base pair 
     # ('A' with 'T' or 'C' with 'G').
     #
     # @param c1 first character.
     # @param c2 second character.
     # @return True if they form a base pair, and False otherwise.
     #
    def matches(self, c1, c2):
        match = False
        pairs="ATA:CGC"
        match = c1+c2 in pairs
        return match
    
## Main program for testing.
 #
 # @param args two DNA strands.
 #    

def main (args=None):
    if args is None:
       args = sys.argv

    if len(args) == 5:
       d = DNAStrand(args[1])
       d2 = DNAStrand(args[2])
       ls = int(args[3])
       rs = int(args[4])
    else:
       d = DNAStrand ("AGAGCAT")
       d2 = DNAStrand ("TCAT")
       ls = 2
       rs = 3

    print(d, d2)
    try:
        d2.createComplement()
        print(f"Complement: {d.createComplement()}") 
        print(f"Count A in {d}: {d.letterCount('A')}")
        print(f"{d} isValid: {d.isValid()}")
        print(f"Strand: {d2}")
        print(f"RightShift: {d}, {rs} = {d2.MoveToRight(d,rs)[1]}")
        print(f"Left Shift: {d}, {ls} = {d2.MoveToLeft(d,ls)[1]}")
        print(f"Maximum Matches: {d2.findMaxPossibleMatches(d)[0]}")
        print(f"Number of matches left shift: {d2}, {ls+rs} = {d.MoveToLeft(d2,ls+rs)[0]}")
    except ValueError:
        print("Ao menos uma fita não e válida")

def findMaxAux(fita1, fita2):
    if type(fita1)!=DNAStrand: fita1=DNAStrand(fita1)
    if type(fita2)!=DNAStrand: fita2=DNAStrand(fita2)
    foo=fita1.findMaxPossibleMatches(fita2)
    bar=fita2.findMaxPossibleMatches(fita1)
    fita1D=dict()
    fita1D["MAX"]=(foo[0][0])
    fita1D["RES"]=foo[0][1] if foo[0][1]!=0 else fita1.strand.lower()
    fita1D["MOV"]=(foo[1])

    fita2D=dict()
    fita2D["MAX"]=(bar[0][0])
    fita2D["RES"]=(bar[0][1] if bar[0][1]!=0 else fita2.strand.lower())
    fita2D["MOV"]=(bar[1])
    espacamento=str("_"*abs(fita1D["MOV"]))
    if fita2D["MOV"]>0:
        fita1D["RES"]=espacamento+fita1D["RES"]
    else:
        fita2D["RES"]=espacamento+fita2D["RES"]
    retorno={"MOV":fita1D["MAX"], "fita1":fita1D["RES"], "fita2":fita2D["RES"]}
    return retorno

foo="GATA"
foo_r="CTAT"
aux1=DNAStrand("GATA")
aux2=DNAStrand("CTTT")
#if __name__ == "__main__" and False:
#   sys.exit(main((1, foo, foo_r, 0, 10)))
