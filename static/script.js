// * -------------------- Get data from business number -------------------- *
const getDataFromBusinessNumber = (businessNumber = document.getElementById('businessNumber').value) => {
    event.preventDefault()
    // Get the business number from the input
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
const getBusinessName = (companyName = document.getElementById('businessName').value) => {
    event.preventDefault()
    document.getElementById('loader').classList.remove("display-none");
    fetch(`http://127.0.0.1:5000/get-number-from-name/${companyName}`, {
                    method: 'GET',
                })
        .then(response => response.json())
        .then(response => {
            // Delete div
            let search_elements = document.querySelectorAll('.companyNameList')
            for (let y = 0; y < search_elements.length; y++){
                search_elements[y].remove()
            }
            console.log('Response:', response)
            try {
                for(let i = 0; i < Object.keys(response).length; i++) {
                    console.log('1')
                    // Create div
                    let newTag = document.createElement('li')
                    newTag.setAttribute('class', 'companyNameList')
                    newTag.setAttribute('onClick',  `getDataFromBusinessNumber(${response[i].businessNumber})`)
                    let text_node = document.createTextNode(response[i].companyName)
                    newTag.appendChild(text_node)
                    document.getElementById('searchAnswer').appendChild(newTag)
                }
                document.getElementById('loader').setAttribute('class', 'display-none')
            }
            catch (e) {
                console.log(`listing error: ${e}`)
            }
        })
        .catch(error => {
            console.log(`FETCH error: ${error}`)
        })
}