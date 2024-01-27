import pytest 
from Game_Of_Life import Cell, SetOfCells

def test_SetOfCells_creation():
    set = SetOfCells (50,100,"BlockPattern.txt","output.txt")
    assert isinstance(set, SetOfCells)

def test_functions_set():
    set = SetOfCells (50,100,"BlockPattern.txt","output.txt")
    set.load_cells()
    r = [[None for i in range(50)]for j in range(100)]
    assert set.get_set() != r
    set.clear_cells()
    assert set.get_set()==r