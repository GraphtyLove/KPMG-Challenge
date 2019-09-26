import React, { Fragment, useState } from 'react';
import styled from 'styled-components'

// * ---------- Pictures ---------- *
import kpmgLogoImg from './assets/img/KPMG_logo.svg'
import kpmgBannerImg from './assets/img/KPMG-banner.png'

// * -------------------- Components -------------------- *
import SearchBar from './components/SearchBar/SearchBar'
import SearchBarItem from './components/SearchBarItem/SearchBarItem'
import ShowCompanyInfo from './components/ShowCompanyInfo/ShowCompanyInfo'
import ShowArticles from './components/ShowArticles/ShowArticles'


// * -------------------- Style -------------------- *
import './App.css';

const Nav = styled.nav`
    min-height: 58px;
    width: 100vw;
    background-color: #ffffff;
    display: flex;
    justify-content: flex-start;
    align-items: center;
`

const KpmgLogo = styled.img`
    height: 50px;
    padding-left: 40px;
`

const BannerDiv = styled.div`
    background-image:url(${props => props.BackgroundImage});
    background-size: cover;
    width: 100vw;
    height: 400px;
`

const BlueDiv = styled.div`
    background-color: #013087;
    width: 320px;
    height: 322px;
    margin-left: 37px;
    padding: 10px 20px 10px 17px;    
    h1 {
        margin-top : 0;
        font-family: KPMGLight;
        font-size: 56px;
        line-height: 1;
        font-weight: normal;
        color: #ffffff;
        max-width: 50px;
    }
    p {
        font-family: Arial,Helvetica,sans-serif;
        color: #ffffff;
        font-weight: bold;
        font-size: 17px;
    }
`

const Header = styled.header`
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
`

const CompanyNameResult = styled.section`
    display: ${props => props.companyList.length > 0 || props.loading ? 'flex' : 'none'};
    font-family: Arial,Helvetica,sans-serif;
    flex-direction: column;
    align-items: center;
    background-color: #ffffff;
    padding: 20px;
    margin-bottom: 20px;
    max-width: 45vw;

    h2 {
        margin-top : 0;
        font-family: KPMGLight;
        font-size: 45px;
        line-height: 1;
        font-weight: normal;
        color: #013087;
        text-align: center;
    }
`

const ResultsCompanyNameResult = styled.div`
    text-align: ${props => props.loading ? 'center' : ''};    
    align-items: ${props => props.loading ? 'center' : ''};
    width: 100%;
    max-height: 500px;
    overflow-y: scroll;
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
    display: ${props =>  Object.keys(props.companyInfo).length > 0 ? 'flex' : 'none'};
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 80%;
    background-color: #ffffff;
    margin-bottom: 20px;
    width: 45vw;
    font-size: 15px;
    padding: 20px;
    
    li {
        list-style: none;
    }
    
    h2 {
        align-items: center;
        margin-top : 0;
        font-family: KPMGLight;
        font-size: 45px;
        line-height: 1;
        font-weight: normal;
        color: #013087;
        text-align: center;
    }
`

const DataFromArticle = styled.div`
    display: ${props =>  Object.keys(props.companyInfoStatus).length > 0 ? 'flex' : 'none'};
    width: 95vw;
    padding: 20px;
    background-color: #ffffff;
    
    li {
        list-style: none;
    }
    
    h2 {
        align-items: center;
        margin-top : 0;
        font-family: KPMGLight;
        font-size: 45px;
        line-height: 1;
        font-weight: normal;
        color: #013087;
        text-align: center;
    }
`

function App() {

    // * -------------------- STATES -------------------- *
    const [loading, setLoading] = useState(false);
    const [companyList, setCompanyList] = useState([]);
    const [errorMessage, setErrorMessage] = useState(null);
    const [companyInfo, setCompanyInfo] = useState({});
    const [companyInfoStatus, setCompanyInfoStatus] = useState({});

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

        // Get the business number from the input
        fetch(`http://127.0.0.1:5000/data-from-business-number/${businessNumber}`, {
                        method: 'GET',
                    })
            .then(response => response.json())
            .then(response => {
                // response["status"] = response["status"].replace(/[\n\r]/g, ' ')
                response["status"] = JSON.parse(response["status"])
                console.log('Response:', response)
                let responseWithoutStatus = {}
                for (const [key, value] of Object.entries(response)) {
                    if(key !== 'status'){
                        responseWithoutStatus[key] = value
                    }
                }
                let responseWithtStatus = {}
                for (const [key, value] of Object.entries(response)) {
                    if(key === 'status'){
                        responseWithtStatus[key] = value
                    }
                }
                console.log('WITH STATUS: ', responseWithtStatus)
                console.log('NO STATUS: ', responseWithoutStatus)

                setCompanyInfo(responseWithoutStatus)
                setCompanyInfoStatus(responseWithtStatus)
            })
            .catch(error => {
                console.log(`Error: ${error}`)

            })
    }

    // * ---------- LOADER ---------- *
    const loaderAndSearchAnswer = <Fragment> <div id="loader" className="lds-roller display-none"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div> </Fragment>


    return (
        <div className="App">
            <Header>
                <BannerDiv BackgroundImage={kpmgBannerImg}>
                    <Nav>
                        <KpmgLogo src={ kpmgLogoImg }/>
                    </Nav>
                    <BlueDiv>
                        <h1>Entreprise search engine</h1>
                        <p>A challenge from KPMG for our data scientist training at BeCode.</p>
                    </BlueDiv>
                </BannerDiv>
            </Header>
            <Main>
                {/* ---------- SEARCH BARS ---------- */}
                <InputContainer>
                    <div>
                        <SearchBar searchForBusinessNumber={ true } search={ getDataFromBusinessNumber }  />
                        <CompanyInfoContainer companyInfo={companyInfo}>
                        <div>
                            <h2>Company informations</h2>
                        </div>
                            <ShowCompanyInfo companyInfo={companyInfo} />
                        </CompanyInfoContainer>
                    </div>
                    <div>
                        <SearchBar searchForBusinessNumber={ false } search={ getBusinessName }  />
                        {/* ---------- COMPANY NAME RESULTS ---------- */}
                        <CompanyNameResult companyList={companyList} loading={loading}>
                            <h2>Results</h2>
                            <ResultsCompanyNameResult loading={loading} >
                                { loading && !errorMessage
                                    ? loaderAndSearchAnswer
                                    : ( companyList.map(( companyArray, index ) => (
                                        <SearchBarItem methodToCall={ getDataFromBusinessNumber } businessNumber={ companyArray[0] } CompanyName={ companyArray[1] } key={ index } />
                                    ) ) )
                                }
                            </ResultsCompanyNameResult>
                        </CompanyNameResult>
                    </div>
                </InputContainer>
                <div>
                    <DataFromArticle companyInfoStatus={companyInfoStatus}>
                        <div>
                            <h2>Articles</h2>
                        </div>
                        <ShowArticles companyInfo={companyInfoStatus} />
                    </DataFromArticle>
                </div>
            </Main>
        </div>
    );
}

export default App;
