import os
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt 
from tabulate import tabulate

mpl.rcParams.update({
    'font.size'           : 20.0,
    'axes.titlesize'      : 'large',
    'axes.labelsize'      : 'medium',
    'xtick.labelsize'     : 'medium',
    'ytick.labelsize'     : 'medium',
    'legend.fontsize'     : 'large',
})
data_dir = '../data/'
img_dir = '../fancy_images/'
cities_500_csv = data_dir +'500_Cities.csv'
acs_merged_csv = data_dir + 'Clean_data_w_state.csv'

if not os.path.isdir(img_dir):
    os.makedirs(img_dir)

df1 = pd.read_csv(cities_500_csv)
df2 = pd.read_csv(acs_merged_csv)
outcome_vars = ['SLEEP', 'CSMOKING', 'BINGE']
df1_sub = df1[df1['MeasureId'].isin(outcome_vars)]
ax = sns.violinplot(x="MeasureId", y="Data_Value", data=df1_sub)
plt.title('Outcome Variables')
plt.tight_layout()
# plt.show()
plt.savefig(self.img_dir+'Outcome_Violin.png')
plt.close()
