import React, { Fragment } from 'react';

const SearchBarItem = ( props ) => {

    let handleClick = (e) => {
            e.preventDefault()
            props.methodToCall(props.businessNumber)
        }

    return (
        <Fragment>
            <li className='companyNameList'><button onClick={ handleClick }> { props.CompanyName } </button></li>
        </Fragment>
    );
};

export default SearchBarItem;
