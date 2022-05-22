// var reservable_campsites= document.querySelector('#reservable_campsites').checked;
// console.log(reservable_campsites);

function showResults(results) {
    //identify if the boxes are checked 
    var reservable_campsites= document.querySelector('#reservable_campsites').checked;
    console.log(reservable_campsites);
    var first_come_campsites= document.querySelector('#first_come_campsites').checked;
    console.log(first_come_campsites);
    var total_campsites= document.querySelector('#total_campsites').checked;
    console.log(total_campsites);


    //create variable for the maximum fee
    var maxFeeSelected=Number(document.querySelector('#max_fees').value);
    console.log(maxFeeSelected);
    //if the maximum price is left empty then it should show all the campsites
    
    
    var stateDiv = document.querySelector('#campgrounds-go-here');
    stateDiv.innerHTML =null;
    // clear anything currently in the div

        //create the header that appears once the search results appear
        document
            .querySelector('#campgrounds_header')
            .innerHTML="Name of Campground Results";

    //loop through to find the names of each campground
    for (const parkName of results.data) {
            
    if (parkName.fees[0]["cost"]< maxFeeSelected || maxFeeSelected===""){
        //this will be a lot of if loops, for each checked box
        if (reservable_campsites===true){

        document
            .querySelector('#campgrounds-go-here')
            .insertAdjacentHTML("beforeend", 
                `<li><a id="${parkName.name}" href="/search/${parkName.id}">${parkName.name}: $${parkName.fees[0]["cost"]} per night.</a></li>
                <p>Reservable campsites: ${parkName.numberOfSitesReservable}</p>
                <p>First Come campsites: ${parkName.numberOfSitesFirstComeFirstServe}</p>
                <p>Total campsites: ${parkName.campsites["totalSites"]}</p>`);

    } 

}}}
//debugger

//requesting from the NPS API the campgrounds in the selected state
document.querySelector('#state-form').addEventListener('submit', (event) => {
    event.preventDefault();

    const stateSelected=document.querySelector('#US_state').value;
    

const url = `http://localhost:5000/search_state?state=${stateSelected}`;

fetch(url, {
    method: "GET",
})
    .then(response => response.json())
    .then(apiResponse => {
        showResults(apiResponse);
    });
});
     


