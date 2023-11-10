import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from io import StringIO

css='''
<style>
    .stButton > button {
       width: 100%;
       background-color: #0A5EC0;
       color: white;
         border: 1px solid #fff;
        border-radius: 20px;
    }
    .stButton > button:hover {
       background-color: #0E4594;
       color: white;
    }
    [data-testid=stDecoration]{
        background-image: linear-gradient(90deg, rgb(26, 117, 209), rgb(206, 230, 255));
    }
  [data-testid=stForm]{
        border-color:#f0f2f6;
    }
</style>
'''
st.markdown(css, unsafe_allow_html=True)

df=pd.read_parquet(r"Data3 - Copy.parquet")

#Replace any NaN values with a string "None"
#Graph won't render otherwise
dfFixNone = df.replace(np.nan, 'None')
df= dfFixNone

col4, col5= st.columns([0.7, 0.3], gap="Medium")
#Unique list for Vintage
clist = df['Vintage'].unique()

col4.header("Vintage Comparison")
col4.write("select a vintage from the sidebar and click add")

with st.sidebar:
        st.header('Filters')
        selected_vintage = st.selectbox("Select Vintage:", clist, key="selected_vintage")
         #filter df based on selected vintage
        
        filtered_df = df[df['Vintage'] == selected_vintage]

        clist1 = filtered_df['FirstSecond'].unique()
        selected_firstsecond = st.selectbox("Select FirstSecond:", clist1, key="selected_firstsecond")
        filtered_df_firstsecond = filtered_df[filtered_df['FirstSecond'] == selected_firstsecond]

        clist2 = filtered_df_firstsecond['Branding'].unique()
        selected_branding = st.selectbox("Select Branding:", clist2, key="selected_branding")
        filtered_df_branding = filtered_df_firstsecond[filtered_df_firstsecond['Branding'] == selected_branding]

        clist3 = filtered_df_branding['Channel'].unique()
        selected_channel = st.selectbox("Select Channel:", clist3, key="selected_channel")
        filtered_df_channel = filtered_df_branding[filtered_df_branding['Channel'] == selected_channel]

        clist4 = filtered_df_channel ['Source'].unique()
        selected_source = st.selectbox("Select Source:", clist4, key="selected_source")
        filtered_df_source = filtered_df_channel [filtered_df_channel ['Source'] == selected_source]

        clist5 = filtered_df_source['Association'].unique()
        selected_association = st.selectbox("Select Association:", clist5, key="selected_association")
        filtered_df_association = filtered_df_source[filtered_df_source['Association'] == selected_association]

        clist6 = filtered_df_association['AnnualFeeGroup'].unique()
        selected_annualfeegroup = st.selectbox("Select AnnualFeeGroup:", clist6, key="selected_annualfeegroup")
        filtered_df_annualfeegroup = filtered_df_association[filtered_df_association['AnnualFeeGroup'] == selected_annualfeegroup]
            
        clist7 = filtered_df_annualfeegroup['OriginalCreditLineRange'].unique()
        selected_originalcreditlinerange = st.selectbox("Select OriginalCreditLineRange:", clist7, key="selected_originalcreditlinerange")
        filtered_df_originalcreditlinerange = filtered_df_annualfeegroup[filtered_df_annualfeegroup['OriginalCreditLineRange'] == selected_originalcreditlinerange]
        with st.form('my_form'):
            col1, col2, col3 = st.columns([1,2,1])
            #submit = st.form_submit_button('Submit')
            with col1:
                add = st.form_submit_button('Add')
            with col2:
                clear = st.form_submit_button('Clear All')


# initialize blank dataframe to hold First df created from user filters
if 'blank_df' not in st.session_state:
    st.session_state['blank_df'] = pd.DataFrame(columns=[
        "Vintage", "FirstSecond", 'Branding', 'Channel', 'Source',
        'Association', 'AnnualFeeGroup', "OriginalCreditLineRange", "MonthsOnBooks", "NewAccountIndicator",
        "ActiveAccountIndicator", "PreTaxIncome", "EndingReceivable", "CumlNewAccountIndicator", "CumlActiveAccountIndicator",
        "CumlPreTaxIncome", "CumlEndingReceivable", "AverageActives", "AverageReceivable", "CumlROA", "CumlROAAnnualized"])

# initialize dataframe to be added to the main dataframe
if "added_df" not in st.session_state:
    st.session_state['added_df'] = pd.DataFrame(columns=[
        "Vintage", "FirstSecond", 'Branding', 'Channel', 'Source',
        'Association', 'AnnualFeeGroup', "OriginalCreditLineRange", "MonthsOnBooks", "NewAccountIndicator",
        "ActiveAccountIndicator", "PreTaxIncome", "EndingReceivable", "CumlNewAccountIndicator", "CumlActiveAccountIndicator",
        "CumlPreTaxIncome", "CumlEndingReceivable", "AverageActives", "AverageReceivable", "CumlROA", "CumlROAAnnualized"])

#initialize boolean for adding a new vintage
#True - the user wants to add another vintage
#False - the user has not yet added another vintage
if "isDfAdded" not in st.session_state:
    st.session_state['isDfAdded'] = False

if 'add_counter' not in st.session_state:
     st.session_state['add_counter'] = 1

if 'selected_vintages_list' not in st.session_state:
    st.session_state.selected_vintages_list = []


def add_to_main():
    if add:
        # create a new filtered df from the entire df
        df_add = df.loc[(df['Vintage'] == selected_vintage)
                        & (df['FirstSecond'] == selected_firstsecond)
                        & (df['Branding'] == selected_branding)
                        & (df['Channel'] == selected_channel)
                        & (df['Source'] == selected_source)
                        & (df['Association'] == selected_association)
                        & (df['AnnualFeeGroup'] == selected_annualfeegroup)
                        & (df['OriginalCreditLineRange'] == selected_originalcreditlinerange)]
        unique_id =f"{selected_vintage} {st.session_state['add_counter']}" 
        st.session_state['add_counter'] += 1
        df_add['Vintage'] = unique_id

        st.session_state.selected_vintages_list.append(unique_id)

        if 'add_counter' not in st.session_state:
            st.session_state['add_counter'] = 1
        #IF THE ADDED DF IS EMPTY
        #User has not yet added another dataframe to the initial dataframe, this runs if the Add button is hit for the First time
        if st.session_state['added_df'].empty == True:
            st.session_state['added_df'] = pd.concat(
                [st.session_state['blank_df'], df_add], axis=0)
        #IF THE ADDED DF IS NOT EMPTY
        #User has added a df before, just take the previous df and concat with new one
        elif st.session_state['added_df'].empty == False:
            st.session_state['added_df'] = pd.concat(
                [st.session_state['added_df'], df_add], axis=0)
        st.session_state['isDfAdded'] = True

def remove_selected_vintage(vintage_to_remove):
   
     if f"{vintage_to_remove}" in st.session_state['added_df']['Vintage'].values:
          df = st.session_state['added_df'].drop(st.session_state['added_df'][st.session_state['added_df']['Vintage'] ==  f"{vintage_to_remove}"].index)
        #   st.session_state['added_df'] = st.session_state['added_df'][st.session_state['added_df']['Vintage'] != vintage_to_remove]
          st.session_state['added_df'] = df
          st.session_state['isDfAdded'] = not st.session_state['added_df'].empty
          st.session_state.selected_vintages_list.remove(vintage_to_remove)
          if st.session_state['added_df'].empty:
               st.session_state['isDfAdded'] = False
          st.experimental_rerun()
          

def clear_from_main():
        if clear:
            st.session_state.selected_vintages_list.clear()
            st.session_state['add_counter'] = 1
            df_clear = df.loc[(df['Vintage'] == None)
                                    & (df['FirstSecond'] == None)
                                    & (df['Branding'] == None)
                                    & (df['Channel'] == None)
                                    & (df['Source'] == None)
                                    & (df['Association'] == None)
                                    & (df['AnnualFeeGroup'] == None)
                                    & (df['OriginalCreditLineRange'] == None)]
            st.session_state['added_df'] = pd.concat([st.session_state['blank_df'], df_clear], axis=0)


if __name__ == "__main__":
    add_to_main()
    clear_from_main()



for i, vintage in enumerate(st.session_state.selected_vintages_list):
     if col5.button(f"Remove {vintage}", key=f"remove_{i}"):
        #st.session_state.selected_vintages_list.pop(i)
        remove_selected_vintage(vintage)


#THE FIRST FILTERED DF WILL DISPLAY, this case happens on first click of "Display Vintage"
if st.session_state['blank_df'].empty == False and st.session_state['isDfAdded'] == False:
        
        fig2a = px.line(st.session_state['blank_df'].melt(id_vars="Vintage"), x=st.session_state['blank_df']['MonthsOnBooks'], y=st.session_state['blank_df']['ActiveAccountIndicator'],
                        color=st.session_state['blank_df']['Vintage'], markers=True, title='Active Accounts', labels={'y': 'Active Accounts', 'x': 'Months on Book', "color": "Vintage"})
        st.plotly_chart(fig2a)
        fig2b = px.line(st.session_state['blank_df'].melt(id_vars="Vintage"), x=st.session_state['blank_df']['MonthsOnBooks'], y=st.session_state['blank_df']['CumlROAAnnualized'],
                        color=st.session_state['blank_df']['Vintage'], markers=True, title='CumlROAAnnualized', labels={'y': 'ROAAnnualized', 'x': 'Months on Book', "color": "Vintage"})
        fig2b.update_layout(yaxis_ticksuffix=".3%")
        st.plotly_chart(fig2b)
        fig2c = px.line(st.session_state['blank_df'].melt(id_vars="Vintage"), x=st.session_state['blank_df']['MonthsOnBooks'], y=st.session_state['blank_df']['CumlPreTaxIncome'],
                        color=st.session_state['blank_df']['Vintage'], markers=True, title='CumlPreTaxIncome', labels={'y': 'PreTaxIncome', 'x': 'Months on Book', "color": "Vintage"})
        st.plotly_chart(fig2c)
        fig2d = px.line(st.session_state['blank_df'].melt(id_vars="Vintage"), x=st.session_state['blank_df']['MonthsOnBooks'], y=st.session_state['blank_df']['EndingReceivable'],
                        color=st.session_state['blank_df']['Vintage'], markers=True, title='EndingReceivable', labels={'y': 'EndingReceivable', 'x': 'Months on Book', "color": "Vintage"})
        st.plotly_chart(fig2d)
        st.dataframe(st.session_state['blank_df'])
#THE ADDED VINTAGES WILL DISPLAY, this case happens after n clicks of "Add a Vintage"
elif st.session_state['added_df'].empty == False and st.session_state['isDfAdded'] == True:
        
        fig3a = px.line(st.session_state['added_df'].melt(id_vars="Vintage"), x=st.session_state['added_df']['MonthsOnBooks'], y=st.session_state['added_df']['ActiveAccountIndicator'],
                        color=st.session_state['added_df']['Vintage'], markers=True, title='Active Accounts', labels={'y': 'Active Accounts', 'x': 'Months on Book', "color": "Vintage"})
        st.plotly_chart(fig3a)
        fig3b = px.line(st.session_state['added_df'].melt(id_vars="Vintage"), x=st.session_state['added_df']['MonthsOnBooks'], y=st.session_state['added_df']['CumlROAAnnualized'],
                        color=st.session_state['added_df']['Vintage'], markers=True, title='CumlROAAnnualized', labels={'y': 'ROAAnnualized', 'x': 'Months on Book', "color": "Vintage"})
        fig3b.update_layout(yaxis_ticksuffix=".3%")
        st.plotly_chart(fig3b)
        fig3c = px.line(st.session_state['added_df'].melt(id_vars="Vintage"), x=st.session_state['added_df']['MonthsOnBooks'], y=st.session_state['added_df']['CumlPreTaxIncome'],
                        color=st.session_state['added_df']['Vintage'], markers=True, title='CumlPreTaxIncome', labels={'y': 'PreTaxIncome', 'x': 'Months on Book', "color": "Vintage"})
        st.plotly_chart(fig3c)
        fig3d = px.line(st.session_state['added_df'].melt(id_vars="Vintage"), x=st.session_state['added_df']['MonthsOnBooks'], y=st.session_state['added_df']['EndingReceivable'],
                        color=st.session_state['added_df']['Vintage'], markers=True, title='EndingReceivable', labels={'y': 'EndingReceivable', 'x': 'Months on Book', "color": "Vintage"})
        st.plotly_chart(fig3d)
        st.dataframe(st.session_state['added_df'])
    
def convert_df_to_csv(df):
    output = StringIO()
    df.to_csv(output, index=False)
    return output.getvalue()

if not st.session_state['added_df'].empty:
        csv = convert_df_to_csv(st.session_state['added_df'])
        st.download_button(
             label="Download data as CSV",
             data=csv,
             file_name='vintage_data.csv',
                     mime='text/csv',
        )





