This section of the project contains the code for visualization of 
our data in a browser. 

D3.v2 visualization tool is used for this purpose. 

The code works as follows:
    1. json.py: 
        - takes no. of nodes for visualization as user input
        - reads website and page rank data from the Database
        - writes the data in JSON format in a new file named
        'prankJSON.js' 
        
    2. prankJSON.js:
        - contains the variable prankJSON with JSON data
        
    3. webapp.js:
        - sets up layout using D3.js
        - accepts json object as input
        - computes nodes, their radius, colour and creates link
        lines between nodes based on provided data

Run the 'json.py' file to see the data in a browser.

To change the number of nodes in output data, re-run the 'json.py'
file with a different input.

License:
    Please read LICENSE document. 

