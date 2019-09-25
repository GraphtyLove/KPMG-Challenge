import React, { Fragment, useState } from 'react';
import styled from 'styled-components'

// * -------------------- STYLE -------------------- *
const SearchSection = styled.form`
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
                                      type="text" />
                        <input type='submit'
                               className="submit"
                               onClick={ callSearchFunction }
                               value={ buttonText } />
                    </SearchBarAndButton>
                </SearchSection>
            </div>
        </Fragment>
    );
};

export default SearchBar;
