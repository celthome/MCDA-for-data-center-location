# MCDM for data center location

## Introduction

Data storage emerges as one of the most rapidly expanding industries globally. With each LLM prompt consuming 60 times more energy than a Google prompt. 
153,520,000,000,000,000,000,000 bytes 
That is the estimated amount of data generated in 2024. That is 153 trillion GB, also equals to 153 Zettabyte.
Thererfore, we had the mission this question:

**How can we use geoinformation apporaches to determine possible data center sites, while minimizing the environmental impact?**

<img width="527" alt="flowchart" src="https://github.com/celthome/MCDA-for-data-center-location/assets/146074360/9d875919-2116-47f8-980e-6e54f03e0f10">

## Requirements
Clone the repository and execute the scripts. All requirements should be downloaded at the beginning of the script. In some cases you need to exchange 'YOUR-API-KEY' with your own API key from f. e. ORS. To do so, simply follow the instruction/link in the code behind the hahstag in that line (#) and log in. 

## Limitations
Since we have 175 centroids in our grid and we calculate bike, car and foot as walking distances (175*3= 525) we get to the limit of the free openrouteservice api. It can only process 500 requests per day.
 
## Folder structure
MCDA-for-data-center-location  
|_ documentation  
    |_ report  
    |_ README  
    |_ flowchart 

|_ data
    |_ input
        |_ baden_wuerttemberg.geojson
        |_ death-rate-from-natural-disasters-gbd.csv
        |_ koppen_geiger_1991_2020.tif
        |_ organized_crime_index.csv
    |_ output
        |_ isochrones
            |_ isochrones_cycling-regular
            |_ isochrones_foot-walking
            |_ isochrones_driving-car
        |_ download
            |_ powerplants
        |_ centroids
            |_
        |_ reclassified
            |_
    |_ result
|_ plots
|_ scripts
    |_ download_data
    |_




    
