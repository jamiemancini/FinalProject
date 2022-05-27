

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
    
    //pulls out the campsites that cost ess than the maxFeeSelected by user
    if (parkName.fees[0]["cost"]< maxFeeSelected || maxFeeSelected==="") 
    
    {
        //this will be a lot of if loops, for each checked box
        if (reservable_campsites===true){

        document
            .querySelector('#campgrounds-go-here')
            .insertAdjacentHTML("beforeend", 
                `<li><a id="${parkName.name}" href="/campground/${parkName.id}">${parkName.name}: $${parkName.fees[0]["cost"]} per night.</a></li>
                <p>Reservable campsites: ${parkName.numberOfSitesReservable}</p>
                <p>First Come campsites: ${parkName.numberOfSitesFirstComeFirstServe}</p>
                <p>Total campsites: ${parkName.campsites["totalSites"]}</p>`);

    } 

}}}
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
     


