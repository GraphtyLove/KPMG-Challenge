import React, { useState } from 'react';
import styled from 'styled-components'
import './App.css';
import SearchBar from './components/SearchBar/SearchBar'
import kpmgLogoImg from './assets/img/KPMG_logo.svg'

// Style
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

const Main = styled.main`
display: flex;
justify-content: space-evenly;
`


function App() {
    return (
    <div className="App">
        <Header>
            <KpmgLogo src={ kpmgLogoImg } alt="kpmg" />
            <h1>Entreprise search engine</h1>
        </Header>
        <Main>
            <SearchBar searchForBusinessNumber={ true  } />
            <SearchBar searchForBusinessNumber={ false } />
        </Main>
    </div>
  );
}

export default App;
