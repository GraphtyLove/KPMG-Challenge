import React, { Fragment } from 'react';

const SearchItem = ( props ) => {
    let handleClick = (e) => {
            e.preventDefault()
            props.methodToCall(props.businessNumber)
        }
    return (
        <Fragment>
            <li><button onClick={ handleClick }>{ props.companyName }</button></li>
        </Fragment>
    );
};

export default SearchItem;
