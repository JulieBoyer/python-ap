from seqtext import Needleman_Wunsch_algo
from seqtext import read_chemin
from seqtext import read_list

def test_align():
    assert Needleman_Wunsch_algo('','',1,-1,-2) == ([[0]], [[(0, 0)]])

def test_readchemin():
    assert read_chemin('','',Needleman_Wunsch_algo('','',1,-1,-2)[1])==[(0, 0)]

def test_readlist():
    assert read_list('','',read_chemin('','',Needleman_Wunsch_algo('','',1,-1,-2)[1]))==('', '')