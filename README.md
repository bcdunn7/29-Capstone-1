# InfluenceF1

#### Deployed here: 

### **Function:**
 * This website is a stat site for certain seasons of the FIA Formula 1 world championship
 * The site displays results and standings data from the Ergast API for seasons which had extremely close standings, especially those where a dramatic or controversial event determined the result of the chamionship
 * The site has two main 'modes'
 - A 'Replay Mode' where users can navigate through a given season race by race to see where the crucial points were scored. Certain races also have information on dramatic or controversial moments that occured in a race.
 - Those dramatic moments are then taken over to the 'Simulator' mode where users are able to toggle the events 'on and off' to see how those moments changed the result of the season. The toggle arrangement for each season can be saved to the user account and will automatically load in the next time that user visits the simulator


### **API and Race Data:** 
* https://ergast.com/mrd/
* The data for the seasons, races, drivers is all found in the ergast API. No active calls are made, the data is all gathered during app deployment. 
* Information for 'changes' (the toggles in the simulator) was supplied by me.


### **Tech Stack:**
* **Front end** is written in JavaScript. The chart is supplied using Chart.JS, though manipulation of chart data was all vanilla JS. jQuery and Bootstrap were used as well, though much of the styling was written in stand-alone CSS.
* **Back end** is written in Python(Flask) with PostgreSQL as the database manager. SQLAlchemy was used as the Flask-Postgres object-relational mapper. Flask-wtforms was used for the few user forms and CSRF security needed.
