# Importing Required Libraries
import streamlit as st           #For building the interactive web app interface
import mysql.connector           #To connect and interact with the MySQL database
import pandas as pd              #For data manipulation and analysis in tabular format
import plotly.express as px      #For creating interactive visualizations like line, bar, and pie charts
from datetime import datetime, timedelta #For handling and formatting date and time operations
import plotly.graph_objects as go #Customizing layouts, adding annotations, combining multiple chart types (like line + bar), or exporting static images.

# MySQL Connection with Error Handling
# Establishes a connection to the local MySQL database; if it fails, shows an error and stops the app
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sportanalytics",
        port=3314
    )
    cursor = conn.cursor()
except mysql.connector.Error as e:
    st.error(f"Database connection failed: {e}") #Display error in Streamlit UI
    st.stop() #Stop app execution if connection fails


#Home Page Content
selected_page = st.sidebar.radio("Select a page", ["Home", "Search", "Ranking Overview", "Top Movers", "Country-wise Filter", "Competitor Comparison"])

if selected_page == "Home":
    #Title of the homepage
    st.title("SportRadar Tennis Analytics")
    #Welcome message
    st.write("Welcome to the Tennis Analytics Dashboard powered by SportRadar! 🎾")
    #Display - Engaging description for the users
    st.write("Get in-depth tennis data with filters and analytics. 'Game on! 😎'")

    #Personalized Greeting
    current_hour = datetime.now().hour
    if current_hour < 12:
        st.write("🌞 Good Morning!")
    elif 12 <= current_hour < 18:
        st.write("☀️ Good Afternoon!")
    else:
        st.write("🌙 Good Evening!")

    # Home Page Content
    st.subheader("🏠 Home Dashboard")
    st.write("Welcome to the main dashboard! Navigate using the sidebar for all available analytics.")

    # Quick Guide or Tips
    with st.expander("📘 How to Use This Dashboard"):
        st.markdown(""" 
        - **Search**: Find specific players or tournaments.
        - **Top Movers**: See the performance changes of the top players.
        - **Ranking Overview**: Get insights into the overall rankings.
        - **Country-wise Analysis**: Filter players by country for specific insights.
        - **Competitor Comparison**: Compare two players' rankings, points, movement, and performance over time in one view.
        """) #Brief instructions on how to navigate the app

# 2. Search Page
#Search Page: Allows users to search for competitors by name or ID
elif selected_page == "Search":
    st.subheader("🔍 Search Competitors")  #Subheader for the Search section
    search_query = st.text_input("Enter competitor name or ID")  #Text input to search by name or ID

    if search_query:
        #SQL query to search competitors by name or ID (using LIKE for partial matching)
        query = f"""
            SELECT DISTINCT co.competitor_id, co.name, co.country, 
                   co.country_code, co.abbreviation, 
                   r.ranks, r.points, r.movement, r.competitions_played
            FROM competitors_table co
            LEFT JOIN competitor_ranking_table r ON co.competitor_id = r.competitor_id
            WHERE co.name LIKE '%{search_query}%' OR co.competitor_id LIKE '%{search_query}%'
        """
        cursor.execute(query)  #Executing the query
        results = cursor.fetchall()  #Fetching all the results

        if results:  # If there are results
            # Define the columns for the DataFrame
            columns = [
                "Competitor ID", "Name", "Country", "Country Code", 
                "Abbreviation", "Rank", "Points", "Movement", "Competitions Played"
            ]
            df = pd.DataFrame(results, columns=columns)  #Create DataFrame from the results
            st.dataframe(df, use_container_width=True)  #Display the DataFrame in the app
        else:  # If no results are found
            st.info("No results found.")  #Display a message if no results are found

#Short Note: Serach Page          
#User Input: Users type a competitor's name or ID in the search box.
#SQL Query: The query searches for matches in the competitors_table and competitor_ranking_table based on the input.

#3) Ranking Overview Page
elif selected_page == "Ranking Overview":
    st.subheader("🏅 Ranking Overview")

    try:
        #SQL Query: Fetch ranking data by joining competitor_ranking_table and competitors_table
        cursor.execute("""
            SELECT
                cr.ranks,             # Rank of the competitor
                cr.movement,          # Rank movement (up/down)
                cr.points,            # Points of the competitor
                co.name AS competitor_name,  # Name of the competitor
                co.country,           # Country of the competitor
                co.week               # Week of the ranking
            FROM competitor_ranking_table cr
            JOIN competitors_table co ON cr.competitor_id = co.competitor_id
            WHERE co.week = 16  # Use the current week, which is 16 for now
            ORDER BY cr.ranks ASC;  # Order by ranks in ascending order (lowest rank comes first)
        """)

        #Fetch the query results
        ranking_data = cursor.fetchall()

        #Check if no data is found
        if not ranking_data:
            st.error("No ranking data found for the current week.")
        else:
            #Convert the results into a DataFrame for better visualization
            df_ranking = pd.DataFrame(ranking_data, columns=["Rank", "Movement", "Points", "Competitor", "Country", "Week"])

            #Remove duplicates based on Competitor Name and Week
            df_ranking.drop_duplicates(subset=["Competitor", "Week"], keep="first", inplace=True)

            #Display the DataFrame as a table
            st.dataframe(df_ranking)

            #Create a bar chart to visualize the ranking data (Competitor vs Points)
            fig = px.bar(df_ranking, x="Competitor", y="Points", color="Country",
                         title="Ranking Overview", labels={"Points": "Points"})
            st.plotly_chart(fig)

            #Convert the DataFrame into CSV format for downloading
            csv = df_ranking.to_csv(index=False)  # Convert DataFrame to CSV without index

            #Provide a download button for the CSV file
            st.download_button(
                label="Download as CSV",     # Label of the button
                data=csv,                   # CSV data to download
                file_name="ranking_overview.csv",  # Name of the downloaded file
                mime="text/csv"             # MIME type for CSV files
            )

    except Exception as e:
        #Handle errors and display a message if something goes wrong
        st.error(f"Error loading ranking overview: {e}")

#Ranking Overview Page - Short Note
# SQL Query: Fetches ranking data for the current week (week 16) and sorts by rank.
# Data Processing: Converts the results into a DataFrame, removes duplicates, and displays the data.
# Visualization: Creates a bar chart showing competitors' points by country.
# CSV Download: Allows users to download the ranking data as a CSV file.


# 4)Top Movers Page
if selected_page == "Top Movers":
    st.subheader("🏆 Top Movers")  # Subheader for the page

    try:
        # SQL Query: Get the top 50 competitors with the largest movement in ranks.
        cursor.execute(""" 
            SELECT
                cr.ranks,              # Rank of the competitor
                cr.movement,           # Movement in rank (up or down)
                cr.points,             # Points of the competitor
                co.name AS competitor_name,  # Name of the competitor
                co.country,            # Country of the competitor
                co.week                # Week of the ranking
            FROM competitor_ranking_table cr
            JOIN (
                SELECT competitor_id, MAX(week) AS latest_week   # Get the latest week per competitor
                FROM competitors_table
                GROUP BY competitor_id
            ) latest
                ON cr.competitor_id = latest.competitor_id        # Join the competitor ranking table
            JOIN competitors_table co
                ON co.competitor_id = cr.competitor_id           # Join with the competitors table
                AND co.week = latest.latest_week                  # Ensure we get the latest data for each competitor
            WHERE cr.movement IS NOT NULL                        # Filter out null movements
            ORDER BY ABS(cr.movement) DESC                       # Order by largest movement (absolute value)
            LIMIT 50;                                            # Limit results to top 50 movers
        """)

        # Fetch the query results
        movers = cursor.fetchall()

        # Check if there are no results
        if not movers:
            st.error("No data found or join issue.")

        # Convert the results into a DataFrame for better visualization
        top_movers_df = pd.DataFrame(movers, columns=['ranks', 'movement', 'points', 'competitor_name', 'country', 'week'])

        # Remove duplicates based on Competitor Name and Week
        top_movers_df.drop_duplicates(subset=["competitor_name", "week"], keep="first", inplace=True)

        # Display the DataFrame in the app with a fixed height to allow scrolling
        st.dataframe(top_movers_df, height=500)  # Set a fixed height for scrolling functionality

        # Create a bar chart to visualize rank movement of top movers
        fig = px.bar(top_movers_df, x='competitor_name', y='movement', title="Top Movers - Movement", labels={'movement': 'Rank Movement', 'competitor_name': 'Competitor'})
        st.plotly_chart(fig)  # Display the chart

    except Exception as e:
        # Handle any exceptions (errors) that occur during data fetching or processing
        st.error(f"Error loading top movers: {e}")

#Top-Movers: Top Movers focusing specifically on players with substantial rank changes.
#Ranking Overview & Top Movers
#The Ranking Overview displays the rankings of all competitors for a given week, 
#whereas Top Movers emphasizes competitors who have had the most notable movements, either up or down.

# 5. Country-wise Filter Page
#Page Title and Description
elif selected_page == "Country-wise Filter":
    st.subheader("🌍 Country-wise Performance Filter")

    #Function to fetch the list of countries for the dropdown filter
    def get_country_list():
        cursor.execute("SELECT DISTINCT country FROM competitors_table;")
        countries = cursor.fetchall()
        return [country[0] for country in countries]
    #Function Purpose: Fetches a list of distinct countries from the competitors_table


    #Function to fetch competitors' data for the selected country
    def get_competitors_by_country(country):
        cursor.execute(""" 
        SELECT co.competitor_id, co.name, MAX(cr.ranks) AS rank, MAX(cr.points) AS points
        FROM competitors_table co
        JOIN competitor_ranking_table cr
        ON co.competitor_id = cr.competitor_id
        WHERE co.country = %s
        GROUP BY co.competitor_id, co.name
        ORDER BY rank ASC;
        """, (country,))
        return cursor.fetchall()
    #Function Purpose: Fetches competitor information (ID, name, rank, points) for a specific country.


    # Streamlit layout
    st.title('Tennis Analytics: Country-wise Competitor Ranking')

    #Fetch the list of countries for the dropdown
    country_list = get_country_list() #Calls the get_country_list() function to retrieve the list of countries from the database.
     
    # Dropdown for selecting a country
    selected_country = st.selectbox("Select Country", country_list) #Displays a dropdown (selectbox) to allow the user to choose a country from the list of countries.

    # Displaying the data for the selected country
    if selected_country:
        st.write(f"**Country**: {selected_country}")
        competitors_data = get_competitors_by_country(selected_country)
        #Calls the get_competitors_by_country(selected_country) function to fetch competitors' data for the selected country.


    #Check if Data Exists and Display it
        if competitors_data:
            # Convert to DataFrame for better display
            df = pd.DataFrame(competitors_data, columns=["Competitor ID", "Name", "Rank", "Points"])
            st.dataframe(df)
    #If competitor data is available, converts the data into a DataFrame (df) and displays it as a table in the app using st.dataframe().


            # Create a bar chart for country-specific ranking
            fig = px.bar(df, x="Name", y="Points", color="Rank",
                         title=f"Competitor Rankings for {selected_country}",
                         labels={"Points": "Points", "Rank": "Rank"})
            st.plotly_chart(fig)
            #Labels for Y-axis ("Points") and color ("Rank")
        else:
            st.warning(f"No data found for {selected_country}.")
    #If no data is found for the selected country, a warning message is displayed saying "No data found for {selected_country}".

#Country-wise Filter: Allows users to explore the performance of competitors from different countries, displaying their rankings and points for a quick overview of the top players from each country.

#6)Competitor Comparison: 
# Define the competitor comparison page logic
if selected_page == "Competitor Comparison":
    st.subheader("🔄 Competitor Comparison")

    # Fetch unique competitor names from the database
    cursor.execute("SELECT DISTINCT name FROM competitors_table ORDER BY name ASC")
    competitors = sorted(set([row[0] for row in cursor.fetchall()]))

    competitor1 = st.selectbox("Select First Competitor", competitors)
    competitor2 = st.selectbox("Select Second Competitor", competitors, index=1)

    if competitor1 and competitor2 and competitor1 != competitor2:
        # Query to fetch latest data for both competitors
        query_static = """
            SELECT 
                co.name AS Competitor, co.country, co.country_code, co.abbreviation,
                cr.ranks, cr.points, cr.movement, cr.competitions_played
            FROM competitors_table co
            JOIN competitor_ranking_table cr ON co.competitor_id = cr.competitor_id
            WHERE (co.name = %s OR co.name = %s)
              AND co.week = (
                  SELECT MAX(week) FROM competitors_table co2
                  WHERE co2.name = co.name
              )
        """
        cursor.execute(query_static, (competitor1, competitor2))
        results = cursor.fetchall()

        if results:
            df_static = pd.DataFrame(results, columns=[ 
                "Competitor", "Country", "Country Code", "Abbreviation", 
                "Rank", "Points", "Movement", "Competitions Played"
            ]).drop_duplicates()

            st.dataframe(df_static)

            # 📊 Points Bar Chart
            st.plotly_chart(px.bar(
                df_static, x="Competitor", y="Points", color="Country", 
                title="Points Comparison", text="Points"
            ))

            # 📊 Movement Bar Chart
            st.plotly_chart(px.bar(
                df_static, x="Competitor", y="Movement", color="Country", 
                title="Rank Movement Comparison", text="Movement"
            ))

            # 🕸️ Radar Chart
            radar_df = df_static[["Competitor", "Rank", "Points", "Movement", "Competitions Played"]].set_index("Competitor")
            radar_df = radar_df.transpose().reset_index().rename(columns={'index': 'Metric'})

            fig_radar = go.Figure()
            for competitor in radar_df.columns[1:]:
                fig_radar.add_trace(go.Scatterpolar(
                    r=radar_df[competitor],
                    theta=radar_df['Metric'],
                    fill='toself',
                    name=competitor
                ))

            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True)),
                showlegend=True,
                title="Competitor Radar Chart"
            )
            st.plotly_chart(fig_radar)

            # 📈 Rank Trend Over Time - no duplicates
            trend_query = """
                SELECT DISTINCT co.name, co.week, cr.ranks
                FROM competitors_table co
                JOIN competitor_ranking_table cr ON co.competitor_id = cr.competitor_id
                WHERE co.name IN (%s, %s)
                ORDER BY co.name, co.week
            """
            cursor.execute(trend_query, (competitor1, competitor2))
            trend_data = cursor.fetchall()

            if trend_data:
                df_trend = pd.DataFrame(trend_data, columns=["Competitor", "Week", "Rank"]).drop_duplicates()
                st.plotly_chart(px.line(
                    df_trend, x="Week", y="Rank", color="Competitor", markers=True,
                    title="Weekly Rank Trend"
                ))
            else:
                st.warning("No trend data available for the selected players.")
        else:
            st.warning("No comparison data available.")
    elif competitor1 == competitor2:
        st.info("Please select two different competitors.")

    # Example competitor data for metrics selection
    data = {
        'Metric': ['Rank', 'Points', 'Matches Played', 'Wins'],
        'Competitor A': [5, 3200, 30, 22],
        'Competitor B': [3, 4100, 35, 26]
    }

    df = pd.DataFrame(data)

    # Get metric list for dynamic selection
    metric_options = df['Metric'].tolist()
    selected_metrics = st.multiselect("Select metrics to compare:", metric_options, default=metric_options)

    # Filter based on selected metrics
    filtered_df = df[df['Metric'].isin(selected_metrics)]

    # Create radar chart figure
    fig = go.Figure()

    # Add traces for each competitor
    for competitor in filtered_df.columns[1:]:
        fig.add_trace(go.Scatterpolar(
            r=filtered_df[competitor],
            theta=filtered_df['Metric'],
            fill='toself',
            name=competitor
        ))

    # Layout and export options
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True
    )

    # Display chart with download options
    st.plotly_chart(fig, use_container_width=True, config={
        "displayModeBar": True,
        "toImageButtonOptions": {
            "format": "png",
            "filename": "competitor_comparison_chart",
            "height": 600,
            "width": 800,
            "scale": 1
        }
    })

    img_bytes = fig.to_image(format="png")
    st.download_button(label="📥 Download Radar Chart (PNG)", data=img_bytes, file_name="comparison_chart.png", mime="image/png")

    # Export Comparison Data as CSV
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(label="📄 Download Comparison Data (CSV)", data=csv_data, file_name="comparison_data.csv", mime="text/csv")


#Short Note: Competitor Comparison: Compares two players' performance across different metrics like ranking, points, movement, and competitions played. It also includes a trend chart to see how their rankings have changed over time.

# Close connection after all pages are displayed
conn.close()
