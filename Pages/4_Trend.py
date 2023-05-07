import streamlit as st
import plotly.express as px
import altair as alt


st.set_page_config(page_title = 'Trend Analysis', layout = 'wide', page_icon = 'Related Images and Videos/Logo.png')
st.title(':blue[Trend Analysis]')


state_groups = {
    'Northern Region': ['Jammu and Kashmir', 'Himachal Pradesh', 'Punjab', 'Chandigarh', 'Uttarakhand', 'Ladakh', 'Delhi', 'Haryana'],
    'Central Region': ['Uttar Pradesh', 'Madhya Pradesh', 'Chhattisgarh'],
    'Western Region': ['Rajasthan', 'Gujarat', 'Dadra and Nagar Haveli and Daman and Diu', 'Maharashtra'],
    'Eastern Region': ['Bihar', 'Jharkhand', 'Odisha', 'West Bengal', 'Sikkim'],
    'Southern Region': ['Andhra Pradesh', 'Telangana', 'Karnataka', 'Kerala', 'Tamil Nadu', 'Puducherry', 'Goa', 'Lakshadweep', 'Andaman and Nicobar Islands'],
    'North-Eastern Region': ['Assam', 'Meghalaya', 'Manipur', 'Nagaland', 'Tripura', 'Arunachal Pradesh', 'Mizoram']
}

# Add state group options
state_options = list(state_groups.keys())
state_group = st.selectbox('Select State Group', state_options, key='state_group')

# Filter data based on user input state group
selected_states = state_groups[state_group]
df = st.session_state['map_trans_df'][st.session_state['map_trans_df']['State'].isin(selected_states)]

# Create selectbox for user input state
state1 = st.selectbox('Select State', selected_states, key='state1')

# Filter data based on user input state
if state1 != 'All':
    df = df[df['State'] == state1]

    # Create selectbox for user input district
    district_options = list(df['District'].unique())
    district1 = st.selectbox('Select District', district_options, key='district1')

    # Filter data based on user input district
    if district1 != 'All':
        df = df[df['District'] == district1]
else:
    district1 = ''

# Create selectbox for user input year
year_options = ['All'] + [year for year in st.session_state['years']]
year1 = st.selectbox('Select Year', year_options, key='year1')

# Filter data based on user input year
if year1 != 'All':
    df = df[df['Year'] == year1]

# Filter data based on user inputs
if state1 == 'All':
    df = st.session_state['map_trans_df']

    if year1 != 'All':
        df = df[df['Year'] == year1]

# Create line chart for transaction count
fig1 = px.line(df, x='Quarter', y='Transaction_count', color='Year', title='Transaction Count Trend Analysis')
fig1.update_xaxes(tickmode='array', tickvals=list(range(1,5)))

fig2 = px.line(df, x='Quarter', y='Transaction_amount', color='Year', title='Transaction Amount Trend Analysis')
fig2.update_xaxes(tickmode='array', tickvals=list(range(1,5)))

tab1, tab2 = st.tabs(['🫰Transaction Count Trend', '💰Transaction Amount Trend'])

tab1.plotly_chart(fig1)
tab2.plotly_chart(fig2)


# Get user input for state, year, and quarter
state_options = ["All"] + list(st.session_state['states'])
year_options = st.session_state["years"]
quarter_options = ["All"] + list(st.session_state['quarters'])

state2 = st.selectbox("Select a state", state_options, key="state2")
year2 = st.selectbox("Select a year", year_options, key="year2")
quarter2 = st.selectbox("Select a quarter", quarter_options, key="quarter2")

# Filter the data based on user input
data = st.session_state["top_trans_dist_df"]
if state2 != "All":
    data = data[data["State"] == state2]
if year2:
    data = data[data["Year"] == year2]
if quarter2 != "All":
    data = data[data["Quarter"] == quarter2]

# Group the data by district and get the top 10 districts by transaction count
top_districts1 = data.groupby("District")["Transaction_count"].sum().nlargest(10).index.tolist()

# Filter the data to only include the top 10 districts
data1 = data[data["District"].isin(top_districts1)]

# Create the chart
chart1 = alt.Chart(data1).mark_bar(size=18).encode(
    x=alt.X("sum(Transaction_count)", title="Transaction Count"),
    y=alt.Y("District", sort=top_districts1, title=None),
    color="State",
    tooltip=["District", "State", "Year", "Quarter", "Transaction_count"]
).properties(
    title="Top 10 Districts by Transaction Count"
).configure_axis(
    labelFontSize=14, titleFontSize=16, labelPadding=8, labelAngle=0, 
    labelOverlap=True, grid=False, ticks=False
)

# Group the data by district and get the top 10 districts by transaction amount
top_districts2 = data.groupby("District")["Transaction_amount"].sum().nlargest(10).index.tolist()

# Filter the data to only include the top 10 districts
data2 = data[data["District"].isin(top_districts2)]

# Create the chart
chart2 = alt.Chart(data2).mark_bar(size=18).encode(
    x=alt.X("sum(Transaction_amount)", title="Transaction Amount"),
    y=alt.Y("District", sort=top_districts2, title=None),
    color="State",
    tooltip=["District", "State", "Year", "Quarter", "Transaction_amount"]
).properties(
    title="Top 10 Districts by Transaction Amount"
).configure_axis(
    labelFontSize=14, titleFontSize=16, labelPadding=8, labelAngle=0, 
    labelOverlap=True, grid=False, ticks=False
)
# Show the chart

tab3, tab4 = st.tabs(['🫰Transaction Count - Top Districts', '💰Transaction Amount - Top Districts'])
tab3.altair_chart(chart1, use_container_width=True)
tab4.altair_chart(chart2, use_container_width=True)




dist_trans = st.session_state['top_trans_dist_df']
pin_trans = st.session_state['top_trans_pin_df']

# Get the top 10 states by transaction volume
top_states = dist_trans.groupby('State')['Transaction_amount'].sum().reset_index().sort_values('Transaction_amount', ascending=False).head(10)

# Get the top 10 districts by transaction volume
top_districts = dist_trans.groupby('District')['Transaction_amount'].sum().reset_index().sort_values('Transaction_amount', ascending=False).head(10)

# Get the top 10 pincodes by transaction volume
top_pincodes = pin_trans.groupby('Pincode')['Transaction_amount'].sum().reset_index().sort_values('Transaction_amount', ascending=False).head(10)

# Define a function to filter the data based on the selected year and quarter
def filter_data(data, year, quarter):
    if quarter == 'All':
        filtered_data = data[data['Year'] == year]
    else:
        filtered_data = data[(data['Year'] == year) & (data['Quarter'] == quarter)]
    return filtered_data

# Get user inputs
trend3 = st.selectbox('Trend', ('Top 10 States by Transaction Volume', 'Top 10 Districts by Transaction Volume', 'Top 10 Pincodes by Transaction Volume'), key = 'trend3')

year3 = st.selectbox('Year', st.session_state["years"], key = 'year3')

quarter3 = st.selectbox('Quarter', quarter_options, key = 'quarter3')

# Filter the data based on the selected year and quarter
filtered_dist_trans = filter_data(dist_trans, year3, quarter3)
filtered_pin_trans = filter_data(pin_trans, year3, quarter3)

# Get the top 10 states by transaction volume for the selected year and quarter
filtered_top_states = filtered_dist_trans.groupby('State')['Transaction_amount'].sum().reset_index().sort_values('Transaction_amount', ascending=False).head(10)

# Get the top 10 districts by transaction volume for the selected year and quarter
filtered_top_districts = filtered_dist_trans.groupby('District')['Transaction_amount'].sum().reset_index().sort_values('Transaction_amount', ascending=False).head(10)

# Get the top 10 pincodes by transaction volume for the selected year and quarter
filtered_top_pincodes = filtered_pin_trans.groupby('Pincode')['Transaction_amount'].sum().reset_index().sort_values('Transaction_amount', ascending=False).head(10)


axis_format = '~s'

if trend3 == 'Top 10 States by Transaction Volume':
    chart = alt.Chart(filtered_top_states).mark_bar(size=18).encode(
        x=alt.X('Transaction_amount', axis=alt.Axis(format=axis_format)),
        y=alt.Y('State', sort='-x'),
        tooltip=['State', alt.Tooltip('Transaction_amount',
                                       format='$,.2f')]
    ).properties(
        title=f'Top 10 States by Transaction Volume ({year3} {quarter3})'
    )

elif trend3 == 'Top 10 Districts by Transaction Volume':
    chart = alt.Chart(filtered_top_districts).mark_bar(size=18).encode(
        x=alt.X('Transaction_amount', axis=alt.Axis(format=axis_format)),
        y=alt.Y('District', sort='-x'),
        tooltip=['District', alt.Tooltip('Transaction_amount',
                                          format='$,.2f')]
    ).properties(
        title=f'Top 10 Districts by Transaction Volume ({year3} {quarter3})'
    )

elif trend3 == 'Top 10 Pincodes by Transaction Volume':
    chart = alt.Chart(filtered_top_pincodes).mark_bar(size=18).encode(
        x=alt.X('Transaction_amount', axis=alt.Axis(format=axis_format)),
        y=alt.Y('Pincode', sort='-x'),
        tooltip=['Pincode', alt.Tooltip('Transaction_amount',
                                          format='.2f')]
    ).properties(
        title=f'Top 10 Pincodes by Transaction Volume ({year3} {quarter3})'
    )

# Render the chart
st.altair_chart(chart, use_container_width=True)