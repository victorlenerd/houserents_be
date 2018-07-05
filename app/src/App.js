import React, { Component } from 'react';
import './App.css';
import './toggle.css';

import Header from './components/header';
import Footer from './components/footer';
import Source from './components/source';
import Map from './components/map';
import Filter from './components/filter';

import Areas from './areas';
import Toggle from 'react-toggle';

import $ from 'jquery';
import * as tf from '@tensorflow/tfjs';

class App extends Component {

  constructor(props) {
    super(props);
    
    this.state = {
      nobed: 1,
      nobath: 1,
      notoilets: 1,
      currentArea: null,
      prices: [],
      mode: true,
      sort: 'high'
    }
  }

  async componentWillMount () {    
    this.model = await tf.loadModel("http://localhost:3000/tf_js_model/model.json");

    this.setState({
      areas: Areas()
    }, this.getAreasRange);

    $(window).on('scroll', function () { 
      $(".header").css("top", $(this).scrollTop() * .5);
    });
  }

  getAreasRange = async () => {
    const { nobed, nobath, notoilets } = this.state;

    let tensors = this.state.areas.map((A, i) => {
      return tf.tensor2d([[A.lng, A.lat, Number(nobed), Number(notoilets), Number(nobath)]]);
    });

    const predictions = tensors.map(T => this.model.predict(T).asScalar().data());

    const allPrices = await Promise.all(predictions)
    
    const prices = allPrices.map(( P ) => Math.ceil(P[0]));

    this.setState({ prices });
  }

  updateOption = (e) => {
    let name = e.target.name;
    let value = e.target.value;

    this.setState({
      [name]: value
    }, () => {
      setTimeout(this.getAreasRange, 500);
    });
  }

  handleChange = () => {
    this.setState({
      mode: !this.state.mode
    });
  }

  centerChange = center => {
    console.log('center', center.lat());
  }
  
  render() {
    const { areas, prices, mode } = this.state;

    return (
      <div className="App">
        <Header />
        <div id="main">
          <section>
            <div className="container">

              <label>
                <Toggle
                  defaultChecked={mode}
                  onChange={this.handleChange} />
                <span>Use Keras Model</span>
              </label>

              <h2>Discover By Address</h2>
             
              <div className="col-lg-8 col-lg-offset-2 col-md-12 col-sm-12 col-xs-12">
                <div className="col-lg-9 col-md-9 col-sm-8 col-xs-12">
                  <Map onCenterChange={this.centerChange} />
                </div>
                <div className="col-lg-3 col-md-3 col-sm-4 col-xs-12 input-container">
                  <Filter showSort={false} updateOption={this.updateOption} />
                  <br />
                  <div className="price">
                    <span>Total Cost:</span>
                    <h2>₦{parseFloat(300000).toLocaleString('en')}</h2>
                  </div>
                </div>
              </div>

            </div>
          </section>
          <hr />
          <section>
            <div className="container">
              <h2>Compare By Areas</h2>
              
              <Filter showSort={true} updateOption={this.updateOption} />

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
