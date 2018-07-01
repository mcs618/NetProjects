# https://stackoverflow.com/questions/25292568/converting-a-dictionary-with-lists-for-values-into-a-dataframe

# https://stackoverflow.com/questions/37790429/seaborn-heatmap-using-pandas-dataframe

# https://stackoverflow.com/questions/12286607/python-making-heatmap-from-dataframe

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


Cols = ['key1', 'key2', 'key3', 'key4', 'key5']
Index = ['A', 'B', 'C', 'D']

testdict = {
    "key1": [21, 2, 3, 4],
    "key2": [5, 6, 7, 8],
    "key3": [9, 10, 11, 12],
    "key4": [13, 14, 15, 16],
    "key5": [17, 18, 19, 20]
}

df = pd.DataFrame(testdict, index=Index, columns=Cols)
df = df.transpose()

sns.heatmap(df, cmap='RdYlGn_r', linewidths=0.5, annot=True)

plt.show()

print(df)
