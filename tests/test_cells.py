import pytest 
from Game_Of_Life import Cell

def test_cell_creation():
    cell = Cell (0,1,True)
    assert isinstance(cell, Cell)

def test_functions_cells():
    cell = Cell (0,1,True)
    assert cell.isAlive()==True
    assert cell.getCol()== 1
    assert cell.getRow()== 0