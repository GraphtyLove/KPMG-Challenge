import React, { Fragment } from 'react';

const SearchItem = ( props ) => {
    return (
        <Fragment>
            <li><button onClick={ props.functionToCall }>{ props.companyName }</button></li>
        </Fragment>
    );
};

export default SearchItem;
