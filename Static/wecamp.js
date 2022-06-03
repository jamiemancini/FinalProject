'use strict';

//requesting from the NPS API the SPECIFIC campground by its park_ID_code 
//when the user clicks on the specific name of the campground
//the park_ID_code is passes through the url to the server

document.querySelector('#state-form').addEventListener('submit', (event) => {
    event.preventDefault();

    // state selected by the user   
    const stateSelected=document.querySelector('#US_state').value;
    
    //endpoint of the NPS API
    const url = `http://localhost:5000/search_state?state=${stateSelected}`;

fetch(url, {
    method: "GET",
})
    .then(response => response.json())
    .then(apiResponse => {
        showResults(apiResponse);
    });
});