import React, { Fragment } from 'react';
import styled from 'styled-components';

const SearchBarItem = props => {

    // * -------------------- STYLE -------------------- *
    const ItemListButton = styled.button`
       /* border: 1px solid #013087; */
       border: 0;
       font-family: Arial,Helvetica,sans-serif;
       font-weight: normal;
       font-size: 15px;
       cursor: pointer;
       text-align:left;

       :hover {
           color: #013087;
           text-decoration: underline;
           text-decoration-color:#013087;
       }

       :focus {
           outline: none;
       }
    `

    // * ---------- Fetch when button is clicked ---------- *
    let handleClick = e => {
            e.preventDefault()
            props.methodToCall( props.businessNumber )
        }

    return (
        <Fragment>
            <li className='companyNameList'><ItemListButton onClick={ handleClick }> { props.CompanyName } </ItemListButton></li>
        </Fragment>
    )
}

export default SearchBarItem
