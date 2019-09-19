import React, { Fragment } from 'react';
import styled from 'styled-components'

// * ---------- STYLE ---------- *
const CenteredSection  = styled.section`
        display: flex;
        flex-direction: column;
        align-items: center;
    `
    const SearchSection = styled.section`
      display: flex;
      flex-direction: column;
      margin-bottom: 20px;
    `
    const SearchBarAndButton = styled.div`
      display: flex;
      justify-content: space-around;
`

const SearchBar = ( props ) => {
    let name = ''
    let placeHolder = ''
    let onClickFunction = ''
    let title = ''
    let buttunText = ''

    // * -------------------- Get data from business number -------------------- *
    const getDataFromBusinessNumber = (businessNumber = document.getElementById('businessNumber').value) => {
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

    // * ---------- Get the number of a business from his name ---------- *
    const getBusinessName = () => {
        const companyName = document.getElementById('companyName').value
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
                    console.log(`listing error: ${ e }`)
                }
            })
            .catch(error => {
                console.log(`FETCH error: ${ error }`)
            })
    }


    if(props.searchForBusinessNumber === true){
        name = 'businessNumber'
        placeHolder = 'Enter a business number...'
        onClickFunction = () => getDataFromBusinessNumber()
        title = <h2>Search with the business number</h2>
        buttunText = 'Get informations'
    } else {
        name = 'companyName'
        placeHolder = 'Enter a company name...'
        onClickFunction = () => getBusinessName()
        title =  <h2>Search with the company name</h2>
        buttunText = 'Search'
    }

    const loaderAndSearchAnswer = <Fragment>
        <div id='searchAnswer'></div>
        <div id="loader" className="lds-roller display-none">
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
        </div>
        </Fragment>


    return (
        <Fragment>
            <div>
                <SearchSection>
                    { title }
                    <SearchBarAndButton>
                        <input id={ name } placeholder={ placeHolder } name={ name } type="text" />
                        <button className="submit" onClick={ onClickFunction }> { buttunText } </button>
                    </SearchBarAndButton>
                </SearchSection>
                <CenteredSection>
                    { props.searchForBusinessNumber
                    ? null
                    : loaderAndSearchAnswer
                    }
                </CenteredSection>

            </div>
        </Fragment>
    );
};

export default SearchBar;
