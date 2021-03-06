from typing import Collection, List
import numpy as np
import copy

class ResizeableMatrix:
    def __init__(self, matrix = None, dtype = int) -> None:
        if matrix:
            self.matrix = matrix
        else:
            self.matrix = np.matrix([[]])
    def append(self, toAppend:List):
        if not np.array_equal(self.matrix, np.matrix([[]])):
            temp_list = self.matrix.tolist()
            temp_list.append(toAppend)

        else:
            temp_list = [toAppend]
        
        
        self.matrix = np.matrix(temp_list)
        del temp_list

    def __getitem__(self, key:Collection):
        if self.matrix is None:
            raise IndexError("Matrix not initialized!")
        x,y = key
        return self.matrix[x, y]

    def __str__(self) -> str:
        return str(self.matrix)
        
    def retrieve_matrix(self):
        return self.matrix