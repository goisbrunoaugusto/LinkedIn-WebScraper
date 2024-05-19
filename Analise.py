import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
plt.autoscale()
pd.set_option('display.max_columns', 3)
plt.rcParams.update({'font.size': 6})

df = pd.read_csv('job_links.csv', encoding='latin-1')

df['Job Title'].value_counts().plot(kind='pie')
#df['Job Location'].value_counts().plot(kind='pie')
plt.show()
