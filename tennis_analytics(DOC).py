#Importing Required Libraries
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
        port=3306
    )
    cursor = conn.cursor()
except mysql.connector.Error as e: 
    #Catches any exceptions thrown by the mysql.connector.connect() function if the connection fails. 
    #The error message is stored in variable e
    st.error(f"Database connection failed: {e}") #Display error in Streamlit UI
    st.stop() #Stop app execution if connection fails


#Home Page Content
selected_page = st.sidebar.radio("Select a page", ["Home", "Search", "Ranking Overview", "Top Movers", "Country-wise Filter", "Competitor Comparison"])

#Displays a sidebar radio button with six page options
#Stores the user’s selected page in the variable selected_page
#Allows the app to render different content dynamically based on selection

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

    #Uses Python's datetime to get the current hour
    #Displays a custom greeting based on the time of day (Morning, Afternoon, or Evening)     

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

#2. Search Page
#Search Page: Allows users to search for competitors by name or ID
elif selected_page == "Search":
    st.subheader("🔍 Search Competitors")  #Subheader for the Search section
    search_query = st.text_input("Enter competitor name or ID")  #Text input to search by name or ID
    #Provides a text input box where users can type a competitor's name or ID to search

    if search_query:
        #SQL query to search competitors by name or ID (using LIKE for partial matching)
        query = f"""
    SELECT DISTINCT co.competitor_id, co.name, co.country, 
           co.country_code, co.abbreviation, 
           r.ranks, r.points, r.movement, r.competitions_played
    FROM competitors_table co
    LEFT JOIN competitor_ranking_table r ON co.competitor_id = r.competitor_id
    WHERE (co.name LIKE '%{search_query}%' OR co.competitor_id LIKE '%{search_query}%')
      AND co.week = (SELECT MAX(week) FROM competitors_table)
"""
        #competitors_table (co)
        #competitor_ranking_table (r)
        #LEFT JOIN - Ensures competitors are shown even if they don't have rankings yet

        cursor.execute(query)  #Executing the query
        results = cursor.fetchall()  #Fetching all the results
        
        #competitors_table (alias co)
        #competitor_ranking_table (alias r)
        #LEFT JOIN - Make sure all competitors are shown even if they don't have rankings
        #LIKE operator allows partial match searching

        if results:  # If there are results
            # Define the columns for the DataFrame
            columns = [
                "Competitor ID", "Name", "Country", "Country Code", 
                "Abbreviation", "Rank", "Points", "Movement", "Competitions Played"
            ]
            #Specifies the column names to be used for displaying the data

            df = pd.DataFrame(results, columns=columns)  #Create DataFrame from the results
            st.dataframe(df, use_container_width=True)  #Display the DataFrame in the app

            #Converts the SQL result into a Pandas DataFrame for easier display in Streamlit
            #Displays the DataFrame (table) interactively on the Streamlit page using the full width of the container

        else:  # If no results are found
            st.info("No results found.")  #Display a message if no results are found

#Short Note: Search Page          
#User Input: Users type a competitor's name or ID in the search box.
#SQL Query: The query searches for matches in the competitors_table and competitor_ranking_table based on the input.

#3) Ranking Overview Page
elif selected_page == "Ranking Overview":
    st.subheader("🏅 Ranking Overview")

    try:
        # Step 1: Get the latest available week dynamically from the database
        cursor.execute("SELECT MAX(week) FROM competitors_table;")
        current_week = cursor.fetchone()[0]  # Extract the latest week value
        
        #Executes an SQL query to get the most recent week (maximum week value) from the competitors_table
        #fetchone()[0] retrieves the first value from the query result.
        if current_week is None:
            st.error("No weekly data found in the database.")

            #If the table is empty or the week is None, it shows an error message in the UI

        else:
            # Step 2: Use parameterized query to fetch ranking data for the latest week
            query = """
                SELECT
                    cr.ranks,                      -- Rank of the competitor
                    cr.movement,                   -- Rank movement (up/down)
                    cr.points,                     -- Points of the competitor
                    co.name AS competitor_name,    -- Competitor name
                    co.country,                    -- Competitor country
                    co.week                        -- Week of the ranking
                FROM competitor_ranking_table cr
                JOIN competitors_table co ON cr.competitor_id = co.competitor_id
                WHERE co.week = %s                -- Filter data for the latest week only
                ORDER BY cr.ranks ASC;            -- Order results by ascending rank
            """
            cursor.execute(query, (current_week,))  # Pass current_week safely
        
            #SQL query to fetch ranking data for the latest week.
            #It joins the competitor_ranking_table (cr) with competitors_table (co) to include name, country, and week.
            #Uses WHERE co.week = %s to get only the latest week’s data (parameterized for safety).
            #Results are sorted by rank in ascending order.
            #Executes the query with current_week passed safely as a parameter to prevent SQL injection 


        #Fetch the query results
        ranking_data = cursor.fetchall() #Retrieves all rows returned by the query and stores them in ranking_data

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

            #Creates a Plotly bar chart to visualize competitor points.
            #X-axis: Competitor, Y-axis: Points, grouped by Country for color.
            #Chart is shown in the app using st.plotly_chart()

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
# SQL Query: Fetches ranking data for the current week and sorts by rank.
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
            
            #Subquery gets the latest week per competitor
            #Joins with the main table to focus only on the most recent data for each competitor
                       
            JOIN competitors_table co
                ON co.competitor_id = cr.competitor_id           # Join with the competitors table
                AND co.week = latest.latest_week                 # Ensure we get the latest data for each competitor
            
            #Joins again with competitors_table to get competitor name and country for the latest week only
                       
            WHERE cr.movement IS NOT NULL                        # Filter out null movements
            ORDER BY ABS(cr.movement) DESC                       # Order by largest movement (absolute value)
            LIMIT 50;                                            # Limit results to top 50 movers
        """)
            #Filters out rows where movement is null (to avoid errors or irrelevant rows)
            #Sorts by absolute movement (so both +ve and -ve are included)
        
            
        # Fetch the query results
        movers = cursor.fetchall()   #Executes the query and stores the result as a list of tuples

        # Check if there are no results
        if not movers:
            st.error("No data found or join issue.") #Displays an error if the result is empty (due to join issues or missing data)

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
#Page Title and Section Header

elif selected_page == "Country-wise Filter":
    st.subheader("🌍 Country-wise Performance Filter")

    #Function to get the list of distinct countries from the database
    def get_country_list():
        cursor.execute("SELECT DISTINCT country FROM competitors_table;")
        countries = cursor.fetchall()
        return [country[0] for country in countries]
    #Fetches a list of unique countries from the competitors_table
    #Returns a clean list of country names for use in the dropdown

    #Function to get the latest available week number from the table
    def get_latest_week():
        cursor.execute("SELECT MAX(week) FROM competitors_table;")
        latest_week = cursor.fetchone()[0] or 0
        st.write(f"Latest Week in the Database: {latest_week}")  #Debugging
        return latest_week
    #Queries the maximum (latest) week available in the database
    #Displays it on the screen for debugging purposes

    #Function to get competitors by country with optional current week filtering
    def get_competitors_by_country(selected_country, current_week_only=False):
        current_week = get_latest_week()  #Retrieves the latest week dynamically
        
        if current_week_only:
            #Filter only by the current week
            st.write(f"Filtering for Current Week: {current_week}")  # Debugging
            cursor.execute("""
                SELECT co.competitor_id, co.name, MIN(cr.ranks) AS rank, MAX(cr.points) AS points
                FROM competitors_table co
                JOIN competitor_ranking_table cr 
                ON co.competitor_id = cr.competitor_id
                WHERE co.country = %s AND co.week = %s
                GROUP BY co.competitor_id, co.name
                ORDER BY rank ASC;                #Orders results by rank ascending
            """, (selected_country, current_week))
            #Filters data for the selected country and only the current week
            #Joins ranking and competitor tables
            #Uses aggregation (MIN, MAX) to get a single rank and point value per player

        else:
            #Filter by the most recent week across all competitors
            st.write(f"Filtering for Most Recent Week for Competitors: {current_week}")  # Debugging
            cursor.execute("""
                SELECT co.competitor_id, co.name, MIN(cr.ranks) AS rank, MAX(cr.points) AS points
                FROM competitors_table co
                JOIN (
                    SELECT competitor_id, MAX(week) AS latest_week
                    FROM competitors_table
                    GROUP BY competitor_id
                ) latest_weeks ON co.competitor_id = latest_weeks.competitor_id AND co.week = latest_weeks.latest_week
                JOIN competitor_ranking_table cr 
                ON co.competitor_id = cr.competitor_id
                WHERE co.country = %s
                GROUP BY co.competitor_id, co.name
                ORDER BY rank ASC;
            """, (selected_country,))
        #Joins competitor table with a subquery that gets the latest week for each player
        #Retrieves the most recent data regardless of the global current week
        #Filters by selected country and orders players by best ranks

        return cursor.fetchall()

    #Fetch the list of countries
    country_list = get_country_list() #Calls the function to get all available countries

    if country_list:
        #Country dropdown
        selected_country = st.selectbox("Select Country", country_list)

        # Toggle to filter current week data
        filter_current_week = st.checkbox("Show Current Week Only") #Adds a checkbox toggle to filter only current week data or allow most recent week per competitor

        #Fetch data based on country and filter
        competitors_data = get_competitors_by_country(selected_country, filter_current_week) #Calls the main function with the user’s choices

        if competitors_data:
            #Convert data to DataFrame
            df = pd.DataFrame(competitors_data, columns=["Competitor ID", "Name", "Rank", "Points"])
            st.dataframe(df)
        #If results are returned, convert to a DataFrame and display

            #Create a bar chart to visualize rankings and points
            fig = px.bar(df, x="Name", y="Points", color="Rank",
                         title=f"Competitor Rankings for {selected_country}",
                         labels={"Points": "Points", "Rank": "Rank"})
            st.plotly_chart(fig)
        else:
            st.warning(f"No data found for {selected_country}.")
    else:
        st.warning("No countries found in the database.")

    #If no data is found for the selected country, a warning message is displayed saying "No data found for {selected_country}".

#Country-wise Filter: Allows users to explore the performance of competitors from different countries, displaying their rankings and points for a quick overview of the top players from each country.

#6)Competitor Comparison: 
# Define the competitor comparison page logic
if selected_page == "Competitor Comparison":
    st.subheader("🔄 Competitor Comparison")

    #Fetches all distinct competitor names from the database and sorts them alphabetically
    cursor.execute("SELECT DISTINCT name FROM competitors_table ORDER BY name ASC")
    competitors = sorted(set([row[0] for row in cursor.fetchall()]))
    #Provides two dropdowns for the user to select two different competitors for comparison
    competitor1 = st.selectbox("Select First Competitor", competitors)
    competitor2 = st.selectbox("Select Second Competitor", competitors, index=1)

    if competitor1 and competitor2 and competitor1 != competitor2:  #Ensures both selections are not empty and not the same
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
        #Executes the query with the selected names and stores the result

        if results:
            df_static = pd.DataFrame(results, columns=[ 
                "Competitor", "Country", "Country Code", "Abbreviation", 
                "Rank", "Points", "Movement", "Competitions Played"
            ]).drop_duplicates()
        #Converts the results into a DataFrame for further visualization and drops duplicates

            st.dataframe(df_static) #Displays the DataFrame in the Streamlit app

            # 📊 Points Bar Chart
            st.plotly_chart(px.bar(            #Creates and displays a bar chart comparing points
                df_static, x="Competitor", y="Points", color="Country", 
                title="Points Comparison", text="Points"
            ))

            # 📊 Movement Bar Chart
            st.plotly_chart(px.bar(            #Bar chart comparing movement in ranks
                df_static, x="Competitor", y="Movement", color="Country", 
                title="Rank Movement Comparison", text="Movement"
            ))

            # 🕸️ Radar Chart
            radar_df = df_static[["Competitor", "Rank", "Points", "Movement", "Competitions Played"]].set_index("Competitor")
            radar_df = radar_df.transpose().reset_index().rename(columns={'index': 'Metric'})
            #Transforms data to create a radar chart, where metrics are plotted around a circle

            fig_radar = go.Figure()
            for competitor in radar_df.columns[1:]:
                fig_radar.add_trace(go.Scatterpolar(
                    r=radar_df[competitor],
                    theta=radar_df['Metric'],
                    fill='toself',
                    name=competitor
                ))
            #Loops through each competitor and adds them to the radar chart

            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True)),
                showlegend=True,
                title="Competitor Radar Chart"
            )
            st.plotly_chart(fig_radar)
            #Sets layout and displays the radar chart

            # 📈 Rank Trend Over Time - no duplicates
            trend_query = """
                SELECT DISTINCT co.name, co.week, cr.ranks
                FROM competitors_table co
                JOIN competitor_ranking_table cr ON co.competitor_id = cr.competitor_id
                WHERE co.name IN (%s, %s)
                ORDER BY co.name, co.week
            """
            #Query to get weekly ranking trend data for both competitors

            cursor.execute(trend_query, (competitor1, competitor2))
            trend_data = cursor.fetchall()
            #Executes the query and fetches trend data

            if trend_data:
                df_trend = pd.DataFrame(trend_data, columns=["Competitor", "Week", "Rank"]).drop_duplicates()
                st.plotly_chart(px.line(
                    df_trend, x="Week", y="Rank", color="Competitor", markers=True,
                    title="Weekly Rank Trend"
                )) #Displays a line chart showing how rankings change over time for both competitors.
            else:
                st.warning("No trend data available for the selected players.")
        else:
            st.warning("No comparison data available.")
    elif competitor1 == competitor2:
        st.info("Please select two different competitors.")
    #Displays appropriate warnings if data is unavailable or if the same competitor is selected

    # Example competitor data for metrics selection
    data = {
        'Metric': ['Rank', 'Points', 'Matches Played', 'Wins'],
        'Competitor A': [5, 3200, 30, 22],
        'Competitor B': [3, 4100, 35, 26]
    }
    #Hardcoded dataset for extra comparison, used to demonstrate metric-based selection
    #Hardcoded dataset - Visual Demo Purposes 
    #To enable metric-based radar chart comparisons even if the database doesn’t have all metrics
    #It helps simulate full feature capability for presentation and testing

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
    #Creates another radar chart with filtered metrics

    # Layout and export options
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True   #Legend is the box that appears on the side or bottom of a chart and shows which color or shape corresponds to which data series
    )                     #Setting showlegend=True tells Plotly to display the legend, so users can clearly see which color represents which competitor in the radar plot
    #Sets layout for clarity and interactivity

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
    #Generates and offers a download button for the radar chart image

    # Export Comparison Data as CSV
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(label="📄 Download Comparison Data (CSV)", data=csv_data, file_name="comparison_data.csv", mime="text/csv")

#Bar Charts: For comparing points and movement.
#Radar Chart: To compare multiple metrics visually in a circular layout.
#Line Chart: To show how ranks changed over weeks


#Two Radar Charts Used:
   #One radar chart is generated from live database data
   #Another from sample static data with selectable metrics
   #This gives users both real and customizable comparisons

#Short Note: Competitor Comparison: Compares two players performance across different metrics like ranking, points, movement, and competitions played. It also includes a trend chart to see how their rankings have changed over time.

#Close connection after all pages are displayed
conn.close()