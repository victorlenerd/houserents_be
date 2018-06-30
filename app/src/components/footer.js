import React from 'react';

import whatsapp from '../svg/whatsapp.svg';
import facebook from '../svg/facebook.svg';
import twitter from '../svg/twitter.svg';
import cog from '../svg/cog.svg';

export default () => (
    <div className="footer">
        <div className="container">
            <div className="footer-left col-lg-6 col-md-6 col-sm-6 col-xs-12">
                <p>Share with your friends on</p>
                <div className="share-icons">
                <img src={whatsapp} />
                <img src={facebook} />
                <img src={twitter} />
                </div>
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