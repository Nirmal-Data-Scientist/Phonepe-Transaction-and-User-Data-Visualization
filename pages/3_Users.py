import streamlit as st
import plotly.express as px
from streamlit_extras.add_vertical_space import add_vertical_space



# Data Prep

agg_user_df1 = st.session_state["agg_user_df"]
map_user_df1 = st.session_state["map_user_df"]
top_user_dist_df1 = st.session_state["top_user_dist_df"]


# App


st.set_page_config(page_title = 'Users', layout = 'wide', page_icon = 'Related Images and Videos/Logo.png')
st.title(':blue[Users]')
add_vertical_space(3)


#1


st.subheader(':blue[Transaction Count and Percentage by Brand]')

col1, col2, col3 = st.columns([5, 3, 1])

state_options = ['All'] + [state for state in st.session_state['states']]
quarter_options = ["All"] + list(map(str, st.session_state['quarters']))

state1 = col1.selectbox('State', options=state_options, key='state1')
year1 = col2.selectbox('Year', options=st.session_state['years'], key='year1')
quarter1 = col3.selectbox("Quarter", options=quarter_options, key='quarter1')

if state1 == "All":
    
    agg_user_df_filtered = agg_user_df1[(agg_user_df1['Year'] == year1)]
    
    if quarter1 != 'All':
        agg_user_df_filtered = agg_user_df_filtered[agg_user_df_filtered['Quarter'] == int(quarter1)]
    
    suffix1 = " quarters" if quarter1 == 'All' else "st" if quarter1 == '1' else "nd" if quarter1 == '2' else "rd" if quarter1 == '3' else "th"
    
    title1=f"Transaction Count and Percentage across all states for {quarter1.lower()}{suffix1} {'' if quarter1 == 'All' else 'quarter'} of {year1}"

else:
    
    agg_user_df_filtered = agg_user_df1[(agg_user_df1['State'] == state1) & (agg_user_df1['Year'] == year1)]
    
    if quarter1 != 'All':
        agg_user_df_filtered = agg_user_df_filtered[agg_user_df_filtered['Quarter'] == int(quarter1)]
    
    suffix1 = " quarters" if quarter1 == 'All' else "st" if quarter1 == '1' else "nd" if quarter1 == '2' else "rd" if quarter1 == '3' else "th"
    
    title1=f"Transaction Count and Percentage in {state1} for {quarter1.lower()}{suffix1} {'' if quarter1 == 'All' else 'quarter'} of {year1}"


fig1 = px.treemap(
                  agg_user_df_filtered,
                  path=['Brand'],
                  values='Transaction_count',
                  color='Percentage',
                  color_continuous_scale='ylorbr',
                  hover_data={'Percentage': ':.2%'},
                  hover_name='Brand'
                  )

fig1.update_layout(
                    width=975, height=600,
                    coloraxis_colorbar=dict(tickformat='.1%'),
                    margin=dict(l=20, r=20, t=60, b=20),
                    title = {
                            "text": title1 ,
                             'x': 0.45,
                             'xanchor': 'center',
                             'y': 0.004,
                             'yanchor': 'bottom'
                             }
                    )

fig1.update_traces(
                    hovertemplate = 
                    '<b>%{label}</b><br>Transaction Count: %{value}<br>Percentage: %{color:.2%}<extra></extra>'
                    )

st.plotly_chart(fig1)

add_vertical_space(2)


#2


st.subheader(':blue[Registered Users Hotspots - Disrict]')

col4, col5, col6 = st.columns([5, 3, 1])

state_options = ['All'] + [state for state in st.session_state['states']]
quarter_options = ["All"] + list(map(str, st.session_state['quarters']))

state2 = col4.selectbox('State', options=state_options, key='state2')
year2 = col5.selectbox('Year', options=st.session_state['years'], key='year2')
quarter2 = col6.selectbox("Quarter", options=quarter_options, key='quarter2')

if state2 == 'All':
    map_user_df_filtered = map_user_df1
else:
    map_user_df_filtered = map_user_df1[(map_user_df1["State"] == state2) & (map_user_df1["Year"] == year2)]
    
    if quarter2 != 'All':
        map_user_df_filtered = map_user_df_filtered[map_user_df_filtered['Quarter'] == int(quarter2)]

fig2 = px.scatter_mapbox(
                         map_user_df_filtered, 
                         lat="Latitude", 
                         lon="Longitude", 
                         size="Registered_users", 
                         hover_name="District",
                         title=f"Registered Users by District"
                     )

fig2.update_layout(
                   mapbox_style = 'carto-positron',
                   mapbox_zoom = 3.5, mapbox_center = {"lat": 20.93684, "lon": 78.96288},
                   geo=dict(
                            scope = 'asia', projection_type = 'equirectangular',
                            showocean = True,
                            oceancolor = 'rgb(229, 255, 255)',
                            showcountries = True
                            ),
                   title={
                          'x': 0.5,
                          'xanchor': 'center',
                          'y': 0.05,
                          'yanchor': 'bottom'
                          },
                   height=600, width=900, coloraxis_colorbar=dict(thickness=20, len=0.5),
                   margin={"r":0,"t":0,"l":0,"b":0}
                  )

fig2.update_geos(fitbounds='locations', visible=False)

st.plotly_chart(fig2)

add_vertical_space(2)


#3


st.subheader(':blue[Top Districts by Registered Users]')

col7, col8, buff1 = st.columns([5, 3, 4])

state3 = col7.selectbox('State', options = state_options, key='state3')
year3 = col8.selectbox('Year', options = st.session_state['years'], key='year3')

if state3 == "All":
    
    top_user_dist_df_filtered = top_user_dist_df1[
                                                  top_user_dist_df1['Year']==year3
                                                  ].groupby('District').sum().reset_index()
    
    top_user_dist_df_filtered = top_user_dist_df_filtered.sort_values(
                                                                      by = 'Registered_users',
                                                                      ascending = False
                                                                      ).head(10)
    
    title3 = f'Top 10 districts across all states by registered users in {year3}'

else:
    
    top_user_dist_df_filtered = top_user_dist_df1[
                                                  (top_user_dist_df1['State']==state3) & 
                                                  (top_user_dist_df1['Year']==year3)
                                                   ]
    
    top_user_dist_df_filtered = top_user_dist_df_filtered.groupby('District').sum().reset_index().sort_values(
                                                                                          by = 'Registered_users',
                                                                                          ascending = False
                                                                                          ).head(10)
    
    title3 = f'Top districts in {state3} by registered users in {year3}'

fig3 = px.bar(
              top_user_dist_df_filtered, 
              x='Registered_users', 
              y='District', 
              color='Registered_users', 
              color_continuous_scale='Greens', 
              orientation='h', 
              hover_name='District', 
              hover_data=['Registered_users']
              )

fig3.update_coloraxes(showscale=True, colorbar=dict(title='Registered Users', tickformat=',.0f'))

fig3.update_traces(
                   hovertemplate='<b>%{hovertext}</b><br>Registered users: %{x:,}<br>',
                   marker=dict(line=dict(width=0.5, color='Gray'))
                   )

fig3.update_layout(
                   height=500, width=950,
                   yaxis=dict(autorange="reversed"),
                   title={
                          'text': title3,
                          'x': 0.5,
                          'xanchor': 'center',
                          'y': 0.005,
                          'yanchor': 'bottom'
                          }
                   )

st.plotly_chart(fig3)

add_vertical_space(2)


#4


st.subheader(':blue[Number of app opens by District]')

col9, col10, buff2 = st.columns([5, 3, 7])

year_options = [year for year in st.session_state['years'] if year != 2018]

year4 = col9.selectbox('Year', options=year_options, key='year4')


if year4 == 2019:
    quarter_options.remove('1')
    
quarter4 = col10.selectbox("Quarter", options=quarter_options, key='quarter4')

map_user_df_filtered = map_user_df1[(map_user_df1["Year"]==year4)]

if quarter4 != 'All':
    map_user_df_filtered = map_user_df_filtered[map_user_df_filtered['Quarter']==int(quarter4)]

map_user_df_filtered = map_user_df_filtered[map_user_df_filtered["App_opens"] != 0]


fig4 = px.density_mapbox(
                         map_user_df_filtered,
                         lat='Latitude', lon='Longitude',
                         z='App_opens', radius=20,
                         center=dict(
                                     lat=20.5937,
                                     lon=78.9629
                                     ),
                        zoom=3, hover_name='District',
                        mapbox_style="stamen-watercolor",
                        opacity=0.8,
                        hover_data={
                                    'Latitude': False,
                                    'Longitude': False,
                                    'State': True
                                    }
                        )

fig4.update_layout(
                   margin=dict(l=20, r=20, t=60, b=20),
                   mapbox=dict(layers=[
                                       dict(
                                            sourcetype='geojson',
                                            source=st.session_state['geojson'],
                                            type='line',
                                            color='white',
                                            opacity=0.8,
                                            )
                                        ]
                               ),
                   width=925, height=600,
                   title={
                          'text': 'App Opens Density Map',
                          'x': 0.43,
                          'xanchor': 'center',
                          'y': 0.09,
                          'yanchor': 'bottom'
                          }
                   )

st.plotly_chart(fig4)