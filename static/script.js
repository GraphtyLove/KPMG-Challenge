
// * -------------------- Get data from business number -------------------- *
const getDataFromBusinessNumber = () => {
    event.preventDefault()
    // Get the business number from the input
    let businessNumber = document.getElementById('businessNumber').value

    fetch(`http://127.0.0.1:5000/data-from-business-number/${businessNumber}`, {
					method: 'GET',
				})
        .then(response => response.json())
        .then(response => {
            console.log('Response:', response)
        })
        .catch(error => {
            console.log(`Error: ${error}`)
        })

}


// * -------------------- Business name -> data -------------------- *
// * ---------- Get the number of a business from his name ---------- *
const getBusinessName = () => {
    let inputValue = document.getElementById('businessName').value
    fetch(`http://127.0.0.1:5000/get-number-from-name/${inputValue}`, {
					method: 'GET',
				})
        .then(response => response.json())
        .then(response => {
            console.log('Response:', response)
        })
        .catch(error => {
            console.log(`Error: ${error}`)
        })
}






// * ---------- Get data from business name ---------- *
const getDataFromBusinessName = () => {
    event.preventDefault()
    // Get the business number from the input
    let businessName = document.getElementById('businessName').value

    fetch(`http://127.0.0.1:5000/data-from-business-number/${businessName}`, {
					method: 'GET',
				})
        .then(response => response.json())
        .then(response => {
            console.log('Response:', response)
        })
        .catch(error => {
            console.log(`Error: ${error}`)
        })

}
