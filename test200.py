import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

#possible features:
#error handling
#conditional rendering/disabling/enabling certain buttons
#clear functionality or reset to default

#df=pd.read_csv(r"\\fnbmcorp\share\Risk\Enterprise Risk\PortfolioManagement\VintageComparisonGraphs\Data\Data2.csv")
#df.to_parquet(r"\\fnbmcorp\share\Risk\Enterprise Risk\PortfolioManagement\VintageComparisonGraphs\Data\Data2.parquet")
#df.to_hdf(r"\\fnbmcorp\share\Risk\Enterprise Risk\PortfolioManagement\VintageComparisonGraphs\Data\Data2.h5", key='data', mode='w')

#df=pd.read_parquet(r"\\fnbmcorp\share\Risk\Enterprise Risk\PortfolioManagement\VintageComparisonGraphs\Data\Data2.parquet")
df=pd.read_csv(r"Data_Test.csv")

#df = pd.read_hdf(r"\\fnbmcorp\share\Risk\Enterprise Risk\PortfolioManagement\VintageComparisonGraphs\Data\Data2.h5", "data")

#Replace any NaN values with a string "None"
#Graph won't render otherwise
dfFixNone = df.replace(np.nan, 'None')
df= dfFixNone

clist = df['Vintage'].unique()
clist1 = df['FirstSecond'].unique()
clist2 = df['Branding']. unique()
clist3 = df['Channel'].unique()
clist4 = df['Source'].unique()
clist5 = df['Association'].unique()
clist6 = df['AnnualFeeGroup'].unique()
clist7 = df['OriginalCreditLineRange'].unique()

# initialize default dataframe to hold ALL csv data
#if 'df_default' not in st.session_state:
    #st.session_state['df_default'] = df

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

def main():
    if submit:
        # filter from original df using selected values
        # create a new filtered df from the entire df
        df_new = df.loc[(df['Vintage'] == selected)
                        & (df['FirstSecond'] == FirstSecond)
                        & (df['Branding'] == Branding)
                        & (df['Channel'] == Channel)
                        & (df['Source'] == Source)
                        & (df['Association'] == Association)
                        & (df['AnnualFeeGroup'] == AnnualFeeGroup)
                        & (df['OriginalCreditLineRange'] == OriginalCreditLineRange)]
        # store this new df into df made earlier
        st.session_state['blank_df'] = pd.concat(
            [st.session_state['blank_df'], df_new], axis=0)

def add_to_main():
    if add:
        # create a new filtered df from the entire df
        df_add = df.loc[(df['Vintage'] == selected)
                        & (df['FirstSecond'] == FirstSecond)
                        & (df['Branding'] == Branding)
                        & (df['Channel'] == Channel)
                        & (df['Source'] == Source)
                        & (df['Association'] == Association)
                        & (df['AnnualFeeGroup'] == AnnualFeeGroup)
                        & (df['OriginalCreditLineRange'] == OriginalCreditLineRange)]
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

st.header("Vintage Comparison")
options = st.multiselect("Select vintages:", clist, key="vintages_selected")
with st.form('my_form'):
    with st.sidebar:
        st.header('Filters')
        selected = st.selectbox("Selected Vintages:",
                                options, key="current_vintage")
        FirstSecond = st.selectbox("FirstSecond:", clist1)
        Branding = st.selectbox("Branding", clist2)
        Channel = st.selectbox("Channel", clist3)
        Source = st.selectbox("Source", clist4)
        Association = st.selectbox("Association", clist5)
        AnnualFeeGroup = st.selectbox("AnnualFeeGroup", clist6)
        OriginalCreditLineRange = st.selectbox(
            "OriginalCreditLineRange", clist7)
        submit = st.form_submit_button('Submit')
        add = st.form_submit_button('Add') 

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    add_to_main()
    
#ENTIRE DF AND ALL PLOT LINES ON LOAD, this is default case
#if st.session_state['blank_df'].empty == True:
    #st.write(df)
    #fig1a = px.line(df.melt(id_vars="Vintage"), x=df['MonthsOnBooks'], y=df['ActiveAccountIndicator'], color=df['Vintage'],
                    #markers=True, title='Active Accounts', labels={'y': 'Active Accounts', 'x': 'Months on Book', "color": "Vintage"})
    #st.plotly_chart(fig1a)
    #fig1b = px.line(df.melt(id_vars="Vintage"), x=df['MonthsOnBooks'], y=df['CumlROAAnnualized'], color=df['Vintage'],
                    #markers=True, title='CumlROAAnnualized', labels={'y': 'ROAAnnualized', 'x': 'Months on Book', "color": "Vintage"})
    #fig1b.update_layout(yaxis_ticksuffix=".3%")
    #st.plotly_chart(fig1b)
    #fig1c = px.line(df.melt(id_vars="Vintage"), x=df['MonthsOnBooks'], y=df['CumlPreTaxIncome'], color=df['Vintage'],
                    #markers=True, title='CumlPreTaxIncome', labels={'y': 'PreTaxIncome', 'x': 'Months on Book', "color": "Vintage"})
    #st.plotly_chart(fig1c)
    #fig1d = #px.line(df.melt(id_vars="Vintage"), x=df['MonthsOnBooks'], y=df['EndingReceivable'], color=df['Vintage'],
                    #markers=True, title='EndingReceivable', labels={'y': 'EndingReceivable', 'x': 'Months on Book', "color": "Vintage"})
    #st.plotly_chart(fig1d)
#THE FIRST FILTERED DF WILL DISPLAY, this case happens on first click of "Display Vintage"
if st.session_state['blank_df'].empty == False and st.session_state['isDfAdded'] == False:
    st.dataframe(st.session_state['blank_df'])
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
#THE ADDED VINTAGES WILL DISPLAY, this case happens after n clicks of "Add a Vintage"
elif st.session_state['added_df'].empty == False and st.session_state['isDfAdded'] == True:
    st.dataframe(st.session_state['added_df'])
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

