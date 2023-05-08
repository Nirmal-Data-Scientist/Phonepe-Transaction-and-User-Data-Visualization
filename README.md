# Phonepe Pulse - Data Visualization Web App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://nirmal7781-phonepe-pulse-home-01h2v4.streamlit.app/)

The Phonepe Data Visualization project is a Python-based solution that extracts data from the Phonepe Pulse Github repository, transforms and stores it in a MySQL database, and displays it through an interactive dashboard using Streamlit, Plotly and few other visualization and data manipulation libraries. The solution includes multiple pages with various visualizations, allowing users to select different facts and figures to display. The project is efficient, secure, and user-friendly, providing valuable insights and information about the data in the Phonepe Pulse Github repository.

## Prerequisites

Before you begin, you will need to have a few tools and libraries installed on your machine:
* Python 3.7 or higher.
    [Note: Streamlit only supports .py files as of now. So, notebook(.ipynb) files are not recommended]
* Git software.
* MySQL software.
* The pandas, streamlit, plotly, seaborn, altair, and mysql-connector-python packages.

#### Python
Python is the programming language used to develop this project. It is a popular high-level programming language known for its readability and versatility. It is widely used for web development, data analysis, and machine learning. It provides a powerful and flexible foundation for working with data.

#### Git
Git is a version control system used for tracking changes in code. It is commonly used for collaborating on code and managing code changes. We used it here to clone the Pulse repository and extract the required data for analysis.

#### Pandas
Pandas is a popular Python library used for data manipulation and analysis. We used pandas to clean and preprocess the data, create new features, and perform data analysis. It provides a wide range of functions and methods for working with data.

#### MySQL
MySQL is an open-source relational database management system. We used it here to store and manage the cleaned and processed data. It provides a scalable and secure solution for managing large amounts of data.

#### Streamlit
Streamlit is an open-source Python library used for building web applications. We used it here to create a multi-page application for visualizing the data. It provides an intuitive and user-friendly interface for exploring and analyzing data.

#### Plotly
Plotly is a data visualization library used for creating interactive and dynamic plots. We used it here to create a variety of charts and visualizations, such as pie charts, bar charts, line plots, and choropleth maps. It provides a wide range of customization options and interactivity features.

#### Altair
Altair is a declarative data visualization library for Python. We used it here to create interactive visualizations using a grammar of graphics approach. It provides a simple and concise syntax for creating complex and dynamic visualizations.

## Features
* ##### Home Page: This page provides an overview of the app and its features, along with links to other pages.

* ##### Overview Page: This page displays various charts and graphs that give a summary of the transaction and user data using donut chart, bar plot and choropleth map.

* ##### Transaction Page: This page displays the transaction data using various filters such as state, year & quarter in the form of transaction hotspots and breakdowns.

* ##### User Page: This page allows users to explore the user data using various filters such as state, year and quarter treemap, choropleth and density mapbox

* ##### Trend Page: This page shows the trend of transaction count and amount over time, and allows users to compare different time periods using line and bar plots

* ##### Comparison Page: This page allows users to compare different regions, transaction types using facet grids, grouped bar and pie chart.

## User Guide

    1. Go to the web app URL in your web browser.
    2. Explore the features in every page of the app.
    3. Use the user friendly interface and give inputs as per your needs and get insightful visualizations.

## Developer Guide
  
To run the app, follow these steps:

    1. Clone the repository to your local machine using the following command: git clone [https://github.com/Nirmal7781/Phonepe_Pulse.git].
    2. Install the required libraries by running the following command: pip install -r requirements.txt.
    3. Run the .ipynb file to clean and transform the data and generate the eight CSV files.
    4. Create a MySQL database and tables, define constraints, and push data into MySQL using user-defined functions.
    5. Open a terminal window and navigate to the directory where the app is located using the following command: cd [Home.py file directory].
    6. Run the Streamlit app using the command [streamlit run Home.py] and access the app through the local URL provided.
    7. The app should now be running on a local server. If it doesn't start automatically, you can access it by going to either 
       * Local URL: [http://localhost:8501] or * Network URL: [http://192.168.43.83:8501].
    8. Explore the different pages of the app, enter inputs as required, and interact with the visualizations to gain insights into the PhonePe transaction data.

To modify the app, you can:

    1. Add new data sources or metrics to the dashboard.
    2. Customize the UI by modifying the existing components or creating new ones.
    3. Integrate the app with other data sources or APIs.
    4. Improve the performance of the app by optimizing the code or using caching techniques.

## Potential Applications

1. **Identifying trends and patterns**: Data scientists can use the app to identify trends and patterns in transaction data, such as which categories of transactions are increasing or decreasing in frequency.

2. **Conducting market research**: The app can be used to analyze transaction data to gain insights into consumer behavior and preferences, which can be valuable for conducting market research.

3. **Developing predictive models**: The insights gained from analyzing the transaction data can be used to develop predictive models, such as predicting future transaction volumes or identifying customers who are likely to churn.

4. **Monitoring business performance**: Data scientists can use the app to monitor the performance of various business metrics, such as transaction volume, revenue, and customer acquisition and retention.

5. **Improving customer experience**: By analyzing transaction data and identifying areas where customers are experiencing friction or challenges, data scientists can work with product teams to improve the customer experience and increase customer satisfaction.

## Web App Snap

<img width="956" alt="1 1" src="https://user-images.githubusercontent.com/123751119/236913668-de5143f7-40b9-467b-8ff9-cdc8a9ef666e.png">

<img width="960" alt="2" src="https://user-images.githubusercontent.com/123751119/236913757-dfe16f66-1fa8-4d72-a7a0-556419772d5c.png">

<img width="957" alt="3" src="https://user-images.githubusercontent.com/123751119/236913796-ccef8b7e-12ce-4db9-b2bb-528c1d780f33.png">

<img width="955" alt="4" src="https://user-images.githubusercontent.com/123751119/236913858-4f0d16c2-e5a7-4084-9cec-9f70f9a31243.png">

## Web App Demo Video

     <a href="https://www.linkedin.com/posts/nirmal-kumar-data-scientist_project-datavisualization-phonepe-activity-7061465588186972160-QQMx?utm_source=share&utm_medium=member_desktop" target="_blank">Demo Video</a>
     
## Streamlit web URL

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://nirmal7781-phonepe-pulse-home-01h2v4.streamlit.app/)

## Disclaimer

This application is intended for educational and research purposes only and should not be used for any commercial or unethical activities.

## Contact

If you have any questions, comments, or suggestions for the app, please feel free to contact me at [nirmal.works@outlook.com]
