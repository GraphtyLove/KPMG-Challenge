import React, {useState, useEffect, Fragment} from 'react';
import styled from 'styled-components';

// * -------------------- Components -------------------- *

const InfoLi = styled.li`
    padding-bottom: 7px;
`

const InfoLiSection = styled.li`
    display: none;
`

const InfoLiDiv = styled.div`
    padding-bottom: 20px;
`

const ShowCompanyInfoDiv = styled.div`
    max-height: 500px;
    overflow-y: scroll;
    font-size: 15px;
`

const SpanTitle = styled.span`
    color: #012972;
`

// * -------------------- Style -------------------- *

function ShowArticles(props) {

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
                if (obj[key]) {
                    if (Object.keys(obj[key]).length > 0) {

                        return (
                            <InfoLiDiv key={key + 'div'}>
                                <InfoLiSection key={key + 'li'}><SpanTitle>{key}: </SpanTitle></InfoLiSection>
                                <ul key={key + 'ul'}>
                                    <LoopThroughCompanyInfo key={key + 'Ltci'} objInfo={props.objInfo[key]}/>
                                </ul>
                            </InfoLiDiv>
                        )
                    }
                }

            } else if (typeof obj[key] == 'string') {
                    if (key.charAt(key.length - 1) === ':') {

                        return [<InfoLi key={key}><SpanTitle>{key}</SpanTitle> {obj[key]}</InfoLi>]
                    } else {
                        return [<InfoLi key={key}><SpanTitle>{key.replace('Extracted_', '').replace('_final', '').replace('_', ' ')}:</SpanTitle> {obj[key]}</InfoLi>]
                    }

            }
        })
        return companyInfoArray
    }

    return (
        <ShowCompanyInfoDiv>
            <ul>
                {companyInfo["status"] && <LoopThroughCompanyInfo key={'loopThroughCompanyInfo'} objInfo={companyInfo}/>}
            </ul>
        </ShowCompanyInfoDiv>
    );
}

export default ShowArticles;
