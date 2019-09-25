import React, { Fragment, useState } from 'react';
import styled from 'styled-components'

// * -------------------- STYLE -------------------- *
const SearchSection = styled.form`
    display: flex;
    flex-direction: column;
    margin: 40px 0 40px 0;
    background-color: #ffffff;
    padding: 20px;
    /* max-width: 550px; */
    width: 45vw;
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

const SearchBarAndButton = styled.div`
    display: flex;
    justify-content: space-around;
`

const InputSearBar = styled.input`
    width: 60%;
    border-radius: 0;
    border: 1px solid transparent;
    border-bottom: 1px solid #CCCCCC;    
    padding: 10px;
    margin-left: 5px;
    font-family: Arial,Helvetica,sans-serif;
    font-size: 15px;
    /* color: #013087; */
    
    :focus {
        outline: none;
        border-bottom: 1px solid #013087;
    }
`

const ButtonSubmit = styled.button`
    justify-content: center;
    align-items: center;
    width: 100px;
    height: 39px;
    font-family: Arial,Helvetica,sans-serif;
    color: #013087;
    font-weight: bold;
    font-size: 15px;
    background-color: #ffffff;
    border-color: #013087;
    box-shadow: 0 0 0;
    transition: all 0.3s cubic-bezier(.25,.8,.25,1);

    :hover {
        outline: none;
        box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
        transition: all 0.3s cubic-bezier(.25,.8,.25,1);
    }

    :focus {
        outline: none;
    }

    :active {
        font-size: 13px;
    }
`


const SearchBar = props => {
    // * -------------------- STATES -------------------- *
    const [inputValue, setInputValue] = useState("");

    // * ---------- Component's properties ---------- *
    let name = ''
    let placeHolder = ''
    let title = ''
    let buttonText = ''

    // * --- Define Component's properties --- *
     if (props.searchForBusinessNumber === true){
        name = 'businessNumber'
        placeHolder = 'Enter a business number...'
        title = <h2>Search with the business number</h2>
        buttonText = 'Get informations'
    } else {
        name = 'companyName'
        placeHolder = 'Enter a company name...'
        title =  <h2>Search with the company name</h2>
        buttonText = 'Search'
    }

    // * ---------- Input's functions ---------- *

    // Define state with value of input
    const handleSearchInputChanges = e => {
        setInputValue(e.target.value)
    }

     // Reset state
    const resetInputField = () => {
        setInputValue('')
    }

     // Search for company's name
    const callSearchFunction = e => {
        e.preventDefault()
        if (inputValue.length > 0) {
            props.search(inputValue)
            resetInputField()
        }
    }

    return (
        <Fragment>
            <div>
                <SearchSection>
                    { title }
                    <SearchBarAndButton>
                        <InputSearBar id={ name }
                            value={ inputValue }
                            onChange={ handleSearchInputChanges }
                            placeholder={ placeHolder }
                            name={ name }
                            type="text">
                        </InputSearBar>
                        <div>
                            <ButtonSubmit 
                                type='submit'
                                className="submit"
                                onClick={ callSearchFunction }
                                value={ buttonText } >
                                Search
                            </ButtonSubmit>
                        </div>
                    </SearchBarAndButton>
                </SearchSection>
            </div>
        </Fragment>
    );
};

export default SearchBar;
