

//requesting from the NPS API the campgrounds in the selected state
//once the submit button is clicked
document.querySelector('#state-form').addEventListener('submit', (event) => {
    event.preventDefault();

    // state selected by the user   
    const stateSelected=document.querySelector('#US_state').value;
    console.log(stateSelected)
    
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
    let maxFeeSelected=document.querySelector('#max_fees');
    console.log(maxFeeSelected.value);
    //to do: if the maximum price is left empty then it should show all the campsites
    
    //phone-reception type chosen
    let phone_reception=document.querySelector('input[name="phone_reception"]:checked');
    console.log(phone_reception);
    
    //toilet-type chosen
    let toilets=document.querySelector('input[name="toilet_type"]:checked');
    console.log(toilets);

    //types and # of campsites  
    let reservable_campsites= document.querySelector('#reservable_campsites');
    console.log(reservable_campsites);
    let first_come_campsites= document.querySelector('#first_come_campsites');
    console.log(first_come_campsites);
    

    // list condition to be filtering by
    let conditions = []
    
    if (maxFeeSelected) {
        conditions.push(function(parkName) {
            let fee = parkName.fees.find(fee => fee !== []);
        
            return (fee === undefined || Number(fee['cost']) < maxFeeSelected.value) || maxFeeSelected.value===""
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
            return parkName.numberOfSitesReservable !== "0";
        })
    }

    if (first_come_campsites.checked) {
        conditions.push(function(parkName) {
            return parkName.numberOfSitesFirstComeFirstServe !== "0"

        })

    }
    


    // all the conditions
    let filtered_results = results.data.filter(function(parkName) {
        return conditions.every(function(condition) {
            return condition(parkName)
        });
    });



    function parkDetailHtml(parkData) {

        let detailHtml = "";

        // checks for images url 
        if (parkData.images.length>0) {
            detailHtml += `<div class="card m-1 p-1 text-center">
                            <img src="${parkData.images[0]['url']}" height="175" class="card_image card-img-top rounded" alt="...">
                            <h5 class="card-title" id="${parkData.name}">${parkData.name}</h5>`;
        }
        else {
            detailHtml += `<div class="card m-1 p-1 text-center">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/1/1d/US-NationalParkService-Logo.svg" height="175" class="card__image card-img-top" alt="...">
                            <div class="card-body">
                            <h5 class="card-title" id="${parkData.name}">${parkData.name}</h5>`;
        }
        console.log(parkData.fees)
        // checks for fees data
        if (parkData.fees.length > 0) {
            detailHtml += `<h6 class="card-subtitle mb-2 text-muted">$${parkData.fees[0]["cost"]} per night</h6>`;
        } else {
            detailHtml += `<h6 class="card-subtitle mb-2 text-muted">No cost detail available</h6>`;
        }


        detailHtml += `<p class="card-text">Toilet: ${parkData.amenities.toilets[0]}</p>
                        <p class="card-text">Cell Reception: ${parkData.amenities["cellPhoneReception"]}</p>
                        <p class="card-text">Reservable campsites: ${parkData.numberOfSitesReservable}</p>
                        <p class="card-text">First Come campsites: ${parkData.numberOfSitesFirstComeFirstServe}</p>
                        <a href="/${parkData.id}" target="_blank" class="btn btn-lg p-1">See Details</a></div>`;

        return detailHtml;
    }

    for (const parkName of filtered_results) {
        console.log(parkName.url)
        console.log(parkName)
        document
        .querySelector('#campgrounds-go-here')
        .insertAdjacentHTML("beforeend", parkDetailHtml(parkName));
    }


    //create the header that appears once the search results appear
        document
            .querySelector('#campgrounds_header')
            .innerHTML="Scroll down for Campground Results";

        document
            .querySelector("#search-number")
            .innerHTML=`found ${filtered_results.length} campgrounds`}



