import numpy as np

class LevelGenerator:
    def __init__(self, size: tuple[int, int]):
        self.__size = size
        self.__level = np.array([[0 for __ in range (size[0])] for _ in range(size[1])])
        for line in range(size[1]):
            for column in range(size[0]):
                if column == 0 or line == 0 or column == size[0]-1 or line == size[1]-1:
                    self.__level[line][column] = 1

    def get_level(self):
        return self.__level

    def generate(self):
        chance = 0.69
        for line in range(3, self.__size[1]):
            for column in range(1, self.__size[0]):
                if self.__level[line - 2][column] == 0 and self.__level[line - 3][column] == 0:
                    if self.__level[line - 1][column] == 0 and (self.__level[line][column - 1] == 0 or column == 0) and sum(self.__level[line]) < 11:
                        if np.random.random() > (1 - chance):
                            rand_int = np.random.random()
                            row_length = 0
                            while rand_int > 0.32 * row_length:
                                if column+row_length < self.__size[0]:
                                    if self.__level[line - 1][column+row_length] == 0 and (self.__level[line - 1][column+row_length+1] == 0 or column+row_length+1 == self.__size[0]):
                                        self.__level[line][column+row_length] = 1
                                        row_length += 1
                                    else:
                                        break
                                else:
                                    break
