
//example https://developer.nps.gov/api/v1/campgrounds?stateCode=CA&api_key=************SECRET****************

// import os 

//do I need import os for the secret KEY to be accessble
//my secret key is in secrets.sh YES!

//function showResults will put the results on search_results.html
//for now just a list of the park names

//still need to sort by amenities
//get API working so that names of parks can be displayed
//"name":"Anacapa Island Campground" 
//name is the key for the value of the name of the campsite

function showResults(results) {
    console.log(results);
    //javascript for turning a json into a dictionary
    // const dic = JSON.parse(results);
    console.log(results.name);
    const stateDiv = document.querySelector('#campgrounds-go-here');
    // clear anything currently in the div
    stateDiv.innerHTML =null;
    
    //loop through to find the names of each campground
    for (const parkName of results.data) {
        document
            .querySelector('#campgrounds-go-here')
            .insertAdjacentHTML("beforeend", `<li>${parkName.name}</li>`);

            //is {parkName.name} accessing the name? how do I try it out?
    } 

}
//debugger

document.querySelector('#state-form').addEventListener('submit', (event) => {
    //do I need to prevent the form from triggering a page load?
    event.preventDefault();

    //get the 2 letter state code entered in by the user
    const stateSelected=document.querySelector('#US_state').value;
    //gets all the campgrounds in the state
    //'https://developer.nps.gov/api/v1/campgrounds?stateCode=${stateSelected}&api_key=${API_KEY}'

    //need to have the serve put in the request to the API
    //need to pass the state code to the server
    //where does json information go when retrieved from the server
const url = `http://localhost:5000/search_state?state=${stateSelected}`;

fetch(url, {
    method: "GET",
    
})
    .then(response => response.json())
    .then(apiResponse => {
        showResults(apiResponse);
    });
});
     


