import streamlit as st
import plotly.express as px


st.set_page_config(page_title = 'Users', layout = 'wide', page_icon = 'Related Images and Videos/Logo.png')
st.title(':blue[Users]')

# Load the necessary dataframes from session state
agg_user_df1 = st.session_state["agg_user_df"]
map_user_df1 = st.session_state["map_user_df"]
top_user_dist_df1 = st.session_state["top_user_dist_df"]
top_user_pin_df1 = st.session_state["top_user_pin_df"]

col1, col2, col3 = st.columns([5, 3, 1])
state1 = st.selectbox('Select State', options=st.session_state['states'], key='state1')
year1 = st.selectbox('Select Year', options=st.session_state['years'], key='year1')
quarter_options = ["All"] + list(map(str, st.session_state['quarters']))
quarter1 = st.selectbox("Quarter", options=quarter_options, key='quarter1')


agg_user_df_filtered = agg_user_df1[(agg_user_df1['State'] == state1) & (agg_user_df1['Year'] == year1)]
if quarter1 != 'All':
    agg_user_df_filtered = agg_user_df_filtered[agg_user_df_filtered['Quarter'] == int(quarter1)]


fig1 = px.treemap(
    agg_user_df_filtered,
    path=['Brand'],
    values='Transaction_count',
    color='Percentage',
    color_continuous_scale='Viridis',
    hover_data={'Percentage': ':.2%'},
    hover_name='Brand'
)

fig1.update_layout(margin=dict(l=20, r=20, t=60, b=20))
fig1.update_layout(title='Transaction Count and Percentage by Brand', width=975, height=600,coloraxis_colorbar=dict(tickformat='.1%'))
fig1.update_layout(title={'x': 0.45, 'xanchor': 'center', 'y': 0.95, 'yanchor': 'top'})

st.plotly_chart(fig1)



# Add "All" option to state options
state_options = ['All'] + [state for state in st.session_state['states']]
quarter_options = ["All"] + list(map(str, st.session_state['quarters']))

# get user inputs for state, year, and quarter
state2 = st.selectbox('Select State', options=state_options, key='state2')
year2 = st.selectbox('Select Year', options=st.session_state['years'], key='year2')
quarter2 = st.selectbox("Quarter", options=quarter_options, key='quarter2')

if state2 == 'All':
    map_user_df_filtered = map_user_df1.copy()
else:
    map_user_df_filtered = map_user_df1[(map_user_df1["State"] == state2) & (map_user_df1["Year"] == year2)]
    if quarter2 != 'All':
        map_user_df_filtered = map_user_df_filtered[map_user_df_filtered['Quarter'] == int(quarter2)]


# create a scattergeo plot to display registered users by district

fig2 = px.scatter_mapbox(map_user_df_filtered, 
                      lat="Latitude", 
                      lon="Longitude", 
                      size="Registered_users", 
                      hover_name="District",
                      title=f"Registered Users by District"
                     )
fig2.update_geos(fitbounds='locations', visible=False)
fig2.update_layout(height=600, width=800, coloraxis_colorbar=dict(thickness=20, len=0.5))

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
                    'y': 0.05,
                    'yanchor': 'bottom'
                }
                  )

fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig2)


state3 = st.selectbox('Select State', options = state_options, key='state3')
year3 = st.selectbox('Select Year', options = st.session_state['years'], key='year3')

# filter data based on user inputs
if state3 == "All":
    top_user_dist_df_filtered = top_user_dist_df1[top_user_dist_df1['Year']==year3].groupby('District').sum().reset_index()
    top_user_dist_df_filtered = top_user_dist_df_filtered.sort_values(by = 'Registered_users', ascending = False).head(10)
    fig_title = f'Top 10 districts across all states by registered users in {year3}'
else:
    top_user_dist_df_filtered = top_user_dist_df1[(top_user_dist_df1['State']==state3) & (top_user_dist_df1['Year']==year3)]
    top_user_dist_df_filtered = top_user_dist_df_filtered.groupby('District').sum().reset_index().sort_values(by = 'Registered_users', ascending = False).head(10)
    fig_title = f'Top 10 districts in {state3} by registered users in {year3}'

# create bar chart
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
fig3.update_layout(title=fig_title)
fig3.update_layout(height=600, width=800)
fig3.update_traces(marker=dict(line=dict(width=0.5, color='Gray')))
fig3.update_coloraxes(showscale=True, colorbar=dict(title='Registered Users', tickformat=',.0f'))
fig3.update_traces(hovertemplate='<b>%{hovertext}</b><br>Registered users: %{x:,}<br>')
st.plotly_chart(fig3)





year_options = [year for year in st.session_state['years'] if year != '2018']
year4 = st.selectbox('Select Year', options=year_options, key='year4')

quarter_options = ['All'] + [str(q) for q in st.session_state['quarters']]
if year4 == '2019':
    quarter_options.remove('1')
quarter4 = st.selectbox("Quarter", options=quarter_options, key='quarter4')

map_user_df_filtered = map_user_df1[(map_user_df1["Year"]==year4)]
if quarter4 != 'All':
    map_user_df_filtered = map_user_df_filtered[map_user_df_filtered['Quarter']==int(quarter4)]
map_user_df_filtered = map_user_df_filtered[map_user_df_filtered["App_opens"] != 0]


fig4 = px.density_mapbox(map_user_df_filtered, lat='Latitude', lon='Longitude', z='App_opens',
                        radius=20, center=dict(lat=20.5937, lon=78.9629), zoom=3,
                        hover_name='District',
                        mapbox_style="stamen-watercolor",
                        opacity=0.8, hover_data={'Latitude': False, 'Longitude': False, 'State': True}
                        )
fig4.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                  mapbox=dict(layers=[dict(sourcetype='geojson',                                            source=st.session_state['geojson'],
                                            type='line',
                                            color='white',
                                            opacity=0.8,
                                            )],
                             ),
                  )

fig4.update_layout(margin=dict(l=20, r=20, t=60, b=20))
fig4.update_layout(title='App Opens Density Map', width=975, height=600)

st.plotly_chart(fig4)