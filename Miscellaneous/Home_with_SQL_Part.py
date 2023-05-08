import io
import pandas as pd
import streamlit as st
import mysql.connector
import ydata_profiling
from streamlit_player import st_player
from streamlit_pandas_profiling import st_profile_report
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.add_vertical_space import add_vertical_space

st.set_page_config(page_title = 'PhonePe Data Visualization', layout = 'wide', page_icon = 'Related Images and Videos/Logo.png')

st.title(':blue[PhonePe Data Visualization]')

add_vertical_space(2)

st.write("""PhonePe has launched PhonePe Pulse, a data analytics platform that provides insights into how Indians are using digital payments.
         With over 30 crore registered users and 2000 crore transactions, PhonePe, India's largest digital payments platform with 46% UPI market share, has a unique ring-side view into the Indian digital payments story.
         Through this app, you can now easily access and visualize the data provided by PhonePe Pulse, gaining deep insights and interesting trends into how India transacts with digital payments.""")

add_vertical_space(2)

st_player(url = "https://www.youtube.com/watch?v=c_1H6vivsiA", height = 480)

add_vertical_space(2)

st.image('Related Images and Videos/1.png')

add_vertical_space(2)

# Retrieve the MySQL credentials from Streamlit Secrets

mysql_credentials = st.secrets["mysql"]; host = mysql_credentials["host"]; user = mysql_credentials["user"]
password = mysql_credentials["password"]; database = mysql_credentials["database"]

# Establish a connection to the MySQL database

conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

cursor = conn.cursor()

def get_dataframe(table_name):
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=[i[0] for i in cursor.description])
    df['Year'] = df['Year'].astype(str)
    return df

agg_trans_df = agg_user_df = map_trans_df = map_user_df = \
    top_trans_dist_df = top_trans_pin_df = top_user_dist_df = top_user_pin_df = None
    
table_names = [
    'agg_trans', 'agg_user', 'map_trans',
    'map_user', 'top_trans_dist', 'top_trans_pin',
    'top_user_dist', 'top_user_pin'
]

for table_name in table_names:
    var_name = f"{table_name}_df"
    globals()[var_name] = get_dataframe(table_name)

cursor.close()
conn.close()

# Key Metrics as cards

col1, col2, col3 = st.columns(3)

total_reg_users = top_user_dist_df['Registered_users'].sum()
col1.metric(label = 'Total Registered Users', value = '{:.2f} Cr'.format(total_reg_users/100000000), delta = 'Forward Trend')

total_app_opens = map_user_df['App_opens'].sum()
col2.metric(label = 'Total App Opens', value = '{:.2f} Cr'.format(total_app_opens/100000000), delta = 'Forward Trend')

col3.metric(label = 'Total Transaction Count', value = '2000 Cr +', delta = 'Forward Trend')

style_metric_cards()

add_vertical_space(2)

st.image('Related Images and Videos/pulse-video.gif', use_column_width = True)

if 'options' not in st.session_state:
    st.session_state['options'] = {
        'Aggregate Transaction': 'agg_trans_df',
        'Aggregate User': 'agg_user_df',
        'Map Transaction': 'map_trans_df',
        'Map User': 'map_user_df',
        'Top Transaction Districtwise': 'top_trans_dist_df',
        'Top Transaction Pincodewise': 'top_trans_pin_df',
        'Top User Districtwise': 'top_user_dist_df',
        'Top User Pincodewise': 'top_user_pin_df'
    }

if 'df_list' not in st.session_state:
    st.session_state['df_list'] = []
    
    for var_name in globals():
        if isinstance(globals()[var_name], pd.core.frame.DataFrame) and var_name.endswith('_df'):
            st.session_state[var_name] = globals()[var_name]
            st.session_state['df_list'].append(var_name)

col, buff = st.columns([2, 4])
option = col.selectbox(label='Data', options=list(st.session_state['options'].keys()), key='df')


tab1, tab2 = st.tabs(['Report and Dataset', 'Download Dataset'])

with tab1:
    
    column1, column2, buffer = st.columns([2, 2, 4])
    
    show_profile = column1.button(label = 'Show Detailed Report', key = 'show')
    show_df = column2.button(label = 'Show Dataset', key = 'show_df')
    
    if show_profile:
        df_name = st.session_state['options'][option]
        df = globals()[df_name]
        pr = df.profile_report()
        st_profile_report(pr)
        
    if show_df:
        st.experimental_data_editor(data = globals()[st.session_state['options'][option]], use_container_width=True)


with tab2:
    col1, col2, col3 = st.columns(3)
    
    df_name = st.session_state['options'][option]
    df = globals()[df_name]
    
    csv = df.to_csv()
    json = df.to_json(orient ='records')
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, engine ='xlsxwriter', index = False)
    excel_bytes = excel_buffer.getvalue()
    
    col1.download_button("Download CSV file", data = csv, file_name = f'{option}.csv', mime = 'text/csv', key = 'csv')
    col2.download_button("Download JSON file", data = json, file_name = f'{option}.json', mime = 'application/json', key = 'json')
    col3.download_button("Download Excel file", data = excel_bytes, file_name = f'{option}.xlsx',
                        mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', key = 'excel')