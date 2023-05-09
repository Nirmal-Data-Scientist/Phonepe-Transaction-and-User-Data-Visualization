import streamlit as st
import plotly.express as px
from streamlit_extras.add_vertical_space import add_vertical_space


# Data Prep


agg_trans = st.session_state["agg_trans_df"]

states = agg_trans["State"].unique()
years = agg_trans["Year"].unique()
quarters = agg_trans["Quarter"].unique()

if 'states' not in st.session_state:
    st.session_state["states"] = states
if 'years' not in st.session_state:
    st.session_state["years"] = years
if 'quarters' not in st.session_state:
    st.session_state["quarters"] = quarters


# App


st.set_page_config(page_title = 'Transaction', layout = 'wide', page_icon = 'Related Images and Videos/Logo.png')
st.title(':blue[Transaction]')
add_vertical_space(3)


#1


st.subheader(':blue[Transaction amount breakdown]')

trans_df = agg_trans

col1, col2, col3 = st.columns([5, 3, 1])

state1 = col1.selectbox("State", states, key='state1')
year1 = col2.selectbox("Year", years, key='year1')
quarter_options = ["All"] + list(map(str, quarters))
quarter1 = col3.selectbox("Quarter", quarter_options, key='quarter1')

if quarter1 != 'All':
    
    trans_df = trans_df[
                        (trans_df["State"] == state1) 
                                    & 
                         (trans_df["Year"] == year1) 
                                    & 
                        (trans_df["Quarter"] == int(quarter1))
                        ]

else:
    
    trans_df = trans_df[(trans_df["State"] == state1) & (trans_df["Year"] == year1)]

trans_df = trans_df.sort_values("Transaction_amount", ascending=False).reset_index(drop = True)

suffix1 = " quarters" if quarter1 == 'All' else "st" if quarter1 == '1' else "nd" if quarter1 == '2' else "rd" if quarter1 == '3' else "th"

title1 = f"Transaction details of {state1} for {quarter1.lower()}{suffix1} {'' if quarter1 == 'All' else 'quarter'} of {year1}"

fig1 = px.bar(
             trans_df, x="Transaction_type", y="Transaction_amount", 
             color="Transaction_type",
             color_discrete_sequence=px.colors.qualitative.Plotly,
             title=title1,
             labels=dict(Transaction_amount='Transaction Amount', Transaction_type='Transaction Type'),
             hover_data={'Quarter': True}
             )

fig1.update_layout(
    showlegend=False, 
    title={
        'x': 0.5,
        'xanchor': 'center',
        'y': 0.9,
        'yanchor': 'top'
    }, width = 900, height = 500
)

fig1.update_traces(marker = dict(line = dict(width = 1, color = 'DarkSlateGrey')))

st.plotly_chart(fig1)

expander1 = st.expander(label = 'Detailed view')
expander1.write(trans_df.loc[:, ['Quarter', 'Transaction_type', 'Transaction_amount']].reset_index(drop=True))


#2


st.subheader(':blue[Transaction Hotspots - Districts]')

map_df = st.session_state["map_trans_df"]

year_col, quarter_col, buff1, buff2 = st.columns([1,1,2,2])

year2 = year_col.selectbox("Year", years, key = 'year2')
quarter2 = quarter_col.selectbox("Quarter", quarter_options, key = 'quarter2')

if quarter2 == "All":
    map_df = map_df[map_df["Year"] == year2]
else:
    map_df = map_df[(map_df["Year"] == year2) & (map_df["Quarter"] == int(quarter2))]

suffix2 = " quarters" if quarter2 == 'All' else "st" if quarter2 == '1' else "nd" if quarter2 == '2' else "rd" if quarter2 == '3' else "th"

title2 = f"Transaction hotspots for {quarter2.lower()}{suffix2} {'' if quarter2 == 'All' else 'quarter'} of {year2}"


fig2 = px.scatter_mapbox(map_df, lat = "Latitude", lon = "Longitude", hover_name = "District",
                        size = "Transaction_amount",
                        hover_data = {"Transaction_count": True, "Transaction_amount": True},
                        title = title2,
                        height=600, width=800
                        )

fig2.update_layout(mapbox_style = 'carto-positron',
                   mapbox_zoom = 3.5, mapbox_center = {"lat": 20.93684, "lon": 78.96288},
                   geo=dict(
                            scope = 'asia', projection_type = 'equirectangular',
                            showocean = True,
                            oceancolor = 'rgb(229, 255, 255)',
                            showcountries = True,
                           ), 
                   title={
                          'x': 0.5,
                          'xanchor': 'center',
                          'y': 0.04,
                          'yanchor': 'bottom',
                          'font': dict(color='black')
                         },
                   margin={"r":0,"t":0,"l":0,"b":0}, width = 900, height = 500
                  )

st.plotly_chart(fig2)

expander2 = st.expander(label = 'Detailed view')
expander2.write(map_df.loc[:, ['State', 'District', 'Quarter', 'Transaction_amount']].reset_index(drop=True))


#3


st.subheader(":blue[Breakdown by transaction count proportion]")

trans_df_2 = agg_trans

state_pie, year_pie, quarter_pie = st.columns([5, 3, 1])

state3 = state_pie.selectbox('State', options = states, key = 'state3')
year3 = year_pie.selectbox('Year', options = years, key = 'year3')
quarter3 = quarter_pie.selectbox('Quarter', options = quarter_options, key = 'quarter3')

filtered_trans = trans_df_2[(trans_df_2.State == state3) & (trans_df_2.Year == year3)]

if quarter3 != 'All':
    filtered_trans = filtered_trans[filtered_trans.Quarter == int(quarter3)]

fig3 = px.pie(
              filtered_trans, names = 'Transaction_type',
              values = 'Transaction_count', hole = .65
              )

fig3.update_layout(width = 900, height = 500)

st.plotly_chart(fig3)

expander3 = st.expander(label = 'Detailed view')
expander3.write(filtered_trans.loc[:, ['Quarter', 'Transaction_type', 'Transaction_count']].reset_index(drop = True))