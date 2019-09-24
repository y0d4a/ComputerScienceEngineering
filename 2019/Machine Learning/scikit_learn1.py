import numpy as np
import scipy
import sklearn
from sklearn import datasets

iris = datasets.load_iris()
X, y = iris.data, iris.target
print('Size of dta : %s ', (X.shape, ))
print('Target value : %s', % np.unique(y))
