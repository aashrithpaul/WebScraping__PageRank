WEB CRAWLING and PAGE RANK PROJECT

Overview:
    This project implements web crawling techniques to gather data
    from web pages and then apply the page rank algorithm to determine
    importance of these web pages. The connections between webpages
    are visualized in a browser using D3.js


Technologies Used:
    - Programming Languages: Python, SQL, JS, HTML, CSS
    - Libraries: BeautifulSoup, D3.js
    - Database: DB Browser for SQLite
    - Data-Exchange: JSON


How it Works:
    - Crawling: Webpages are crawled by 'crawler.py' and 
    the database 'page_rank.sqlite' is populated.
    - PageRank: 'pagerank.py' retrieves data from DB, calculates
    page rank and update DB with new ranks.
    - Data-Exchange: 'json.py' converts the data in DB into 
    JSON format.
    - Process Data: 'webapp.js' uses JSON data as input and 
    computes data for visualization.
    - Visualization: visualized in browser using 'webapp.html'
    which is linked to 'webapp.css' and 'webapp.js' 

    (refer end of page in-depth working)


How to Install and Run:
    - Ensure Python is Installed on your system.
    - Ensure DB Browser for SQLite is installed on your system.
    - Create a new folder/repository and download the project files
    into the new repository.
    - Please make sure to download bs4 folder as well. If not, you
    can get download it from the web.    
    - Open the project folder in your IDE (I used VS Code)
    Execute the programs in the following order:
    -- 1. crawler.py 
        (you can input a website of your choice to start from)
    -- 2. pagerank.py
    -- 3. json.py (in visualization folder)
    -- 4. Open webapp.html in browser 

    The following programs are helpers:
    - x_cleardb.py: Run to clear the whole database. You can start 
    from step 1 and execute the whole project again.
    - x_resetrank.py: Run to reset all ranks to initial value of 1.
    Continue from step 2 for calculating the ranks again.


Credits: 
    I would like to acknowledge and extend my gratitude to 
    Prof. Charles Russel Severance and Michael Bostock whose 
    knowledge, insights and resources have greatly 
    contributed to the development of this project.



Detailed Working:
    - 1. crawler.py:
        -- This script requests input from the user for a website to 
        start crawling and the number of pages to crawl.
        -- Using the sqlite module, creates a database to store the 
        crawled webpages.
        -- Using the BeautifulSoup module, the webpages html is parsed
        and links from a page are checked and propulated into the 
        DB.
        -- From the DB selects a random link whose html is not parsed and 
        continues crawling.
        -- Note: Crawling of webpages is limited to the links which have the
        same domain name as the input, effectively limiting the scope to 
        relevant pages and reducing crawling to unwanted pages. 
        -- Exits the crawl once the nput no.of pages have been crawled or
        there if all links in DB are visited.
    - 2. pagerank.py:
        -- This uses the sqlite module to retrieve data from the DB to 
        compute rank.
        -- Requests user input for the number of iteration. More iterations
        give more precise results.
        -- The rank is computed using a basic version of the Google's
        Page Rank Algorithm.
        -- The rank of a page is distributed to its outbound links. The 
        surplus / deficit of the total of old ranks to the total of 
        new ranks is distribued among all the new ranks of webpages. 
        -- This ensures data is not lost during rank distribution.
        -- Computed new ranks are commited into the DB.
    - 3. json.py:
        -- Requests user input for the number of nodes to convert to JSON
        format.
        -- This script converts the data in DB to JSON format and writes
        it to a new file for front-end scripts (js and html) to read. 
        -- The data contains nodes (webpages and info) and  links i.e., 
        connections from one page to another.
        -- Note: I suggest using a smaller number for the input nodes so
        as to get a much clear visualization. Too many nodes and output
        is not a elegant. It will be clutted and there is less contrast 
        to clearly see the connections.
    - 4. webapp.js: 
        -- This script uses the D3 library to create a layout to plot the 
        connections between pages.
        -- It loads the newly created json data and computes the colour 
        and size of node based on the rank of the webpage.
    - 5. webapp.html:
        -- Loads all the scripts and their data. 
        -- Open this file in your browser to see the final results.


Limitations: 
    - BeautifulSoup (bs4) library can parse most of html pages but not all of them.
    - Many webpages use other laguages other than html (like xml, php) which 
    cannot be parsed by bs4.
    - Some sites have rate-limiters i.e., if a site is accessed too many times 
    by our code in a short span of time, access is denied for a priod of time.
    - Some have softwares in place to block crawlers. Such sites cannot be parsed.





            




