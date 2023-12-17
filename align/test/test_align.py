from seqtext import Needleman_Wunsch_algo

def test_align():
    assert Needleman_Wunsch_algo('','',1,-1,-2) ==([[0]],[[(0,0)]],[[0]])
