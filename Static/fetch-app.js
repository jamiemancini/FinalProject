

//requesting from the NPS API the campgrounds in the selected state
//once the submit button is clicked
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
    let maxFeeSelected=Number(document.querySelector('#max_fees'));
    console.log(maxFeeSelected);
    //to do: if the maximum price is left empty then it should show all the campsites
    
    //phone-reception type chosen
    let phone_reception=document.querySelector('input[name="phone_reception"]:checked');
    console.log(phone_reception);
    
    //toilet-type chosen
    let toilets=document.querySelector('input[name="toilet_type"]:checked');
    console.log(toilets)

    //types and # of campsites  
    let reservable_campsites= document.querySelector('#reservable_campsites');
    console.log(reservable_campsites);
    let first_come_campsites= document.querySelector('#first_come_campsites');
    console.log(first_come_campsites);
    let total_campsites= document.querySelector('#total_campsites');
    console.log(total_campsites);

    // list condition to be filtering by
    let conditions = []
    
    if (maxFeeSelected) {
        conditions.push(function(parkName) {
            let fee = parkName.fees.find(fee => fee["cost"] !== "");
            return fee["cost"] < maxFeeSelected.value || maxFeeSelected.value===0
        });
    }

    if (phone_reception && phone_reception.value !== "both") {
        conditions.push(function(parkName) {
            return parkName.amenities["cellPhoneReception"].toLowerCase().includes(phone_reception.value)
        });
    }

    if (toilets) { 

        conditions.push(function(parkName) {
            if (parkName.amenities["toilets"].length) {
                let toiletType = parkName.amenities["toilets"][0].toLowerCase()

                if (toilets.value==="portable") {
                    return toiletType.includes("portable") || toiletType.includes("vault")
                }
                else if (toilets.value ==="flush") {
                    return toiletType.incudes("flush")
                }

                else {
                    // !toiletType.includes("no toilets")
                    return toiletType.includes("portable") || toiletType.includes("vault") || toiletType.includes("flush")
                }
            }

        });
    }
    if (reservable_campsites.checked) {
        conditions.push(function(parkName) {
            return parkName.numberOfSitesReservable !== "0"
        })
    }

    if (first_come_campsites.checked) {
        conditions.push(function(parkName) {
            return parkName.numberOfSitesFirstComeFirstServe !== "0"
        })

    }
    
    if (total_campsites.checked) {
        conditions.push(function(parkName) {
            return parkName.campsites["totalSites"] !== "0"
        })
    }

    // all the conditions
    let filtered_results = results.data.filter(function(parkName) {
        return conditions.every(function(condition) {
            return condition(parkName)
        });
    });


    for (const parkName of filtered_results) {
        console.log(parkName.url)
        document
        .querySelector('#campgrounds-go-here')
        .insertAdjacentHTML("beforeend", 
                       
                        `<li><a id="${parkName.name}" href="/${parkName.id}">${parkName.name}: $${parkName.fees[0]["cost"]} per night.</a></li>
                        <p>Reservable campsites: ${parkName.numberOfSitesReservable}</p>
                        <p>First Come campsites: ${parkName.numberOfSitesFirstComeFirstServe}</p>`);
    }

    //original specific search result was using the parkName.id from the JSON
//06/02 - new thinking is link directly using parkName.url from the JSON
//<li><a id="${parkName.name}" href="${parkName.url}" target="_blank">${parkName.name}: $${parkName.fees[0]["cost"]} per night.</a></li>

//06/07 - changed back to original
//<li><a id="${parkName.name}" href="/campground/${parkName.id}">${parkName.name}: $${parkName.fees[0]["cost"]} per night.</a></li>




    //create the header that appears once the search results appear
        document
            .querySelector('#campgrounds_header')
            .innerHTML="Campground Results";

        document
            .querySelector("#search-number")
            .innerHTML=`found ${filtered_results.length} campgrounds`

    //loop through to find the names of each campground
//     for (const parkName of results.data) {
//             let name =parkName.name;
//             let fees = parkName.fees[0]["cost"];
//             let toiletType = parkName.amenities["toilets"][0];
//             let cellPhoneReception = parkName.amenities["cellPhoneReception"];
//             let reservableSites = parkName.numberOfSitesReservable;
//             let firstServeSites = parkName.numberOfSitesFirstComeFirstServe;
//             let totalCampsites = parkName.campsites["totalSites"];
//             //let i=0; MAYBE: add a counter so that the user can see the total
//             //number of results

//     //05/28: (1) approach is to create variables for each of the key:value pairs
//     //that I'll be using.  (name, fees, toilets, cell phone reception, campsite counts
//     // by reservable, first come and total sites) This is done before I use my if elif statements
//     //that filters by the user's choice

//     //(2) approach is to create a new data set with just the information that is 
//     //needed about each campsite (name, fees, toilets, cell phone reception, campsite counts
//     // by reservable, first come and total sites) 
//     {
    
//     //pulls out the campsites that cost less than the maxFeeSelected by user
//     //if the user doesn't pick a maxFee then all the results will be displayed
//     if (fees < maxFeeSelected || maxFeeSelected===0) {
        
//         //results if phone reception is needed
//         if (phone_reception==="yes"){
            
//             //IF USER clicks on the radio button "Vaulted / Portable"
//             //results if toilets with "Vaulted / Portable Toilet"
//             if (toilets==="portable"){

//                 //I need to check if the campsite in the JSON 
//                 //retreived information has the words "Vault" or "Portable"
                
//                 //STOPPED HERE 5/31
//                 //if (toiletType.includes("Vaulted") || toiletType.includes("Portable") 

//                 // check which of reservable, first_come and total_campsites
//                 // are shown to the user
//                 // total of 7 different options 

//                 //3 of 3 - all true 
//                 //show the reservable, first_come and total_campsites
//                 if (reservable_campsites===true  && first_come_campsites===true 
//                     && total_campsites===true){
                    
                                                                                      
//                 document
//                     .querySelector('#campgrounds-go-here')
//                     .insertAdjacentHTML("beforeend", 
//                         `<li><a id="${parkName.name}" href="/campground/${parkName.id}">${parkName.name}: $${parkName.fees[0]["cost"]} per night.</a></li>
//                         <p>Reservable campsites: ${parkName.numberOfSitesReservable}</p>
//                         <p>First Come campsites: ${parkName.numberOfSitesFirstComeFirstServe}</p>
//                         <p>Total campsites: ${parkName.campsites["totalSites"]}</p>`);

//     }                   
//                 //2 of 3 true 
//                 //show the reservable, first_come BUT NOT!!!! total_campsites
//                 else if (reservable_campsites===true  && first_come_campsites===true 
//                     && total_campsites===false){
                
//                 document
//                     .querySelector('#campgrounds-go-here')
//                     .insertAdjacentHTML("beforeend", 
//                         `<li><a id="${parkName.name}" href="/campground/${parkName.id}">${parkName.name}: $${parkName.fees[0]["cost"]} per night.</a></li>
//                         <p>Reservable campsites: ${parkName.numberOfSitesReservable}</p>
//                         <p>First Come campsites: ${parkName.numberOfSitesFirstComeFirstServe}</p>`);
//     }

//                 //2 of 3 true 
//                 //show the reservable and total_campsites BUT NOT!!!!! first_come
//                 else if (reservable_campsites===true  && first_come_campsites===false 
//                     && total_campsites===true){
                                                     
//                 document
//                     .querySelector('#campgrounds-go-here')
//                     .insertAdjacentHTML("beforeend", 
//                         `<li><a id="${parkName.name}" href="/campground/${parkName.id}">${parkName.name}: $${parkName.fees[0]["cost"]} per night.</a></li>
//                         <p>Reservable campsites: ${parkName.numberOfSitesReservable}</p>
//                         <p>Total campsites: ${parkName.campsites["totalSites"]}</p>`);                
//                     }

//                 //2 of 3 true
//                 //show the first_come and total_campsites BUT NOT!!!!! reservable
//                 else if (reservable_campsites===false  && first_come_campsites===true 
//                     && total_campsites===true){
                                        
//                 document
//                     .querySelector('#campgrounds-go-here')
//                     .insertAdjacentHTML("beforeend", 
//                         `<li><a id="${parkName.name}" href="/campground/${parkName.id}">${parkName.name}: $${parkName.fees[0]["cost"]} per night.</a></li>
//                         <p>First Come campsites: ${parkName.numberOfSitesFirstComeFirstServe}</p>
//                         <p>Total campsites: ${parkName.campsites["totalSites"]}</p>`);
//                     }

//                 //1 of 3 true 
//                 //show the reservable BUT NOT!!!! first_come and NOT!!!!total_campsites
//                 else if (reservable_campsites===true  && first_come_campsites===false 
//                     && total_campsites===false){
//                 document
//                     .querySelector('#campgrounds-go-here')
//                     .insertAdjacentHTML("beforeend", 
//                         `<li><a id="${parkName.name}" href="/campground/${parkName.id}">${parkName.name}: $${parkName.fees[0]["cost"]} per night.</a></li>
//                         <p>Reservable campsites: ${parkName.numberOfSitesReservable}</p>`);

//                     }

//                 // 1 of 3 true 
//                 // show first_come BUT NOT!!!! reservable and NOT!!! toal_campsites
//                 else if (reservable_campsites===false  && first_come_campsites===true 
//                     && total_campsites===false){
                            
                                                                                               
//                 document
//                     .querySelector('#campgrounds-go-here')
//                     .insertAdjacentHTML("beforeend", 
//                         `<li><a id="${parkName.name}" href="/campground/${parkName.id}">${parkName.name}: $${parkName.fees[0]["cost"]} per night.</a></li>
//                         <p>First Come campsites: ${parkName.numberOfSitesFirstComeFirstServe}</p>`);

//                             }
        
//                  //1 of 3 true 
//                 //total_campsites BUT NOT!!!! reservable and NOT!!! first_come
//                 else if (reservable_campsites===false  && first_come_campsites===false 
//                     && total_campsites===true){
                    
                                                                                       
//                 document
//                     .querySelector('#campgrounds-go-here')
//                     .insertAdjacentHTML("beforeend", 
//                         `<li><a id="${parkName.name}" href="/campground/${parkName.id}">${parkName.name}: $${parkName.fees[0]["cost"]} per night.</a></li>
//                         <p>Total campsites: ${parkName.campsites["totalSites"]}</p>`);
        
//     }       
//                 else {
//                 document
//                     .querySelector('#campgrounds-go-here')
//                     .insertAdjacentHTML("beforeend", 
//                         `<li><a id="${parkName.name}" href="/campground/${parkName.id}">${parkName.name}: $${parkName.fees[0]["cost"]} per night.</a></li>`);
//                 }

// }}}}}

}
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
     

