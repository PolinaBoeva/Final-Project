#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
from streamlit_jupyter import StreamlitPatcher, tqdm


st.set_option('deprecation.showPyplotGlobalUse', False)
# In[2]:


df_salary = pd.read_csv('data/data_salary.csv', index_col='Год')
df_salary = df_salary.rename(columns={'Здравоохранение и предоставление социальных услуг': 'Социальная сфера'})
df_salary['ВВП'] = df_salary['ВВП'] * 1000000

df_salary["ИПЦ"] = 100 + df_salary['Инфляция'].shift(1)
df_salary["ИПЦ"][[2000]] = 100
cpi_array = df_salary["ИПЦ"].to_numpy()
cpi_base = cpi_array[0]
cpi_values = []
for i in range(len(cpi_array)):
    cpi_2000_price = cpi_base*np.prod(cpi_array[1:i+1])/100**(i)
    cpi_values.append(cpi_2000_price)
df_salary['ИПЦ баз'] = cpi_values

st.title("Анализ зарплат в России по секторам")

# Поправка на инфляцию
# Зарплата в ценах 2000 года

st.title("Анализ зарплат в России")
for column in df_salary.columns:
   if column not in ('Инфляция', 'ВВП', 'Родившиеся', 'USD/RUB'):
    name = f'{column} с учетом инфл.'
    name_s = f'ИНЗ {column}'
    name_r = f'ИPЗ {column}'
    df_salary[name_s] = df_salary[column] * 100 / df_salary[column][[2000]]
    df_salary[name_r] = df_salary[name_s] / df_salary['ИПЦ баз']
    df_salary[name] = df_salary[column][[2000]]*df_salary[name_r]

st.dataframe(df_salary)


# In[4]:


# Графики
col_without_infl = [col for col in df_salary.columns if ('инфл.' not in col) and (col not in ('Инфляция', 'ВВП', 'Родившиеся', 'USD/RUB'))]
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(df_salary[col_without_infl])
ax.legend(col_without_infl)
ax.set_title('Динамика номинальной заработной платы')
ax.set_xlabel('Год')
ax.set_ylabel('Номинальная зп')
x_values = range(2000, 2023, 5)
ax.set_xticks(x_values)
plt.gca().spines[['top', 'right']].set_visible(False)
st.pyplot(fig)

col_infl = [col for col in df_salary.columns if 'инфл.' in col]
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(df_salary[col_infl])
ax.legend(col_infl)
ax.set_title('Динамика реальной заработной платы')
ax.set_xlabel('Год')
ax.set_ylabel('Реальная зп')
x_values = range(2000, 2023, 5)
ax.set_xticks(x_values)
plt.gca().spines[['top', 'right']].set_visible(False)
st.pyplot(fig)


# In[5]:


st.markdown("На графиках виден рост номинальной и реальной заработной платы (номинальная с учетом уровня инфляции) работников как по экономике в целом, так и по отдельным отраслям")


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
title = f'Номинальная и реальная заработная плата {status}'
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(df_salary[[status, status_infl]])
ax.legend([status, status_infl])
ax.set_title(title)
ax.set_xlabel('Год')
ax.set_ylabel('Заработная плата')
x_values = range(2000, 2023, 5)
ax.set_xticks(x_values)
plt.gca().spines[['top', 'right']].set_visible(False)
st.pyplot(fig)



# In[8]:


# Рост от года к году в %
for column in df_salary.columns:
   if column not in ('Инфляция', 'ВВП', 'Родившиеся', 'USD/RUB') and ('инфл' not in column):
    name = f'{column} с учетом инфл.'
    column_name_infl = f'Изменение реальной зарплаты {column}'
    df_salary[column_name_infl] = df_salary[name].pct_change()*100


# In[9]:


# График темпов роста
name = f'Изменение реальной зарплаты {status}'
title = f'Процентное изменение реальных зарплат {status}'
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(df_salary[[name, 'Инфляция']])
ax.legend([name, 'Инфляция'])
ax.set_title(title)
ax.set_xlabel('Год')
ax.set_ylabel('Проценты')
x_values = range(2000, 2023, 5)
ax.set_xticks(x_values)
plt.gca().spines[['top', 'right']].set_visible(False)
st.pyplot(fig)

st.markdown("Несмотря на рост реальных зарплат, темпы роста снизились относительно 2000-х и не всегда оказываются выше уроня инфляции")


# In[10]:


# Корреляция социальноэкономических показателей с динамикой реальных зарплат
st.write("Рассмотрим корреляцию социальноэкономических показателей с динамикой реальных зарплат")
fig, ax = plt.subplots(figsize=(8, 4))
title = f'{status} vs Родившиеся'
ax.scatter(status, 'Родившиеся',
                data=df_salary)
plt.gca().set(xlabel=status, ylabel='Родившиеся')
plt.xticks(fontsize=12); plt.yticks(fontsize=12)
ax.set_title(title, fontsize=10)
ax.legend(fontsize=12)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(8, 4))
title = f'{status} vs ВВП'
ax.scatter(status, 'ВВП',
                data=df_salary)
plt.gca().set(xlabel=status, ylabel='ВВП')
plt.xticks(fontsize=12); plt.yticks(fontsize=12)
ax.set_title(title, fontsize=10)
ax.legend(fontsize=12)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(8, 4))
title = f'{status} vs USD/RUB'
ax.scatter(status, 'USD/RUB',
                data=df_salary)
plt.gca().set(xlabel=status, ylabel='USD/RUB')
plt.xticks(fontsize=12); plt.yticks(fontsize=12)
ax.set_title(title, fontsize=10)
ax.legend(fontsize=12)
st.pyplot(fig)

st.markdown("Можно заметить сильную положительную линейную зависимость реальных зарплат с ВВП, также существует положительная зависимость зарплат и среднего курса доллара к рублю. До определенного уровня зарплат наблюдается рост количества родившихся, но затем следует снижение, стоит учитывать влияние большого количества иных факторов на демографические показатели.")


# In[11]:


# Тепловая карта
plt.figure(figsize=(12,10), dpi= 80)
col = [col for col in df_salary.columns if 'Рост' not in col]
sns.heatmap(df_salary[col].corr(), xticklabels=df_salary[col].corr().columns, yticklabels=df_salary[col].corr().columns, cmap='RdYlGn', center=0, annot=True)
plt.title('Корреляции', fontsize=22)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
st.pyplot()
