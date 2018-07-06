import React, { Component } from 'react';
import './App.css';
import './toggle.css';

import Header from './components/header';
import Footer from './components/footer';
import Source from './components/source';
import Map from './components/map';
import Filter from './components/filter';

import Areas from './areas';

import Predict from './utils/predict';
import Toggle from 'react-toggle';

import $ from 'jquery';

class App extends Component {

  constructor(props) {
    super(props);
    
    this.state = {
      no_bed: 1,
      no_bath: 1,
      no_toilets: 1,

      tno_bed: 1,
      tno_bath: 1,
      tno_toilets: 1,

      currentArea: {
        lat: 6.5005,
        lng: 3.3666
      },
      prices: [],
      areaPrice: 0,
      mode: true,
      sort: 'high',
    }
  }

  async componentWillMount () {    
    this.setState({
      areas: Areas()
    }, () => {
      this.getAddressRange();
      this.getAreasRange();
    });

    $(window).on('scroll', function () { 
      $(".header").css("top", $(this).scrollTop() * .5);
    });
  }

  getAreasRange = async () => {
    const { no_bed, no_bath, no_toilets, mode } = this.state;

    const { prices } = await Predict({ 
      locations: this.state.areas.map(({ lat, lng }) => ({ lat, lng })), 
      specs: { no_bed, no_bath, no_toilets }
    }, mode);

    this.setState({
      prices: prices.map((P) => Math.round(P))
    });
  }

  getAddressRange = async () => {
    const { tno_bed: no_bed, tno_bath: no_bath, tno_toilets: no_toilets, currentArea: { lat, lng }, mode } = this.state;

    const { prices } = await Predict({ 
      locations: [{ lat, lng }], 
      specs: { no_bed, no_bath, no_toilets }
    }, mode);

    this.setState({
      areaPrice:  Math.round(prices[0])
    });
  }

  updateOption = (e, topFilter) => {
    let name = (!topFilter) ? e.target.name : `t${e.target.name}`;
    let value = e.target.value; 

    this.setState({
      [name]: value
    }, () => {
      setTimeout(
        (!topFilter) ? this.getAreasRange : this.getAddressRange
      , 500);
    });
  }

  handleChange = () => {
    this.setState({
      mode: !this.state.mode
    }, () => {
      this.getAddressRange();
      this.getAreasRange();
    });
  }

  centerChange = center => {
    this.setState({ 
      currentArea: {
        lat: center.lat(),
        lng: center.lng()
      }
    }, this.getAddressRange);
  }

  sort = (e) => {
    let type = e.target.value;
    let pairAreaPrice = this.state.areas.map((A, i)=> ({ a: A, p: this.state.prices[i]}))
    
    let sortedPairs = (type !== 'high') ? 
      pairAreaPrice.sort((a, b) => a.p - b.p) : 
      pairAreaPrice.sort((a, b) => b.p - a.p);

    this.setState({
      prices: sortedPairs.map((sp) => sp.p),
      areas: sortedPairs.map((sp) => sp.a)
    });
  }
  
  render() {
    const { areas, prices, mode, areaPrice } = this.state;

    return (
      <div className="App">
        <Header />
        <div id="main">
          <section>
            <div className="container" style={{ textAlign: 'center' }}>
              <div className="col-lg-8 col-lg-offset-2 col-md-12 col-sm-12 col-xs-12">
                <p className="hint">There two models for making predictions. One made with Scikit Learn and the other with Keras. You can switch between models.</p>
                <br />
                <label>
                  <Toggle
                    defaultChecked={mode}
                    onChange={this.handleChange} />
                  {(mode) ? <span className="toggle-label">Scikit Learn Model</span> : <span className="toggle-label">Keras Model</span>}
                </label>
              </div>
            </div>
          </section>
          <hr />
          <section>
            <div className="container">

              <h2>Discover By Address</h2>
             
              <div className="col-lg-8 col-lg-offset-2 col-md-12 col-sm-12 col-xs-12">
                <div className="col-lg-9 col-md-9 col-sm-8 col-xs-12">
                  <Map onCenterChange={this.centerChange} />
                </div>
                <div className="col-lg-3 col-md-3 col-sm-4 col-xs-12 input-container">
                  <Filter showSort={false} updateOption={e => this.updateOption(e, true)} />
                  <br />
                  <div className="price-top">
                    <span>Total Cost:</span>
                    <h4>₦{parseFloat(areaPrice).toLocaleString('en')}</h4>
                  </div>
                </div>
              </div>

            </div>
          </section>
          <hr />
          <section>
            <div className="container">
              <h2>Compare By Areas</h2>
              
              <Filter showSort={true} sort={this.sort} updateOption={this.updateOption} />

              <div className="col-lg-8 col-lg-offset-2 col-md-8 col-md-offset-2 col-sm-12 col-xs-12">              
                <div className="input-container col-lg-12 col-md-12 col-sm-12 col-xs-12">
                  {prices.length > 1 && <ul className="areas-list" type="none">
                    {areas.map((a, i) => {
                      return (
                        <li key={i}>
                          {a.name}
                          <div className="price">
                            <span>₦{parseFloat(prices[i]).toLocaleString('en')}</span>
                          </div>
                        </li>
                      )
                    })}
                  </ul>}
                </div>
              </div>
            </div>
          </section>
          <Source />
          <Footer />
        </div>
      </div>
    );
  }
}

export default App
