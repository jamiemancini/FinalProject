
//example https://developer.nps.gov/api/v1/campgrounds?stateCode=CA&api_key=************SECRET****************

// import os 
//do I need import os for the secret KEY to be accessble
//my secret key is in secrets.sh

//function showResults will put the results on search_results.html
//for now just a list of the park names

//still need to sort by amenities
//get API working so that names of parks can be displayed

function showResults(results) {
    const stateDiv = document.querySelector('#campgrounds-go-here');
    // clear anything currently in the div
    stateDiv.innerHTML =null;
    //loop through to find the names of each campground
    for (const parkName of results) {
        document
            .querySelector('#campgrounds-go-here')
            .insertAdjacentHTML("beforeend", '<li>${parkName.name}</li>');
            //is {parkName.name} accessing the name? how do I try it out?
    } 

}


document.querySelector('#state-form').addEventListener('submit', (event) => {
    //do I need to prevent the form from triggering a page load?
    event.preventDefault();

    //get the 2 letter state code entered in by the user
    const sateSelected=document.querySelector('#US_state').value;
    //make the AJAX request
    //gets all the campgrounds in the state

fetch("https://developer.nps.gov/api/v1/campgrounds?stateCode=${stateSelected}&api_key=${API_KEY}")
    .then(response => response.json())
    .then(apiResponse => {
        showResults(apiResponse);
    });
});
     


