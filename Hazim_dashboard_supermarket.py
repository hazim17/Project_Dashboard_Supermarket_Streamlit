import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data/supermarket_sales - Sheet1.csv')

st.set_page_config(page_title='Supermarket Dashboard', layout='wide')
st.title("Supermarket Sales Performance and Buyers Behavior Characteristics")


#------------ Sidebar --------------
st.sidebar.subheader("Visualization Settings")

selection_gender = st.sidebar.selectbox('Gender:',list(('Male', 'Female')))

_,line_col,_ = st.columns(3)
line_col.metric('Total Respondents', len(df))

#------------ End Sidebar --------------

#------------ 1st line --------------
st.header("Supermarket Sales Performance")
line1_col1, line1_col2, line1_col3 = st.columns((5, 5, 5))

## -- Plot 1 line 1--
# Cost of goods sold in each Branch
data1 = df.groupby(['Branch'])[['cogs', 'gross income']].sum()

fig1, ax1 = plt.subplots()
x_axis_11 = ('A', 'B', 'C')
y_axis_11 = data1['cogs']

plt.bar(x_axis_11, y_axis_11, align='center', alpha=0.5, color='red')
ax1.set_xlabel('Branch')
ax1.set_ylabel('COGS')
plt.title('Cost of goods sold per Branch')

line1_col1.write('Cost of goods sold (COGS) per Branch')
line1_col1.pyplot(fig1)
## -- end Plot 1 line 1--

## -- Plot 2 line 1--
# Gross Income and COGS in each Branch
fig2, ax2 = plt.subplots()
x_axis_12 = ('A', 'B', 'C')
y_axis_12 = data1['gross income']

plt.bar(x_axis_12, y_axis_12, align='center', alpha=0.5)
ax2.set_xlabel('Branch')
ax2.set_ylabel('Gross Income')

line1_col2.write('Gross Income per Branch')
line1_col2.pyplot(fig2)
## -- end Plot 2 line 1--


## -- Plot 3 line 1--
gmp_mean_rating = df.groupby(['Branch']).agg({'gross margin percentage': 'mean', 'Rating': 'mean'}).reset_index()

fig3,ax3 = plt.subplots()

sns.barplot(x='Branch', y='gross margin percentage', data=gmp_mean_rating, palette=['#bc8fff', '#fff88f', '#52fa74'])

line1_col3.write('Average of Gross Margin Percentage in each Branch')
line1_col3.pyplot(fig3)

## -- end Plot 3 line 1 --

#------------ END 1st line --------------

#------------ 2nd line --------------

line2_col1, line2_col2, line2_col3 = st.columns((5, 5, 1))

## -- Plot 1 line 2--
fig4,ax4 = plt.subplots()

sns.barplot(x='Branch', y='Rating', data=gmp_mean_rating, palette=['#bc8fff', '#fff88f', '#52fa74'])

line2_col1.write('Average of Rating in each Branch')
line2_col1.pyplot(fig4)

# -- end Plot 1 line 2 --

## -- Plot 2&3 line 2--
fig5,ax5 = plt.subplots()

gi_date = df.groupby(['Date', 'Branch']).agg({'gross income': sum}).reset_index()
gi_date['month'] = pd.DatetimeIndex(gi_date['Date']).month

selection_class = line2_col3.radio('Branch',['A','B','C'])
nana = gi_date[gi_date['Branch'] == selection_class][['month', 'gross income']]

sns.lineplot(x='month', y='gross income', data=nana, color='#fc58f2' )
x_ticks = np.arange(1, 4, 1)
ax5.set_xticks(x_ticks)

line2_col2.write('Gross income Jan-March in Store Branch {}'.format(selection_class))
line2_col2.pyplot(fig5)

## -- end Plot 2&3 line 2 --

#------------ END 2nd line --------------

#------------ 3rd line --------------
st.header("Buyers Behavior Characteristics")
line3_col1, line3_col2, line3_col3 = st.columns((5, 5, 5))

## -- Plot 1 line 3--
data2 = df.groupby(['Gender', 'Product line'])[['Quantity']].sum()

# convert 2d array to 1d array, Male
male_qty = data2.loc['Male'].values
# male_qty.shape #2d array
male_qty_1d = male_qty.flatten()

# convert 2d array to 1d array, Female
female_qty = data2.loc['Female'].values
# female_qty.shape #2d array
female_qty_1d = female_qty.flatten()

colors = sns.color_palette('Set2')[0:7]

labels = data2.loc['Male'].index

if selection_gender == 'Male':
    # Male
    fig6,ax6 = plt.subplots()
    # plt.figure(0)
    plt.pie(x=male_qty_1d, 
            autopct="%.1f%%", 
            explode=[0.05]*6, 
            labels=labels, 
            colors = colors,
            pctdistance=0.5)
    line3_col1.write("Type of Product that Male Buy")
    line3_col1.pyplot(fig6)
elif selection_gender == 'Female':
    # Female
    fig7,ax7 = plt.subplots()
    # plt.figure(1)
    plt.pie(x=female_qty_1d, 
            autopct="%.1f%%", 
            explode=[0.05]*6, 
            colors = colors,
            labels=labels, 
            pctdistance=0.5)
    line3_col1.write("Type of Product that Female Buy")
    line3_col1.pyplot(fig7)

## -- end Plot 1 line 3--

## -- Plot 2 line 3--
data3 = df.groupby(['Gender'])[['Total']].sum()

# convert 2d array to 1d array
gender_total = data3.values
gender_total_1d = gender_total.flatten()

fig8,ax8 = plt.subplots()

colors_pie_gender = ['tab:orange', 'tab:cyan']
labels_pie_gender = data3.index

plt.pie(x=gender_total_1d, 
        autopct="%.1f%%", 
        explode=[0.05]*2, 
        labels=labels_pie_gender,
        colors = colors_pie_gender,
        pctdistance=0.5)

line3_col2.write("Spending Money by Gender")
line3_col2.pyplot(fig8)

## -- end Plot 2 line 3--

## -- Plot 3 line 3--
payment_gender = df.groupby(['Gender', 'Payment'])[['Invoice ID']].count()

# convert 2d array to 1d array, Male
male_payment = payment_gender.loc['Male'].values
# male_payment.shape #2d array
male_payment_1d = male_payment.flatten()

# convert 2d array to 1d array, Female
female_payment = payment_gender.loc['Female'].values
# female_qty.shape #2d array
female_payment_1d = female_payment.flatten()

colors_payment = sns.color_palette('Paired')[0:3]

labels_payment = payment_gender.loc['Male'].index

if selection_gender == 'Male':
    # Male
    fig91,ax91 = plt.subplots()
    # plt.figure(0)
    plt.pie(x=male_payment_1d, 
            autopct="%.1f%%", 
            explode=[0.05]*3, 
            labels=labels_payment, 
            colors = colors_payment,
            pctdistance=0.5)
    line3_col3.write("Type of Payment that Male Use")
    line3_col3.pyplot(fig91)
elif selection_gender == 'Female':
    # Female
    fig92,ax92 = plt.subplots()
    # plt.figure(1)
    plt.pie(x=female_payment_1d, 
            autopct="%.1f%%", 
            explode=[0.05]*3, 
            colors = colors_payment,
            labels=labels_payment, 
            pctdistance=0.5)
    line3_col3.write("Type of Payment that Female Use")
    line3_col3.pyplot(fig92)
## -- end Plot 3 line 3--

#------------ END 3rd line --------------


#------------ 4th line --------------
line4_col1, line4_col2 = st.columns((5, 5))

## -- Plot 3 line 3--
# Purchase time in hour
hour = df['Time'].astype(str).str[:2]
id = df['Invoice ID']
hours = pd.DataFrame(hour)
gender = df[['Invoice ID', 'Gender']]
data_gender_time = pd.concat([gender, hours], axis=1)

# Data For male
male = data_gender_time[data_gender_time['Gender'] == 'Male']
time_male_count = male.Time.value_counts().sort_index()

# Male
fig10,ax10 = plt.subplots()
x_male = time_male_count.index
y_male = time_male_count.values
plt.bar(x=x_male,
        height=y_male,
        width=0.5,
       color='#3d6aff')
plt.xlabel("Time")
plt.ylabel("Number of Purchases")
line4_col1.write("Time of Male Buying in Supermarket")
line4_col1.pyplot(fig10)

## -- end Plot 3 line 3--

## -- Plot 4 line 3--
# Data For Female
female = data_gender_time[data_gender_time['Gender'] == 'Female']
time_female_count = female.Time.value_counts().sort_index()

fig11,ax11 = plt.subplots()
x_female = time_female_count.index
y_female = time_female_count.values
plt.bar(x=x_female,
        height=y_female,
        width=0.5,
       color='#f53172')
plt.xlabel("Time")
plt.ylabel("Number of Purchases")
line4_col2.write("Time of Female Buying in Supermarket")
line4_col2.pyplot(fig11)

## -- end Plot 4 line 3--

#------------ END 4th line --------------



