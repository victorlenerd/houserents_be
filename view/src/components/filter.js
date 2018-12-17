import React from 'react';

const getOptions = () => [1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((o, i) => {
    return (<option key={i} value={o}>{o}</option>);
});

export default (props) => (
    <div  className={(props.showSort) ? "col-lg-8 col-lg-offset-2 col-md-8 col-md-offset-2 col-sm-12 col-xs-12": ""}>
        <div  className={(props.showSort) ? "input-container col-lg-12 col-md-12 col-sm-12 col-xs-12": ""}>
            <div className={(props.showSort) ? "col-lg-3 col-md-3 col-sm-6 col-xs-12" : ""}>
                <div className="input-label">NO. Of Bedrooms</div>
                <select onChange={props.updateOption} name="no_bed">
                {getOptions()}
                </select>
            </div>
            <div className={(props.showSort) ? "col-lg-3 col-md-3 col-sm-6 col-xs-12" : ""}>
                <div className="input-label">NO. Of Bathrooms</div>
                <select onChange={props.updateOption} name="no_bath">
                {getOptions()}
                </select>
            </div>
            <div className={(props.showSort) ? "col-lg-3 col-md-3 col-sm-6 col-xs-12" : ""}>
                <div className="input-label">NO. Of Toilets</div>
                <select onChange={props.updateOption} name="no_toilets">
                {getOptions()}
                </select>
            </div>

            {props.showSort && <div className={(props.showSort) ? "col-lg-3 col-md-3 col-sm-6 col-xs-12" : "col-lg-12 col-md-12 col-sm-12 col-xs-12"}>
                <div className="input-label">Sort</div>
                <select name="sort" onChange={props.sort}>
                    <option value="high">High</option>
                    <option value="low">Low</option>
                </select>
            </div>}
        </div>
  </div>
);