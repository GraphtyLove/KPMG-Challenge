import React, { Fragment } from 'react';
import styled from 'styled-components';

// * -------------------- STYLE -------------------- *
const ItemListButton = styled.button`
    border: 0;
    font-family: Arial,Helvetica,sans-serif;
    font-weight: normal;
    font-size: 15px;
    cursor: pointer;
    text-align:left;
    -webkit-box-shadow: 4px 4px 5px 0px rgba(0,0,0,0.33);
    -moz-box-shadow: 4px 4px 5px 0px rgba(0,0,0,0.33);
    box-shadow: 4px 4px 5px 0px rgba(0,0,0,0.33);
    border: 1px solid black;
    background: #fff;
    margin-bottom: 10px;
    padding: 10px;
    :hover {
        color: #013087;
        text-decoration: underline;
        text-decoration-color:#013087;
    }
    :focus {
        outline: none;
    }
`

const SearchBarItem = props => {
    // * ---------- Fetch when button is clicked ---------- *
    let handleClick = e => {
            e.preventDefault()
            props.methodToCall( props.businessNumber )
        }

    return (
        <Fragment>
            <li><ItemListButton onClick={ handleClick }> { props.CompanyName } </ItemListButton></li>
        </Fragment>
    )
}

export default SearchBarItem
