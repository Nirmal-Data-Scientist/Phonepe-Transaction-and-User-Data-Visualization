import streamlit as st
import seaborn as sns
import pandas as pd
import plotly.express as px


st.set_page_config(page_title = 'Comparitive Analysis', layout = 'wide', page_icon = 'Related Images and Videos/Logo.png')
st.title(':blue[Comparitive Analysis]')



# Define the state groups
state_groups = {
    'Northern Region': ['Jammu and Kashmir', 'Himachal Pradesh', 'Punjab', 'Chandigarh', 'Uttarakhand', 'Ladakh', 'Delhi', 'Haryana'],
    'Central Region': ['Uttar Pradesh', 'Madhya Pradesh', 'Chhattisgarh'],
    'Western Region': ['Rajasthan', 'Gujarat',  'Dadra and Nagar Haveli and Daman and Diu', 'Maharashtra'],
    'Eastern Region': ['Bihar', 'Jharkhand', 'Odisha', 'West Bengal', 'Sikkim'],
    'Southern Region': ['Andhra Pradesh', 'Telangana', 'Karnataka', 'Kerala', 'Tamil Nadu', 'Puducherry', 'Goa', 'Lakshadweep', 'Andaman and Nicobar Islands'],
    'North-Eastern Region': ['Assam', 'Meghalaya', 'Manipur', 'Nagaland', 'Tripura', 'Arunachal Pradesh', 'Mizoram']
}

trans_df = st.session_state['agg_trans_df']
user_df = st.session_state["agg_user_df"]

# Create a new column 'Region' in the trans_df and user_df based on the state groups
trans_df['Region'] = trans_df['Region'] = trans_df['State'].apply(lambda x: [k for k, v in state_groups.items() if x in v][0])
trans_df["Transaction_amount(B)"] = trans_df["Transaction_amount"] / 1e9
year_order = sorted(trans_df["Year"].unique())
trans_df["Year"] = pd.Categorical(trans_df["Year"], categories=year_order, ordered=True)


user_df['Region'] = trans_df['Region'] = user_df['State'].apply(lambda x: [k for k, v in state_groups.items() if x in v][0])



fig1 = sns.catplot(x="Year", y="Transaction_amount", col="Region", data=trans_df, kind="bar", errorbar=None, height=5, aspect=1.5, col_wrap=2, sharex=False)

for ax in fig1.axes.flat:
    ax.set_yticklabels(['₹. {:,.0f}B'.format(y/1e9) for y in ax.get_yticks()])

sns.set_theme(rc={'xtick.labelsize':10,'ytick.labelsize':10,'axes.labelsize':14})
sns.set_style("white")
st.pyplot(fig1)


transaction_types = trans_df['Transaction_type'].unique()

st.subheader('Transaction Breakdown')

# Allow user to select state, year, and quarter
col1, col2, col3 = st.columns([5, 3, 1])

selected_states = col1.multiselect("Select State(s)", st.session_state['states'], key='selected_states')
year1 = col2.selectbox("Year", st.session_state['years'], key='year1')
quarter_options = ["All"] + list(st.session_state['quarters'])
quarter1 = col3.selectbox("Quarter", quarter_options, key='quarter1')

if quarter1 != 'All':
    suffix1 = "st" if quarter1 == 1 else "nd" if quarter1 == 2 else "rd" if quarter1 == 3 else "th"

trans_df = st.session_state["agg_trans_df"]



trans_df = trans_df[(trans_df["Year"] == year1)]

if quarter1 != "All":
    trans_df = trans_df[(trans_df["Quarter"] == quarter1)]

placeholder = st.empty()

if selected_states:
    trans_df = trans_df[trans_df["State"].isin(selected_states)]
    trans_df = trans_df.sort_values("Transaction_count", ascending=False)

    fig1 = px.bar(
                trans_df, x="Transaction_type", y="Transaction_count", 
                color="State",
                color_discrete_sequence=px.colors.qualitative.Plotly,
                barmode='group',
                title=f"Transaction details for {selected_states if selected_states else 'All States'} in the {quarter1}{suffix1 if quarter1 != 'All' else ''} quarter of {year1}",
                labels=dict(Transaction_count='Transaction Count', Transaction_type='Transaction Type')
                )

    fig1.update_layout(
        showlegend=False, 
        title={
            'x': 0.5,
            'xanchor': 'center',
            'y': 0.9,
            'yanchor': 'top'
        }
    )

    fig1.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
    fig1.update_layout( width=850, height=550)
    st.plotly_chart(fig1)
else:
    placeholder.info("Please select at least one state to display the plot.")



# Allow user to select state and transaction type
col4, col5 = st.columns([4, 4])

selected_state2 = col4.selectbox("State", st.session_state['states'], key='selected_state2')
selected_type = col5.selectbox("Transaction Type", transaction_types, key='selected_type')

trans_df2 = st.session_state["agg_trans_df"]
trans_df2 = trans_df2[(trans_df2["Transaction_type"] == selected_type)]

if selected_state2:
    trans_df2 = trans_df2[trans_df2["State"] == selected_state2]

trans_df2 = trans_df2.groupby(['State', 'Year', 'Quarter']).sum().reset_index()

fig2 = px.line(
             trans_df2, x="Quarter", y="Transaction_count", 
             color="State",
             color_discrete_sequence=px.colors.qualitative.Plotly,
             title=f"{selected_type} transactions for {selected_state2 if selected_state2 else 'All States'} in {year1}",
             labels=dict(Transaction_count='Transaction Count', Quarter='Quarter')
             )

fig2.update_layout(
    showlegend=True, 
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    title={
        'x': 0.5,
        'xanchor': 'center',
        'y': 0.9,
        'yanchor': 'top'
    }
)

fig2.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
fig2.update_xaxes(tickmode='array', tickvals=list(range(0,5)))
fig2.update_layout( width=850, height=550)


st.plotly_chart(fig2)