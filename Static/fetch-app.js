
function showResults(results) {
    console.log(results);
    const maxFeeSelected=Number(document.querySelector('#max_fees').value);
    console.log(maxFeeSelected);
    const stateDiv = document.querySelector('#campgrounds-go-here');
    // clear anything currently in the div
    stateDiv.innerHTML =null;
    
    //loop through to find the names of each campground
    for (const parkName of results.data) 
    if (parkName.fees[0]['cost']< maxFeeSelected || maxFeeSelected==="")
    {
        document
            .querySelector('#campgrounds-go-here')
            .insertAdjacentHTML("beforeend", `<li>${parkName.name}: $${parkName.fees[0]['cost']} per night</li>`);

    } 

}
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
     


