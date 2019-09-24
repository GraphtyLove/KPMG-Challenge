import React, { Fragment } from 'react';

const SearchBarItem = props => {

    // * ---------- Fetch when button is clicked ---------- *
    let handleClick = e => {
            e.preventDefault()
            props.methodToCall( props.businessNumber )
        }

    return (
        <Fragment>
            <li className='companyNameList'><button onClick={ handleClick }> { props.CompanyName } </button></li>
        </Fragment>
    )
}

export default SearchBarItem
