# Capstone 1 Proposal

## A Formula 1 'what if' stat site.

#### API: 
* https://ergast.com/mrd/

#### Goals:
 * The website would be a stat site for certain seasons of the FIA Formula 1 world championship
 * The site would display results and standings data from the Ergast API for seasons which had extremely close standings, especially those where a dramatic or controversial event determined the result of the chamionship
 * The goal of the site would be to show users how close the racing was, and then allow users to adjust certain races to show what could have been
    * This would be the extra, beyond CRUD feature as it would allow users to manually change different parts of the data to look at possible 'what if' senarios for different seasons  
  
#### Users and Demographics:
* The site would obviously be geared towards fans or members of the F1 community, or perhaps in some cases towards interested new fans as a way to learn about the sport
* But primarily it would be for committed fans who understand the dymanics of a season and would be able to appreciate and understand the way manipulating the data would have significant consequences on the chamionship standings

#### Data:
* The data would be supplied from Ergast and would incororate a subsection of the overall season finishing data
* The specifics (what year or drivers) is still to be decided but the data would be the finishing positions of two or more drivers over the course of a season


#### Creating the Project:
* Schema: One area I am struggling with is database shcema and use. I don't plan to have users or a log-in abiliity, it doesn't seem to be helpful for this application. Nor do I have posts, or content that would be created and saved beyond a browser session. So I'm unsure of what schema would be useful. I'm unaware if it would be better to just use API requests to gather the data each time, or if it would be better to request the data once and store it in a database and access it from there.
* Possible Issues: One possible issue is the request caps the API has set (4 a second or 200 an hour). 1 Request gets me all the data for a single driver for a whole season so I wouldn't imagine needing to make more than 2-3 within a second, and the 200/hr limit would only be reaching if someone was rapidly looking at repeated sets of data
* User flow: I'm still deciding between a multi-page application (1 for each season) or a single page with the ability to select between seasons to analyze. Either way, a user would select a season to analyze and then be taken or show the main page which would display a table of the season races with the ability to manipulate certain portions of the data to analyze 'what if' senarios.

#### Stretch goals:
* I have a few stretch goals, some of them far more possible than others.
* One, which should be managable, is to include a graph of the data on the page with the table for better UX
* Another, would be to link to article or even video clips (not sure how possible this is within time constraints) of the different seasons and dramatic events that would be analyzed