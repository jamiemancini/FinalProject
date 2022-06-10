'use strict';
// use the park_id number to make a another call to the apiResponse

//is passed through the server into as the variable campground_id
    
    //endpoint of the NPS API using the campground code to query the API
    const url = `http://localhost:5000/campgrounds?limit=1&q=${campground_id}`;

fetch(url, {
    method: "GET",
})
    .then(response => response.json())
    .then(apiResponse => {
        printResults(apiResponse);
    });
});

// function that grabs information from the API JSON response
// the JSON ONLY has information for that 1 campsite
function printResults(results) {

    document
        .querySelector('#campsite_image')
        .insertAdjacentHTML("beforeend", 
             `<img src ={results.} >`);}
