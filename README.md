# Game Analytics: **Unlocking Tennis Data with SportRadar API**

## Project Overview
The SportRadar Event Explorer project aims to develop a comprehensive solution for managing, visualizing, and analyzing sports competition data extracted from the Sportradar API. The application will parse JSON data, store structured information in a relational database, and provide intuitive insights into tournaments, competition hierarchies, and event details. This project is designed to assist sports enthusiasts, analysts, and organizations in understanding competition structures and trends while exploring detailed event-specific information interactively.

### Skills Acquired

- **Python Scripting:** Automated extraction, transformation, and loading (ETL) of sports data.
- **Data Collection via API Integration:** Seamless interaction with the Sportradar API for real-time data collection.
- **Data Management Using SQL:** Designing and managing relational databases.
- **Streamlit:** Creating dynamic dashboards and visual analytics for user interaction.

### Domain
**Sports/Data Analytics**

### Business Use Cases

- **Event Exploration:** Enable users to navigate through competition hierarchies (e.g., ATP Vienna events).
- **Trend Analysis:** Visualize the distribution of events by type, gender, and competition level.
- **Performance Insights:** Analyze player participation across singles and doubles events.
- **Decision Support:** Offer data-driven insights to event organizers or sports bodies for resource allocation.

### Project Setup in VS Code

**Step 1: Check or Install Python**
Make sure Python (preferably 3.10 or higher) is installed.

To check:

python --version
If not installed, download it from python.org

**Step 2: Set Up Python Environment**
Create a virtual environment to isolate the project dependencies:
python -m venv env

**Activation part:**
Windows Users ---> Windows: .\env\Scripts\activate
Mac/Linux: source env/bin/activate

**Step 3: Configure Python Path in VS Code**
- Open the project folder in VS Code.
- Open any .py file or your main.ipynb.
- In the bottom-left corner, will see the Python interpreter (EG: Python 3.13.2 64-bit).
- Click on it.

**Step 4: Install Required Packages**
If you have a requirements.txt, install all packages.
* In the Terminal - pip install -r requirements.txt

**Step 5: Organize Code Files**

**Use .ipynb files for:**
- Step-by-step exploration
- API testing
- Data analysis
- Prototyping workflows

**Use .py files for:**
- App logic (e.g., Streamlit interface)
- Script automation
- Reusable functions and modules

### Development Approach

**Data Extraction**
- Connect to the Sportradar API to retrieve competition data.
- Parse and extract relevant information from JSON responses.
- Transform nested JSON structures into flat, relational data suitable for analysis.

**Data Storage**
- Design a SQL database schema tailored to sports data.
- Define appropriate data types and relationships.
- Implement primary and foreign keys to maintain data integrity.
- Store parsed data for easy querying and analysis.

**Data Analysis & Visualization**
- Use Python libraries (e.g., Pandas, Matplotlib) to analyze stored data.
- Develop an interactive dashboard using Streamlit to:
- Visualize competition trends.
- Explore player participation and event distributions.

**Insights Delivery**
- Generate insights into competition structures and participation trends.
- Provide actionable recommendations for event organizers and sports analysts.

#### Technologies Used
##### Languages
*Python:* Core language for scripting, data processing, and API integration.

**SQL (MySQL):** For storing and querying structured tennis competition data.

#### Libraries & Frameworks
**Pandas:** For data manipulation and analysis.

**Plotly:** For creating interactive and responsive visualizations.

**Streamlit:** For building and deploying the web dashboard interface.

#### Applications & Tools
**Visual Studio Code (VS Code):** IDE used for writing and debugging code.

**XAMPP (MySQL Server):** Local server setup for MySQL database hosting.

##### APIs
**Sportradar Tennis API:** External data source providing real-time and historical tennis statistics.

#### Expected Outcomes
- A robust system for parsing and storing sports data.
- Intuitive dashboards for exploring competition hierarchies and trends.
- Actionable insights to aid sports decision-making processes.

#### Repository Structure
/README.md       # Project documentation
/data                     # Raw and processed data files 
/scripts                 # Python scripts for API integration and data processing
/database             # SQL schema and database files
/dashboard          # Streamlit application files

**/README.md**
The README.md file provides an introduction to the project, explains how to set it up and use it, lists its features and technologies, and offers guidelines for contributing. It serves as the primary documentation for developers and users to understand the project's purpose, functionality, and setup.

**.md = Markdown file format.**
It’s typically used for project documentation.

**Why it’s used in GitHub?**
GitHub automatically renders .md files in a formatted way, which is why README.md files are shown with nice formatting when you visit a repository.

**/data**
The data directory contains all raw and processed data files used in the project. This may include data fetched from the API, intermediate transformations, or cleaned data that is ready for analysis.

**Why it’s used?**
This folder helps to separate your data from code files, keeping the project organized. It makes it easier for collaborators to access and understand data storage without affecting the functionality of the application.

**/scripts**
The scripts folder houses all Python scripts responsible for API integration, data extraction, transformation, and loading (ETL). This includes the logic for interacting with the SportRadar API, cleaning the fetched data, and storing it in a structured database.

**Why it’s used?**
By keeping scripts in a separate folder, the project is organized and modular. It allows you to maintain and update your codebase without cluttering other parts of the project.

**/database**
The database folder contains the SQL schema files and other database-related resources. This can include .sql files for setting up tables, constraints, and relations, as well as scripts for managing database migrations or backups.

**Why it’s used?**
This folder centralizes your database-related resources, helping you quickly update and manage your database schema and any SQL queries needed to work with the data.

**/dashboard**
The dashboard folder holds the Streamlit application files. These files are responsible for creating interactive visualizations, dashboards, and user interfaces. It typically includes .py files with Streamlit code for presenting the data in a user-friendly way.

**Why it’s used?**
It separates the code related to the visualization and user interface from the rest of the project, making it easier to maintain and update the dashboard without interfering with backend processes.

#### Getting Started
- Clone this repository.
- Install the required Python libraries from requirements.txt.
- Obtain API access credentials from Sportradar.
- Run the data extraction script to populate the database.
- Launch the Streamlit dashboard to explore insights interactively.

#### API Endpoint Configuration and Access Details

- **API Key:** uTdw18HoNI3f8JZtcHNxtd8V1VxvGrIqQ9QoGh9y
- **Endpoint:** https://api.sportradar.com/tennis/{access_level}/{version_number}/{language_code}/competitions.{format}
- **Access Level:** trial
- **Version:** v3
- **Language Code:** en
- **Status Code:** 200

#### Usage: How to Run the Project

To run the project, open the terminal and use the following command:
streamlit run your_dashboard_file.py

**Example** - streamlit run tennis_analytics.py

#### Optional Enhancements (Planned for Future Releases)
- **Notification system for ranking changes** - Alert users when a competitor's rank changes.
- **Geo-visualizations based on country stats** - Display insights using interactive maps for country-wise analysis.
- **Mobile-responsive Streamlit interface** - Enhance usability across mobile and tablet devices.

**Conclusion**

This project brings together data collection, processing, and visualization to make tennis analytics accessible and insightful.

#### Acknowledgements
**Sportradar** - https://developer.sportradar.com/tennis/reference/competitions

**Streamlit Documents** - https://docs.streamlit.io/develop/api-reference/widgets/st.slider

**Author**
**Bala Sowntharya Bala Subramanian**
