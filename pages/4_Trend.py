import streamlit as st
import plotly.express as px
import altair as alt
from streamlit_extras.add_vertical_space import add_vertical_space

st.set_page_config(page_title = 'Trend Analysis', layout = 'wide', page_icon = 'Related Images and Videos/Logo.png')
st.title(':blue[Trend Analysis]')
add_vertical_space(3)

st.subheader(':blue[Transaction Count and Amount - Trend over the years]')
add_vertical_space(1)

col1, col2, col3, col4 = st.columns([3, 4, 4, 2])

region1 = col1.selectbox('Region', st.session_state["agg_trans_df"]["Region"].unique(), key='region1')

df = st.session_state['map_trans_df'][st.session_state['map_trans_df']['Region'] == region1]

state1 = col2.selectbox('State', df['State'].unique(), key='state1')

if state1 != 'All':
    df = df[df['State'] == state1]

    district_options = list(df['District'].unique())
    district1 = col3.selectbox('District', district_options, key='district1')

    if district1 != 'All':
        df = df[df['District'] == district1]
else:
    district1 = ''

year_options = ['All'] + [year for year in st.session_state['years']]
year1 = col4.selectbox('Year', year_options, key='year1')

title1=f'Transaction count trend for {district1} district in {state1} across {str(year1).lower()} years'
title2=f'Transaction amount trend for {district1} district in {state1} across {str(year1).lower()} years'

if year1 != 'All':
    df = df[df['Year'] == year1]
    title1=f'Transaction count trend for {district1} district in {state1} during {year1}'
    title2=f'Transaction amount trend for {district1} district in {state1} during {year1}'
    
if state1 == 'All':
    df = st.session_state['map_trans_df']

    if year1 != 'All':
        df = df[df['Year'] == year1]


fig1 = px.line(df, x='Quarter', y='Transaction_count', color='Year', title=title1)
fig1.update_xaxes(tickmode='array', tickvals=list(range(1,5)))
fig1.update_layout(height = 500, width = 900)
fig1.update_layout(title={'x': 0.5, 'xanchor': 'center', 'y': 0.9, 'yanchor': 'bottom'})


fig2 = px.line(df, x='Quarter', y='Transaction_amount', color='Year', title=title2)
fig2.update_xaxes(tickmode='array', tickvals=list(range(1,5)))
fig2.update_layout(height = 500, width = 900)
fig2.update_layout(title={'x': 0.5, 'xanchor': 'center', 'y': 0.9, 'yanchor': 'bottom'})

tab1, tab2 = st.tabs(['🫰Transaction Count Trend', '💰Transaction Amount Trend'])

tab1.plotly_chart(fig1)
tab2.plotly_chart(fig2)


st.subheader(':blue[Transaction Count and Amount - Top Districts]')

col5, col6, col7 = st.columns([5, 3, 1])

state_options = ["All"] + list(st.session_state['states'])
year_options = st.session_state["years"]
quarter_options = ["All"] + list(st.session_state['quarters'])

state2 = col5.selectbox("State", state_options, key="state2")
year2 = col6.selectbox("Year", year_options, key="year2")
quarter2 = col7.selectbox("Quarter", quarter_options, key="quarter2")

data = st.session_state["top_trans_dist_df"]

if state2 != "All":
    data = data[data["State"] == state2]
if year2:
    data = data[data["Year"] == year2]
if quarter2 != "All":
    data = data[data["Quarter"] == quarter2]

top_districts1 = data.groupby("District")["Transaction_count"].sum().nlargest(10).index.tolist()

suffix1 = " quarters" if quarter2 == 'All' else "st" if quarter2 == 1 else "nd" if quarter2 == 2 else "rd" if quarter2 == 3 else "th"

title3 = f"Top districts in {'India' if state2 == 'All' else state2} by Transaction count during {str(quarter2).lower()}{suffix1} {'' if quarter2 == 'All' else 'quarter'} of {year2}"


data1 = data[data["District"].isin(top_districts1)]
data1["Transaction_count_millions"] = data1["Transaction_count"] / 1e6


chart1 = alt.Chart(data1, height=500, width=900).mark_bar(size=18).encode(
    x=alt.X("Transaction_count_millions", title="Transaction Count (in millions)"),
    y=alt.Y("District", sort=top_districts1, title=None),
    color="State",
    tooltip=["District", "State", "Year", "Quarter", "Transaction_count"]
).properties(
    title=alt.TitleParams(
        text=title3,
        align="center", anchor = 'middle',
        baseline="bottom"
    )
).configure_axis(
    labelFontSize=14, titleFontSize=16, labelPadding=8, labelAngle=0, 
    labelOverlap=True, grid=False, ticks=False
)


top_districts2 = data.groupby("District")["Transaction_amount"].sum().nlargest(10).index.tolist()

title4 = f"Top districts in {'India' if state2 == 'All' else state2} by Transaction amount during {str(quarter2).lower()}{suffix1} {'' if quarter2 == 'All' else 'quarter'} of {year2}"

data2 = data[data["District"].isin(top_districts2)]

chart2 = alt.Chart(data2, height = 500, width = 900).mark_bar(size=18).encode(
    x=alt.X("sum(Transaction_amount)", title="Transaction Amount"),
    y=alt.Y("District", sort=top_districts2, title=None),
    color="State",
    tooltip=["District", "State", "Year", "Quarter", "Transaction_amount"]
).properties(
    title=alt.TitleParams(
        text=title4,
        align="center", anchor = 'middle',
        baseline="bottom"
    )
).configure_axis(
    labelFontSize=14, titleFontSize=16, labelPadding=8, labelAngle=0, 
    labelOverlap=True, grid=False, ticks=False
)

tab3, tab4 = st.tabs(['🫰Transaction Count - Top Districts', '💰Transaction Amount - Top Districts'])
tab3.altair_chart(chart1, use_container_width=True)
tab4.altair_chart(chart2, use_container_width=True)



st.subheader(':blue[Other Key Trends over the years]')



dist_trans = st.session_state['top_trans_dist_df']
pin_trans = st.session_state['top_trans_pin_df']

top_states = dist_trans.groupby('State')['Transaction_amount'].sum().reset_index().sort_values('Transaction_amount', ascending=False).head(10)

top_districts = dist_trans.groupby('District')['Transaction_amount'].sum().reset_index().sort_values('Transaction_amount', ascending=False).head(10)

top_pincodes = pin_trans.groupby('Pincode')['Transaction_amount'].sum().reset_index().sort_values('Transaction_amount', ascending=False).head(10)

def filter_data(data, year, quarter):
    if quarter == 'All':
        filtered_data = data[data['Year'] == year]
    else:
        filtered_data = data[(data['Year'] == year) & (data['Quarter'] == quarter)]
    return filtered_data

col8, col9, col10 = st.columns([5, 3, 1])

trend3 = col8.selectbox('Trend', ('Top 10 States by Transaction Volume', 'Top 10 Districts by Transaction Volume', 'Top 10 Pincodes by Transaction Volume'), key = 'trend3')

year3 = col9.selectbox('Year', st.session_state["years"], key = 'year3')

quarter3 = col10.selectbox('Quarter', quarter_options, key = 'quarter3')

filtered_dist_trans = filter_data(dist_trans, year3, quarter3)
filtered_pin_trans = filter_data(pin_trans, year3, quarter3)

filtered_top_states = filtered_dist_trans.groupby('State')['Transaction_amount'].sum().reset_index().sort_values('Transaction_amount', ascending=False).head(10)

filtered_top_districts = filtered_dist_trans.groupby('District')['Transaction_amount'].sum().reset_index().sort_values('Transaction_amount', ascending=False).head(10)

filtered_top_pincodes = filtered_pin_trans.groupby('Pincode')['Transaction_amount'].sum().reset_index().sort_values('Transaction_amount', ascending=False).head(10)
filtered_top_pincodes['Pincode'] = filtered_top_pincodes['Pincode'].astype(str)


axis_format = '~s'
suffix2 = " quarters" if quarter3 == 'All' else "st" if quarter3 == 1 else "nd" if quarter3 == 2 else "rd" if quarter3 == 3 else "th"

if trend3 == 'Top 10 States by Transaction Volume':
    chart = alt.Chart(filtered_top_states, height = 500, width = 900).mark_bar(size=18).encode(
        x=alt.X('Transaction_amount', axis=alt.Axis(format=axis_format)),
        y=alt.Y('State', sort='-x'),
        tooltip=['State', alt.Tooltip('Transaction_amount',
                                       format='.2f')]
    ).properties(
        title=alt.TitleParams(text = f"Top 10 states by Transaction volume {'across' if quarter3 == 'All' else 'in'} {str(quarter3).lower()}{suffix2} {'' if quarter3 == 'All' else 'quarter'} of {year3}",
        align="center", anchor = 'middle')
    )

elif trend3 == 'Top 10 Districts by Transaction Volume':
    chart = alt.Chart(filtered_top_districts, height = 500, width = 900).mark_bar(size=18).encode(
        x=alt.X('Transaction_amount', axis=alt.Axis(format=axis_format)),
        y=alt.Y('District', sort='-x'),
        tooltip=['District', alt.Tooltip('Transaction_amount',
                                          format='.2f')]
    ).properties(
        title=alt.TitleParams(text = f"Top 10 districts by Transaction volume {'across' if quarter3 == 'All' else 'in'} {str(quarter3).lower()}{suffix2} {'' if quarter3 == 'All' else 'quarter'} of {year3}",
        align="center", anchor = 'middle')
    )

elif trend3 == 'Top 10 Pincodes by Transaction Volume':
    chart = alt.Chart(filtered_top_pincodes, height = 500, width = 900).mark_bar(size=18).encode(
        x=alt.X('Transaction_amount', axis=alt.Axis(format=axis_format)),
        y=alt.Y('Pincode', sort='-x'),
        tooltip=['Pincode', alt.Tooltip('Transaction_amount',
                                          format='.2f')]
    ).properties(
        title=alt.TitleParams(text = f"Top 10 pincode locations by Transaction volume {'across' if quarter3 == 'All' else 'in'} {str(quarter3).lower()}{suffix2} {'' if quarter3 == 'All' else 'quarter'} of {year3}",
        align="center", anchor = 'middle')
    )


st.altair_chart(chart, use_container_width=True)