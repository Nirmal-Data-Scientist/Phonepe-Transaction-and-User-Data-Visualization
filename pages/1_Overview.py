import streamlit as st
import plotly.express as px
import json
from streamlit_extras.add_vertical_space import add_vertical_space


# Data Prep


agg_trans = st.session_state["agg_trans_df"]
map_trans = st.session_state["map_trans_df"]
map_user = st.session_state["map_user_df"]


#1


total_trans_count = agg_trans['Transaction_count'].sum()
trans_type_count = agg_trans.groupby('Transaction_type')['Transaction_count'].sum()
trans_type_perc = round(trans_type_count / total_trans_count * 100, 2)

trans_type_fig = px.pie(
                        trans_type_perc, names=trans_type_perc.index,
                        values='Transaction_count', hole=.65,
                        hover_data={'Transaction_count': False}
                        )

trans_type_fig.update_layout(width = 900, height = 500)


#2


trans_state = agg_trans.groupby('State')['Transaction_count'].sum().reset_index()
trans_state_sorted = trans_state.sort_values(by='Transaction_count', ascending=False).head(15)

trans_state_fig = px.bar(
                         trans_state_sorted, x='Transaction_count',
                         y='State', orientation='h',
                         text='Transaction_count', text_auto='.2s',
                         labels = {'Transaction_count': "Transaction Count"}
                         )

trans_state_fig.update_layout(
                                yaxis=dict(autorange="reversed"),
                                width = 900, height = 500
                                )


#3


trans_district = map_trans.groupby(['State', 'District'])[[
                                                            'Transaction_count', 'Transaction_amount'
                                                            ]
                                                          ].sum().reset_index()

trans_district_sorted = trans_district.sort_values(by='Transaction_count', ascending=False).head(15)

trans_district_fig = px.bar(
                            trans_district_sorted, y='District',
                            x='Transaction_count', text='Transaction_count',
                            hover_name='District', height=600,
                            labels = {'Transaction_count': "Transaction Count"},
                            hover_data = {'State': True, 'District': False}
                            )
trans_district_fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')

trans_district_fig.update_layout(
                                 yaxis = dict(autorange="reversed"),
                                 width = 900, height = 500
                                 )


#4


total_reg_users = map_user['Registered_users'].sum()
user_state = map_user.groupby('State')['Registered_users'].sum().reset_index()

with open(r"Miscellaneous/india_states.json") as f:
    geojson = json.load(f)

if 'geojson' not in st.session_state:
    st.session_state["geojson"] = geojson

user_state_fig = px.choropleth(
                                user_state, geojson = geojson,
                                locations = 'State',
                                featureidkey = 'properties.ST_NM',
                                color='Registered_users', projection = 'orthographic',
                                labels = {'Registered_users': "Registered Users"},
                                color_continuous_scale = 'reds'
                                )

user_state_fig.update_geos(fitbounds='locations', visible=False)
user_state_fig.update_layout(height=600, width=900, coloraxis_colorbar=dict(thickness=20, len=0.5))  


# App


st.set_page_config(page_title = 'Overview', layout = 'wide', page_icon = 'Related Images and Videos/Logo.png')

st.title(':blue[Overview]')

add_vertical_space(3)

#1

st.subheader(":blue[Transaction Breakdown by Type]")

st.plotly_chart(trans_type_fig)

#2

st.subheader(":blue[Transaction Count by State]")

st.plotly_chart(trans_state_fig)

#3

st.subheader(":blue[Transaction Count by District]")

st.plotly_chart(trans_district_fig)

#4

st.subheader(':blue[Registered User Count by State]')

st.plotly_chart(user_state_fig, use_container_width = True)