#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from streamlit_jupyter import StreamlitPatcher, tqdm

StreamlitPatcher().jupyter()  # register streamlit with jupyter-compatible wrappers

st.set_option('deprecation.showPyplotGlobalUse', False)
# In[2]:


df_salary = pd.read_csv('data_salary.csv', index_col='Год')
df_salary = df_salary.rename(columns={'Здравоохранение и предоставление социальных услуг': 'Социальная сфера'})
df_salary['ВВП'] = df_salary['ВВП'] * 1000000


# In[3]:


st.title("Анализ зарплат в России")
# Поправка на инфляцию
for column in df_salary.columns:
   if column not in ('Инфляция', 'ВВП', 'Родившиеся', 'USD/RUB'):
    name = f'{column} с учетом инфл.'
    df_salary[name] = df_salary[column]*(1 - df_salary["Инфляция"]/100)
st.dataframe(df_salary)


# In[4]:


# Графики
col_without_infl = [col for col in df_salary.columns if ('инфл.' not in col) and (col not in ('Инфляция', 'ВВП', 'Родившиеся', 'USD/RUB'))]
df_salary[col_without_infl].plot(kind='line', figsize=(8, 4), title='Динамика номинальной заработной платы')
plt.show()
st.pyplot()

col_infl = [col for col in df_salary.columns if 'инфл.' in col]
df_salary[col_infl].plot(kind='line', figsize=(8, 4), title='Динамика реальной заработной платы')
plt.show()
st.pyplot()


# In[5]:


st.markdown("На графиках виден рост номинальной и реальной заработной платы работников как по экономике в целом, так и по отдельным отраслям")


# In[16]:


# Выбор истересующего сектора стримлит
sector = list(df_salary.columns)
sector = [i for i in sector if ('инфл.' not in i) and (i not in ('Инфляция', 'ВВП', 'Родившиеся', 'USD/RUB'))]
st.sidebar.write("Выбери интересующий сектор")
status = st.sidebar.radio('sector:', sector)


# In[15]:


# Графики с учетом инфляции
# df_salary[status].plot(kind='line', figsize=(8, 4), title=status)
status_infl = status + ' с учетом инфл.'
title = f'Aнализ фактора инфляции для сектора {status}'
df_salary[[status, status_infl]].plot(kind='line', figsize=(8, 4), title=title)
plt.show()
st.pyplot()


# In[8]:


# Рост от года к году в %
for column in df_salary.columns:
   if column not in ('Инфляция', 'ВВП', 'Родившиеся', 'USD/RUB') and ('инфл' not in column):
    name = f'{column} с учетом инфл.'
    column_name_infl = f'Рост реальной зарплаты {column}'
    df_salary[column_name_infl] = df_salary[name].pct_change()*100


# In[9]:


# График темпов роста
name = f'Рост реальной зарплаты {status}'
title = f'Процентное изменение реальных зарплат {status}'
df_salary[[name, 'Инфляция']].plot(kind='line', figsize=(8, 4), title=title)
plt.show()
st.pyplot()
st.markdown("Несмотря на рост реальных зарплат, темпы роста снизились относительно 2000-х и не всегда оказываются выше уроня инфляции")


# In[10]:


# Корреляция социальноэкономических покахателей с динамикой реальных зарплат
st.write("Рассмотрим корреляцию социальноэкономических показателей с динамикой реальных зарплат")
plt.scatter(status, 'Родившиеся',
                data=df_salary)
plt.gca().set(xlabel=status, ylabel='Родившиеся')

plt.xticks(fontsize=12); plt.yticks(fontsize=12)
title = f'{status} vs Родившиеся'
plt.title(title, fontsize=10)
plt.legend(fontsize=12)
plt.show()
st.pyplot()

plt.scatter(status, 'ВВП',
                data=df_salary)
plt.gca().set(xlabel=status, ylabel='ВВП')

plt.xticks(fontsize=12); plt.yticks(fontsize=12)
title = f'{status} vs ВВП'
plt.title(title, fontsize=10)
plt.legend(fontsize=12)
plt.show()
st.pyplot()

plt.scatter(status, 'USD/RUB',
                data=df_salary)
plt.gca().set(xlabel=status, ylabel='USD/RUB')

plt.xticks(fontsize=12); plt.yticks(fontsize=12)
title = f'{status} vs USD/RUB'
plt.title(title, fontsize=10)
plt.legend(fontsize=12)
plt.show()
st.pyplot()
st.markdown("Можно заметить сильную положительную линейную зависимость реальных зарплат с ВВП, также существует положительная зависимость зарплат и среднего курса доллара к рублю. До определенного уровня зарплат наблюдается рост количества родившихся, но затем следует снижение, стоит учитывать влияние большого количества иных факторов на демографические показатели.")


# In[11]:


# Тепловая карта
plt.figure(figsize=(12,10), dpi= 80)
col = [col for col in df_salary.columns if 'Рост' not in col]
sns.heatmap(df_salary[col].corr(), xticklabels=df_salary[col].corr().columns, yticklabels=df_salary[col].corr().columns, cmap='RdYlGn', center=0, annot=True)
plt.title('Корреляции', fontsize=22)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.show()
st.pyplot()

