import streamlit as st
import plotly.express as px
import altair as alt
from streamlit_extras.add_vertical_space import add_vertical_space


# Data Prep


map_trans = st.session_state['map_trans_df']
top_trans_dist = dist_trans = st.session_state["top_trans_dist_df"]       # Would apply filter over the first df so taking same df again in some other name
pin_trans = st.session_state['top_trans_pin_df']


top_states = dist_trans.groupby('State')[
                                         'Transaction_amount'
                                         ].sum().reset_index().sort_values(
                                                                           'Transaction_amount',
                                                                           ascending=False
                                                                           ).head(10)

top_districts = dist_trans.groupby('District')[
                                               'Transaction_amount'
                                               ].sum().reset_index().sort_values(
                                                                                 'Transaction_amount',
                                                                                 ascending=False
                                                                                 ).head(10)

top_pincodes = pin_trans.groupby('Pincode')[
                                            'Transaction_amount'
                                            ].sum().reset_index().sort_values(
                                                                              'Transaction_amount',
                                                                              ascending=False
                                                                              ).head(10)


# Function Definition


def filter_top_trans_dist(top_trans_dist, year, quarter):
    
    filtered_top_trans_dist = top_trans_dist[top_trans_dist['Year'] == year]
    if quarter != 'All':
        filtered_top_trans_dist = filter_top_trans_dist[(filter_top_trans_dist['Quarter'] == quarter)]
    return filtered_top_trans_dist


# App

st.set_page_config(page_title = 'Trend Analysis', layout = 'wide', page_icon = 'Related Images and Videos/Logo.png')
st.title(':blue[Trend Analysis]')
add_vertical_space(3)


#1

st.subheader(':blue[Transaction Count and Amount - Trend over the years]')
add_vertical_space(1)

col1, col2, col3, col4 = st.columns([3, 4, 4, 2])

region1 = col1.selectbox('Region', map_trans["Region"].unique(), key='region1')

df = map_trans[map_trans['Region'] == region1]

state1 = col2.selectbox('State', df['State'].unique(), key='state1')

df = df[df['State'] == state1]

district1 = col3.selectbox('District', df['District'].unique(), key='district1')

df = df[df['District'] == district1]

year_options = ['All'] + [year for year in st.session_state['years']]
year1 = col4.selectbox('Year', year_options, key='year1')

title1=f'Transaction count trend for {district1} district in {state1} across {str(year1).lower()} years'
title2=f'Transaction amount trend for {district1} district in {state1} across {str(year1).lower()} years'

if year1 != 'All':
    
    df = df[df['Year'] == year1]
    
    title1=f'Transaction count trend for {district1} district in {state1} during {year1}'
    title2=f'Transaction amount trend for {district1} district in {state1} during {year1}'

fig1 = px.line(df, x='Quarter', y='Transaction_count', color='Year', title=title1)

fig1.update_xaxes(tickmode='array', tickvals=list(range(1,5)))

fig1.update_layout(
                   height = 500, width = 900,
                   yaxis_title = 'Transaction Count',
                   title={
                          'x': 0.5,
                          'xanchor': 'center',
                          'y': 0.9,
                          'yanchor': 'bottom'
                          }
                   )

fig2 = px.line(df, x='Quarter', y='Transaction_amount', color='Year', title=title2)

fig2.update_xaxes(tickmode='array', tickvals=list(range(1,5)))

fig2.update_layout(
                   height = 500, width = 900,
                   yaxis_title = 'Transaction Amount',
                   title={
                          'x': 0.5,
                          'xanchor': 'center',
                          'y': 0.9,
                          'yanchor': 'bottom'
                          }
                   )

tab1, tab2 = st.tabs(['🫰Transaction Count Trend', '💰Transaction Amount Trend'])

tab1.plotly_chart(fig1)

expander1 = tab1.expander('Detailed view')
expander1.write(df.loc[:, ['Region', 'District', 'Year', 'Quarter', 'Transaction_count']].reset_index(drop = True))

tab2.plotly_chart(fig2)

expander2 = tab2.expander('Detailed view')
expander2.write(df.loc[:, ['Region', 'District', 'Year', 'Quarter', 'Transaction_amount']].reset_index(drop = True))


#2


st.subheader(':blue[Transaction Count and Amount - Top Districts]')

col5, col6, col7 = st.columns([5, 3, 1])

state_options = ["All"] + list(st.session_state['states'])
year_options = st.session_state["years"]
quarter_options = ["All"] + list(st.session_state['quarters'])

state2 = col5.selectbox("State", state_options, key="state2")
year2 = col6.selectbox("Year", year_options, key="year2")
quarter2 = col7.selectbox("Quarter", quarter_options, key="quarter2")

if state2 != "All":
    top_trans_dist = top_trans_dist[top_trans_dist["State"] == state2]

top_trans_dist = top_trans_dist[top_trans_dist["Year"] == year2]

if quarter2 != "All":
    top_trans_dist = top_trans_dist[top_trans_dist["Quarter"] == quarter2]


top_dist_grouped_1 = top_trans_dist.groupby("District")["Transaction_count"].sum().nlargest(10).index.tolist()

top_trans_dist_filtered_1 = top_trans_dist[top_trans_dist["District"].isin(top_dist_grouped_1)]


suffix1 = " quarters" if quarter2 == 'All' else "st" if quarter2 == 1 else "nd" if quarter2 == 2 else "rd" if quarter2 == 3 else "th"

title3 = f"Top districts in {'India' if state2 == 'All' else state2} by Transaction count during {str(quarter2).lower()}{suffix1} {'' if quarter2 == 'All' else 'quarter'} of {year2}"

axis_format = '~s'


chart1 = alt.Chart(
                    top_trans_dist_filtered_1,
                    height=500, width=900
                    ).mark_bar(size=18).encode(
                                                x=alt.X(
                                                        "Transaction_count",
                                                        title="Transaction Count",
                                                        axis=alt.Axis(format=axis_format)
                                                        ),
                                                y=alt.Y(
                                                        "District",
                                                        sort=top_dist_grouped_1,
                                                        title=None
                                                        ),
                                                color="State",
                                                tooltip=[
                                                         "District", "State", "Year",
                                                         "Quarter", "Transaction_count"
                                                         ]
                                                ).properties(
                                                             title=alt.TitleParams(
                                                                                    text=title3,
                                                                                    align="center",
                                                                                    anchor = 'middle',
                                                                                    baseline="bottom"
                                                                                    )
                                                             ).configure_axis(grid=False)


top_dist_grouped_2 = top_trans_dist.groupby("District")["Transaction_amount"].sum().nlargest(10).index.tolist()

top_trans_dist_filtered_2 = top_trans_dist[top_trans_dist["District"].isin(top_dist_grouped_2)]

title4 = f"Top districts in {'India' if state2 == 'All' else state2} by Transaction amount during {str(quarter2).lower()}{suffix1} {'' if quarter2 == 'All' else 'quarter'} of {year2}"


chart2 = alt.Chart(
                   top_trans_dist_filtered_2,
                   height = 500, width = 900
                   ).mark_bar(size=18).encode(
                                              x=alt.X(
                                                      "sum(Transaction_amount)",
                                                      title="Transaction Amount",
                                                      axis=alt.Axis(format=axis_format)
                                                      ),
                                              y=alt.Y(
                                                      "District", sort=top_dist_grouped_2,
                                                      title=None
                                                      ),
                                              color="State",
                                              tooltip=[
                                                        "District", "State", "Year",
                                                        "Quarter", "Transaction_amount"
                                                        ]
                                              ).properties(
                                                           title=alt.TitleParams(
                                                                                 text=title4,
                                                                                 align="center",
                                                                                 anchor = 'middle',
                                                                                 baseline="bottom"
                                                                                 )
                                                           ).configure_axis(grid=False)

tab3, tab4 = st.tabs(['🫰Transaction Count - Top Districts', '💰Transaction Amount - Top Districts'])

tab3.altair_chart(chart1, use_container_width=True)

expander3 = tab3.expander('Detailed view')
expander3.write(top_trans_dist_filtered_1.loc[
                                               :,
                                               [
                                                'State', 'District', 'Quarter', 'Transaction_count'
                                                ]
                                               ].reset_index(drop = True))

tab4.altair_chart(chart2, use_container_width=True)

expander4 = tab4.expander('Detailed view')
expander4.write(top_trans_dist_filtered_2.loc[
                                               :, 
                                               [
                                                'State', 'District', 'Quarter', 'Transaction_amount'
                                                ]
                                               ].reset_index(drop = True))


#3


st.subheader(':blue[Other Key Trends over the years]')


col8, col9, col10 = st.columns([5, 3, 1])

trend3 = col8.selectbox(
                        'Trend',
                        (
                         'Top 10 States by Transaction Volume',
                         'Top 10 Districts by Transaction Volume',
                         'Top 10 Pincodes by Transaction Volume'
                         ),
                        key = 'trend3'
                        )

year3 = col9.selectbox('Year', st.session_state["years"], key = 'year3')

quarter3 = col10.selectbox('Quarter', quarter_options, key = 'quarter3')

filtered_dist_trans = filter_top_trans_dist(dist_trans, year3, quarter3)
filtered_pin_trans = filter_top_trans_dist(pin_trans, year3, quarter3)

filtered_top_states = filtered_dist_trans.groupby('State')[
                                                           'Transaction_amount'
                                                           ].sum().reset_index().sort_values(
                                                                                             'Transaction_amount',
                                                                                             ascending=False
                                                                                             ).head(10)

filtered_top_districts = filtered_dist_trans.groupby('District')[
                                                                 'Transaction_amount'
                                                                 ].sum().reset_index().sort_values(
                                                                                                   'Transaction_amount',
                                                                                                   ascending=False
                                                                                                   ).head(10)

filtered_top_pincodes = filtered_pin_trans.groupby('Pincode')[
                                                              'Transaction_amount'
                                                              ].sum().reset_index().sort_values(
                                                                                                'Transaction_amount',
                                                                                                ascending=False
                                                                                                ).head(10)
filtered_top_pincodes['Pincode'] = filtered_top_pincodes['Pincode'].astype(str)

suffix2 = " quarters" if quarter3 == 'All' else "st" if quarter3 == 1 else "nd" if quarter3 == 2 else "rd" if quarter3 == 3 else "th"

title5 = f"Top 10 states by Transaction volume {'across' if quarter3 == 'All' else 'in'} {str(quarter3).lower()}{suffix2} {'' if quarter3 == 'All' else 'quarter'} of {year3}"

title6 = f"Top 10 districts by Transaction volume {'across' if quarter3 == 'All' else 'in'} {str(quarter3).lower()}{suffix2} {'' if quarter3 == 'All' else 'quarter'} of {year3}"

title7 = f"Top 10 pincode locations by Transaction volume {'across' if quarter3 == 'All' else 'in'} {str(quarter3).lower()}{suffix2} {'' if quarter3 == 'All' else 'quarter'} of {year3}"

if trend3 == 'Top 10 States by Transaction Volume':
    
    chart3 = alt.Chart(
                      filtered_top_states,
                      height = 500, width = 900
                      ).mark_bar(size=18).encode(
                                                 x=alt.X(
                                                         'Transaction_amount',
                                                         axis=alt.Axis(format=axis_format),
                                                         title="Transaction Amount"
                                                         ),
                                                 y=alt.Y('State', sort='-x'),
                                                 tooltip=[
                                                          'State', alt.Tooltip('Transaction_amount',format='.2f')
                                                          ]
                                                 ).properties(
                                                              title=alt.TitleParams(
                                                                                    text = title5,
                                                                                    align="center",
                                                                                    anchor = 'middle'
                                                                                    )
                                                              )

elif trend3 == 'Top 10 Districts by Transaction Volume':
    
    chart3 = alt.Chart(
                      filtered_top_districts,
                      height = 500, width = 900
                      ).mark_bar(size=18).encode(
                                                 x=alt.X(
                                                         'Transaction_amount',
                                                         axis=alt.Axis(format=axis_format),
                                                         title="Transaction Amount"
                                                         ),
                                                 y=alt.Y('District', sort='-x'),
                                                 tooltip=[
                                                          'District', alt.Tooltip('Transaction_amount',format='.2f')
                                                          ]
                                                 ).properties(
                                                              title=alt.TitleParams(
                                                                                    text = title6,
                                                                                    align="center",
                                                                                    anchor = 'middle'
                                                                                    )
                                                              )

elif trend3 == 'Top 10 Pincodes by Transaction Volume':
    
    chart3 = alt.Chart(
                      filtered_top_pincodes,
                      height = 500, width = 900
                      ).mark_bar(size=18).encode(
                                                 x=alt.X(
                                                         'Transaction_amount',
                                                         axis=alt.Axis(format=axis_format),
                                                         title="Transaction Amount"
                                                         ),
                                                 y=alt.Y('Pincode', sort='-x'),
                                                 tooltip=[
                                                          'Pincode', alt.Tooltip('Transaction_amount', format='.2f')
                                                          ]
                                                 ).properties(
                                                              title=alt.TitleParams(
                                                                                    text = title7,
                                                                                    align="center",
                                                                                    anchor = 'middle'
                                                                                    )
                                                              )

st.altair_chart(chart3, use_container_width=True)

expander5 = st.expander('Detailed view')
data = filtered_top_states if trend3 == 'Top 10 States by Transaction Volume' else filtered_top_districts if trend3 == 'Top 10 Districts by Transaction Volume' else filtered_top_pincodes
expander5.dataframe(data.reset_index(drop = True))