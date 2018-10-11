import os
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt 
from tabulate import tabulate


def to_markdown(df, round_places=3):
    """Returns a markdown, rounded representation of a dataframe"""
    print(tabulate(df.round(round_places), headers='keys', tablefmt='pipe', showindex=False))

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
plt.savefig(img_dir+'Outcome_Violin.png')
plt.close()

ax = sns.violinplot(x=df2["Med_age"], orient='v')
plt.title('Median Age')
ax.set(xlabel='', ylabel='')
plt.tight_layout()
# plt.show()
plt.savefig(img_dir+'Med_Age_Violin.png')
plt.close()


state_vars = [ x for x in df2.columns if x.startswith('State')]
states = df2[state_vars]
states['State_Abbr_CO']=states[state_vars].apply(lambda row: 1 if row.sum()==0 else 0, axis=1)
states_sum = states.sum()

ax = sns.violinplot(x=states_sum, orient='v')
plt.title('Count of State Tracts')
ax.set(xlabel='', ylabel='')
plt.tight_layout()
# plt.show()
plt.savefig(img_dir+'State_Count_Violin.png')
plt.close()

vois = ['Percent_female', 'Edu_less_than_hs_or_GED',
       'Income_to_pov_rat_lt_1_5', 'Commute_time_lt_30',
       'Work_depart_before_8am', 'Percent_insured']
mpl.rcParams.update({
    'font.size'           : 20.0,
    'axes.titlesize'      : 'large',
    'axes.labelsize'      : 'medium',
    'xtick.labelsize'     : 'small',
    'ytick.labelsize'     : 'medium',
    'legend.fontsize'     : 'large',
})

ax = sns.violinplot(data=df2[vois])
plt.title('Demographic Percentages')
ax.set(ylabel='%')
xticks=['Female', 'Edu < HS','IPR < 1.5','Commute < 30', 'Work before 8', 'Insured']
ax.set_xticklabels(xticks, rotation=30)
# ax.set_xticklabels(ax.get_xticklabels(),rotation=30)
plt.tight_layout()
# plt.show()
plt.savefig(img_dir+'Demographics_Violin.png')
plt.close()

#### TABLE FOR SAMPLE SIZE #######

'''
# BD 
|   Initial |   Final |   Dropped |   Dropped % |
|----------:|--------:|----------:|------------:|
|     28004 |   27141 |       863 |       3.082 |

Directory exists: /home/danny/Desktop/galvanize/500_cities/src/../images_smoking/
Table for missing data
|   Initial |   Final |   Dropped |   Dropped % |
|----------:|--------:|----------:|------------:|
|     28004 |   27080 |       924 |         3.3 |

|   Initial |   Final |   Dropped |   Dropped % |
|----------:|--------:|----------:|------------:|
|     28004 |   27137 |       867 |       3.096 |


'''
data = {'Initial': [28004, 28004, 28004],
                'Final' : [27141, 27080, 27137]}
df = pd.DataFrame.from_dict(data)
df['Dropped'] = df.Initial-df.Final
df['Drop %'] = df.Dropped/df.Initial*100
df = df.T 
df.columns = ['Binge Drinking', 'Smoking', 'Sleep < 7hrs']
to_markdown(df)


