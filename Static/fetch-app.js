

//requesting from the NPS API the campgrounds in the selected state
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
     

//the function that displays the results
function showResults(results) {
    

    //clearing the div before putting in the new results
    let stateDiv = document.querySelector('#campgrounds-go-here');
    stateDiv.innerHTML =null;
    // console.log(stateDiv)

    //maximum fee input
    let maxFeeSelected=Number(document.querySelector('#max_fees').value);
    console.log(maxFeeSelected);
    //to do: if the maximum price is left empty then it should show all the campsites
    
    //phone-reception type chosen
    let phone_reception=document.querySelector('input[name="phone_reception"]:checked').value;
    console.log(phone_reception);
    
    //toilet-type chosen
    let toilets=document.querySelector('input[name="toilet_type"]:checked').value;
    console.log(toilets)

    //types and # of campsites  
    let reservable_campsites= document.querySelector('#reservable_campsites').checked;
    console.log(reservable_campsites);
    let first_come_campsites= document.querySelector('#first_come_campsites').checked;
    console.log(first_come_campsites);
    let total_campsites= document.querySelector('#total_campsites').checked;
    console.log(total_campsites);



    //create the header that appears once the search results appear
        document
            .querySelector('#campgrounds_header')
            .innerHTML="Campground Results";

    //loop through to find the names of each campground
    for (const parkName of results.data) {
            let name =parkName.name;
            let fees = parkName.fees[0]["cost"];
            let toiletType = parkName.amenities["toilets"][0];
            let cellPhoneReception = parkName.amenities["cellPhoneReception"];
            let reservableSites = parkName.numberOfSitesReservable;
            let firstServeSites = parkName.numberOfSitesFirstComeFirstServe;
            let totalCampsites = parkName.campsites["totalSites"];
            //let i=0; MAYBE: add a counter so that the user can see the total
            //number of results

    //05/28: (1) approach is to create variables for each of the key:value pairs
    //that I'll be using.  (name, fees, toilets, cell phone reception, campsite counts
    // by reservable, first come and total sites) This is done before I use my if elif statements
    //that filters by the user's choice

    //(2) approach is to create a new data set with just the information that is 
    //needed about each campsite (name, fees, toilets, cell phone reception, campsite counts
    // by reservable, first come and total sites) 
    {
    
    //pulls out the campsites that cost less than the maxFeeSelected by user
    //if the user doesn't pick a maxFee then all the results will be displayed
    if (fees < maxFeeSelected || maxFeeSelected===0) {
        if (phone_reception==="yes"){
            if (toilets==="portable"){
                if (reservable_campsites===true){
                    if (first_come_campsites===true){
                        if (total_campsites===true){
                            
        

        document
            .querySelector('#campgrounds-go-here')
            .insertAdjacentHTML("beforeend", 
                `<li><a id="${parkName.name}" href="/campground/${parkName.id}">${parkName.name}: $${parkName.fees[0]["cost"]} per night.</a></li>
                <p>Reservable campsites: ${parkName.numberOfSitesReservable}</p>
                <p>First Come campsites: ${parkName.numberOfSitesFirstComeFirstServe}</p>
                <p>Total campsites: ${parkName.campsites["totalSites"]}</p>`);

    } 

}}}}}}}}
//debugger

// //takes 
// //requesting from the NPS API the campgrounds in the selected state
// document.querySelector('#state-form').addEventListener('submit', (event) => {
//     event.preventDefault();

// const stateSelected=document.querySelector('#US_state').value;
    

// const url = `http://localhost:5000/search_state?state=${stateSelected}`;

// fetch(url, {
//     method: "GET",
// })
//     .then(response => response.json())
//     .then(apiResponse => {
//         showResults(apiResponse);
//     });
// });
     


