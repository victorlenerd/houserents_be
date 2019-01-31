import React from 'react';
import cog from '../assets/svg/cog.svg';

export default () => (
    <div className="footer">
        <div className="container">
            <div className="footer-left col-lg-6 col-md-6 col-sm-6 col-xs-12">
                <a className="github-button" href="https://github.com/victorlenerd/houserents" data-size="large" data-show-count="true" aria-label="Star victorlenerd/houserents on GitHub">Star</a>
            </div>
            <div className="footer-right col-lg-6 col-md-6 col-sm-6 col-xs-12">
                <div className="signature pull-right">
                    <img src={cog} className="pull-left" />
                    <p className="pull-right">
                        Designed & Developed By <a href="https://www.linkedin.com/in/victorlenerd/" target="_blank" className="highlight">VictorLeNerd</a>
                    </p>
                </div>
            </div>
        </div>
    </div>
)