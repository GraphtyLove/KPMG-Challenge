import React, { Fragment, useState, useEffect } from 'react';
import styled from 'styled-components'
import SearchItem from './SearchItem'

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
    const InputSearBar = styled.input`
    width: 60%;
    border-radius: 3px;
    border: 0.1px solid black;    
    padding: 10px;
    margin-left: 5px;
`

const SearchBar = ( props ) => {
    let name = ''
    let placeHolder = ''
    let onClickFunction = ''
    let title = ''
    let buttonText = ''
    let componentList = []

    // * ---------- STATES ---------- *
    const [companyList, setCompanyList] = useState([])
    const [test, setTest] = useState(0);


    // * -------------------- Get data from business number -------------------- *
    const getDataFromBusinessNumber = ( businessNumber = document.getElementById('businessNumber').value ) => {
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
        console.log('first: ', companyList)
        // Empty state companyList
        componentList = []
        setCompanyList([])
            // Loop to empty the state
        for(let i = 0; i < componentList; i++){
            componentList.pop()
        }
        for(let i = 0; i < setCompanyList; i++){
            setCompanyList.pop()
        }

        console.log('second: ', companyList)

        const companyName = document.getElementById('companyName').value
        document.getElementById('loader').classList.remove("display-none");
        fetch(`http://127.0.0.1:5000/get-number-from-name/${companyName}`, {
                        method: 'GET',
                    })
            .then(response => response.json())
            .then(response => {
                let count = 0
                console.log('Response:', response)
                try {
                    for(let i = 0; i < Object.keys(response).length; i++) {
                        let tempArray = companyList
                        tempArray.push([response[i].businessNumber, response[i].companyName])
                        setTest(count)
                        console.log(`count: ${count}`)
                        console.log(`test: ${test}`)
                        count++
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
        buttonText = 'Get informations'
    } else {
        name = 'companyName'
        placeHolder = 'Enter a company name...'
        onClickFunction = () => getBusinessName()
        title =  <h2>Search with the company name</h2>
        buttonText = 'Search'
    }


    for(let i = 0; i < companyList.length; i++){
        componentList.push(<SearchItem companyName={ companyList[i][1] } methodToCall={ getDataFromBusinessNumber } businessNumber={ companyList[i][0] } key={ i } />)
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
                        <InputSearBar id={ name } placeholder={ placeHolder } name={ name } type="text" />
                        <button className="submit" onClick={ onClickFunction }> { buttonText } </button>
                    </SearchBarAndButton>
                </SearchSection>
                <CenteredSection>
                    { props.searchForBusinessNumber
                    ? null
                    : loaderAndSearchAnswer
                    }
                    { componentList }
                </CenteredSection>

            </div>
        </Fragment>
    );
};

export default SearchBar;
