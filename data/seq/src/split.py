import random
import pandas as pd

class Spliter:
    def __init__(self, X, y, valid_size=0.1, test_size=0.1):
        # X와 y는 pd.Series
        self.X = X
        self.y = y
        self.valid_size = valid_size
        self.test_size = test_size
        self.train_size = 1 - (valid_size + test_size)

    def split(self):
        # X와 y의 크기가 다르면 False를 리턴, 아니면 True를 리턴
        if len(self.X) != len(self.y):
            return False
        else:
            size = len(self.X)
            index = list(range(size))
            random.shuffle(index)
            mid1 = int(size*self.train_size)
            mid2 = mid1 + int(size*self.valid_size)
            self.train_index = index[:mid1]
            self.valid_index = index[mid1:mid2]
            self.test_index = index[mid2:]
        return True

    def get_train(self):
        # X와 y의 train set을 튜플로 리턴
        return self.X[self.train_index], self.y[self.train_index]

    def get_valid(self):
        # X와 y의 validation set을 튜플로 리턴
        return self.X[self.valid_index], self.y[self.valid_index]

    def get_test(self):
        # X와 y의 test set을 튜플로 리턴
        return self.X[self.test_index], self.y[self.test_index]
