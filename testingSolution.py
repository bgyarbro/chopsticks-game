import numpy as np
import pandas as pd

col_names = ['P1_left', 'P1_right', 'P2_left', 'P2_right']

hands = pd.DataFrame(np.asarray([[1,1,1,1],
                                 [1,1,1,1],
                                 [1,1,2,1],
                                 [2,1,2,1]]), columns = col_names)

#print(hands)

#print("smaller")
#print(np.unique(hands, axis=1))

#print(df)

#print(df.drop_duplicates)



#df = pd.DataFrame(columns = col_names)


#df.append(hands)
#print("after append")

gs_Round_N_End = [[0,1,0,0],
                  [0,2,0,0],
                  [0,3,0,0],
                  [0,4,0,0],
                  [1,0,0,0],
                  [1,1,0,0],
                  [1,2,0,0],
                  [1,3,0,0],
                  [1,4,0,0],
                  [2,0,0,0],
                  [2,1,0,0],
                  [2,2,0,0],
                  [2,3,0,0],
                  [2,4,0,0],
                  [3,0,0,0],
                  [3,1,0,0],
                  [3,2,0,0],
                  [3,3,0,0],
                  [3,4,0,0],
                  [4,0,0,0],
                  [4,1,0,0],
                  [4,2,0,0],
                  [4,3,0,0],
                  [4,4,0,0]]


df = pd.DataFrame(gs_Round_N_End, columns = ['p1l', 'p1r', 'p2l', 'p2r'])

print(df)

df_np = np.asarray(df)

print(df_np)
