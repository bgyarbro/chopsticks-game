import numpy as np
import pandas as pd

endStates = [[0,0,1,0,0],
             [0,0,2,0,0],
             [1,1,1,1,1]]

endStates = np.asarray(endStates)

print(endStates[endStates[:,0] == 0])
