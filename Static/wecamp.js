//eventlistener for when the search_results.html page is loaded
//because when that happens I want to trigger the call to the API below
window.addEventListener("load", (event) => { 
    console.log('The page has fully loaded');
//need to get the campground_id from search.html



    // const campground_id = document.querySelectorAll('.campground_id');
// use the park_id number to make a another call to the apiResponse
//is passed through the server into as the variable campground_id
    //endpoint of the NPS API using the campground code to query the API
    

    //below is the code using meta in the html of sear_results.html
    // const campground_id = JSON.parse(document.querySelector("#campgroundResult").getAttribute("campground-id"));
    
    const campground_id = "E7CC7363-9C34-42ED-B3F0-769BB39E9400";
    console.log(campground_id);

    const url = `http://localhost:5000/search_campgrounds?q=${campground_id}`;

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

    console.log(results)}
    
    // document
    //     .querySelector('#campsite_image')
    //     .insertAdjacentHTML("beforeend", 
    //          `<img src ={results.data.images >`);}
