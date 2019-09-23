import React, { Fragment, useState } from 'react';
import styled from 'styled-components'

// * ---------- Pictures ---------- *
import kpmgLogoImg from './assets/img/KPMG_logo.svg'

// * -------------------- Components -------------------- *
import SearchBar from './components/SearchBar/SearchBar'
import SearchBarItem from './components/SearchBarItem/SearchBarItem'

// * -------------------- Style -------------------- *
import './App.css';

const KpmgLogo = styled.img`
height: 150px;
width: auto;
margin-top: 50px;
`

const Header = styled.header`
display: flex;
flex-direction: column;
justify-content: center;
align-items: center;
`

const CompanyNameResult = styled.section`
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
`

const InputContainer = styled.section`
    display: flex;
    justify-content: space-evenly;
    width: 100%;
`

const Main = styled.main`
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
`

const CompanyInfoContainer = styled.section`
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    width: 80%;
`

// ! TEST to put 'généralités' in array !
let test = []


function App() {

    // * -------------------- STATES -------------------- *
    const [loading, setLoading] = useState(false);
    const [companyList, setCompanyList] = useState([]);
    const [errorMessage, setErrorMessage] = useState(null);
    const [companyInfo, setCompanyInfo] = useState(null);

    // * ---------- SEARCH FOR COMPANY NAME AND BUSINESS NUMBER ---------- *
    const getBusinessName = searchValue => {
    setLoading(true)
    setErrorMessage(null)

    fetch(`http://127.0.0.1:5000/get-number-from-name/${searchValue}`)
        .then(response => response.json())
        .then(jsonResponse => {
            console.log(jsonResponse)
            if(jsonResponse){
                const tempArray = []
                for(let i = 0; i < Object.keys(jsonResponse).length; i++) {
                    tempArray.push([jsonResponse[i].businessNumber, jsonResponse[i].companyName])
                }
                setCompanyList(tempArray)
                setLoading(false)
            } else {
              setErrorMessage(jsonResponse.Error)
              setLoading(false)
            }
        })
    }

    // * -------------------- Get data from business number -------------------- *
    const getDataFromBusinessNumber = ( businessNumber = document.getElementById('businessNumber').value ) => {
        console.log(typeof(businessNumber))
        // Get the business number from the input
        fetch(`http://127.0.0.1:5000/data-from-business-number/${businessNumber}`, {
                        method: 'GET',
                    })
            .then(response => response.json())
            .then(response => {
                console.log('Response:', response)

                // ! REMPLIR AVEC LE JSON !
                for (let key in response['Généralités']){
                    test[key] = response['Généralités'][key]
                }
                console.log(test)
                setCompanyInfo(response)

            })
            .catch(error => {
                console.log(`Error: ${error}`)

            })
    }

    // * ---------- LOADER ---------- *
    const loaderAndSearchAnswer =   <Fragment> <div id="loader" className="lds-roller display-none"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div> </Fragment>

    return (
    <div className="App">
        <Header>
            <KpmgLogo src={ kpmgLogoImg } alt="kpmg" />
            <h1>Entreprise search engine</h1>
        </Header>
        <Main>
            {/* ---------- SEARCH BARS ---------- */}
            <InputContainer>
                <SearchBar searchForBusinessNumber={ true } search={ getDataFromBusinessNumber }  />
                <div>
                    <SearchBar searchForBusinessNumber={ false } search={ getBusinessName }  />
                    {/* ---------- COMPANY NAME RESULTS ---------- */}
                    <CompanyNameResult>
                        { loading && !errorMessage
                            ? loaderAndSearchAnswer
                            : ( companyList.map(( companyArray, index ) => (
                                <SearchBarItem methodToCall={ getDataFromBusinessNumber } businessNumber={ companyArray[0] } CompanyName={ companyArray[1] } key={ index } />
                            ) ) )
                        }
                    </CompanyNameResult>
                </div>
            </InputContainer>
            <CompanyInfoContainer>
                <ul>
                    { (companyInfo &&  companyInfo['Généralités'] && companyInfo['Généralités']['Dénomination:']) && <li>Dénomination: { companyInfo['Généralités']['Dénomination:'] } </li> }
                    { (companyInfo && companyInfo['business_number']) && <li>Business number: { companyInfo['business_number'] } </li> }
                    { (companyInfo &&  companyInfo['Généralités'] && companyInfo['Généralités']['Date de début:']) && <li>Date de début: { companyInfo['Généralités']['Date de début:'] } </li> }

                </ul>
            </CompanyInfoContainer>
        </Main>
    </div>
  );
}

export default App;
