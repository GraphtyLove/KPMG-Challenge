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