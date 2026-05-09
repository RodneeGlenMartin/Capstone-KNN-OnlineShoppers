import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('online_shoppers_intention.csv')
print(df.shape)
print(df.head())
print(df.info())
print(df['Revenue'].value_counts())
