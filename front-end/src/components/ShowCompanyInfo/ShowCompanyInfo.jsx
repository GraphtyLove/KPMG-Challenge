import React, { useState, useEffect } from 'react';
import styled from 'styled-components';

// * -------------------- Components -------------------- *



// * -------------------- Style -------------------- *

function ShowCompanyInfo(props) {

    // * -------------------- STATES -------------------- *

    const [companyInfo, setCompanyInfo] = useState(props.companyInfo);

    // * -------------------- UPDATE FROM PROPS -------------------- *

    useEffect(() => {
        setCompanyInfo(props.companyInfo)
      }, [props.companyInfo]);

    // * -------------------- LOOP THROUGH COMPANY INFO -------------------- *
    
    const LoopThroughCompanyInfo = (props) => {
        let obj = props.objInfo
        let companyInfoArray = Object.keys(obj).map(key => {
            if (typeof obj[key] == 'object') {
                if(obj[key]) {
                    if (Object.keys(obj[key]).length > 0) {
                        return (
                            <div key={key+'div'}>
                                <li key={key+'li'}>{key}:</li>
                                <ul key={key+'ul'}>
                                    <LoopThroughCompanyInfo key={key+'Ltci'} objInfo ={props.objInfo[key]} />
                                </ul>
                            </div>
                        )
                    }
                }
            } else if (typeof obj[key] == 'string') {
                if(obj[key] !== 'Pas de données reprises dans la BCE.' && obj[key] !== 'Liens externes' && obj[key] !== 'None' && obj[key] !== ''){
                    if (key.charAt(key.length-1) === ':') {
                        return [<li key={key}>{key}  {obj[key]}</li>]
                    } else {
                        return [<li key={key}>{key}: {obj[key]}</li>]
                    }
                    
                    
                }
            }
        })
        return companyInfoArray
    } 

    return (
    <div>
        <ul>
            {companyInfo && <LoopThroughCompanyInfo key={'loopThroughCompanyInfo'} objInfo={companyInfo} />}
        </ul>
    </div>
  );
}

export default ShowCompanyInfo;
