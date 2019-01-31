import React from 'react';
import github from '../assets/svg/github.svg';

export default () => (
    <div className="source-pane">
    <div className="col-lg-12 col-md-12">
        <div className="container">
        <div className="col-lg-8 col-lg-offset-2 col-md-8 col-md-offset-2 col-sm-12  col-xs-12 inner-pane">
            <h5>This project is opensource you can find the source codes here</h5>
    
            <div className="sources col-lg-12 col-md-12 col-sm-12 col-xs-12">

            <div className="col-lg-4 col-md-4 col-sm-4 col-xs-12">
                <a target="_blank"  href="https://github.com/victorlenerd/toletngscrapper">
                <div className="source">
                    <img src={github} />
                    <span>Scrapper</span>
                </div>
                </a>
            </div>

            <div className="col-lg-4 col-md-4 col-sm-4 col-xs-12">
                <a target="_blank" href="https://github.com/victorlenerd/lagos_housing">
                    <div className="source">
                        <img src={github} />
                        <span>ML Python Notebook</span>
                    </div>
                </a>
            </div>

            <div className="col-lg-4 col-md-4 col-sm-4 col-xs-12">
                <a target="_blank"  href="https://github.com/victorlenerd/houserents">
                    <div className="source">
                        <img src={github} />
                        <span>React Web App</span>
                    </div>
                </a>
            </div>

            </div>
        </div>
        <div className="clearfix"></div>
        </div>
    </div>
</div>
);

