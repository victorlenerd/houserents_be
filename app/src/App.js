import React, { Component } from 'react';
import './App.css';

import Header from './components/header';
import Footer from './components/footer';
import Source from './components/source';

import Areas from './areas';

import { GoogleMap, withGoogleMap } from "react-google-maps"


class App extends Component {

  constructor(props) {
    super(props);
    
    this.state = {
      nobed: '1',
      nobath: '1',
      notoilets: '1', 
      currentArea: null,
      prices: [],
      sort: 'high'
    }
  }

  componentWillMount () {
    this.setState({
      areas: Areas()
    },this.getAreasRange);
  }

  getOptions() {
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((o, i) => {
      return (<option key={i} value={i}>{o}</option>) 
    })
  }

  getAreasRange = () => {
    const { nobed, nobath, notoilets } = this.state;

    let requests = this.state.areas.map((A, i) => {
      return fetch(`http://localhost:5000/predict?lat=${A.lat}&lng=${A.lng}&no_bed=${nobed}&no_toilets=${notoilets}&no_bath=${nobath}`).then(res => res.json())
    });

    Promise.all(requests)
    .then((allPrice) => {
      this.setState({ prices: allPrice.map((P) => P.price) });
    })
    .catch((err) => {
      console.error(err);
    });
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

  updateSearch = (e) => {

  }
  
  render() {
    const { areas, prices } = this.state;

    return (
      <div className="App">
        <Header />
        <section>
          <div className="container">
            <h2>Discover By Address</h2>
            <div className="col-lg-8 col-lg-offset-2 col-md-8 col-md-offset-2 col-sm-12 col-xs-12">

              <div className="input-container col-lg-12 col-md-12 col-sm-12 col-xs-12">
                <div className="col-lg-4 col-md-6 col-sm-6 col-xs-12">
                  <div className="input-label">Address</div>
                  <input type="text" className="address" placeholder="Eg. Adekunle, Yaba" />
                </div>
                <div className="col-lg-3 col-md-2 col-sm-6 col-xs-12">
                  <div className="input-label">NO. Of Bedrooms</div>
                  <select onChange={this.updateSearch} name="nobed">
                    {this.getOptions()}
                  </select>
                </div>
                <div className="col-lg-3 col-md-2 col-sm-6 col-xs-12">
                  <div className="input-label">NO. Of Bathrooms</div>
                  <select onChange={this.updateSearch} name="nobath">
                    {this.getOptions()}
                  </select>
                </div>
                <div className="col-lg-2 col-md-2 col-sm-6 col-xs-12">
                  <div className="input-label">NO. Of Toilets</div>
                  <select onChange={this.updateSearch} name="notoilets">
                    {this.getOptions()}
                  </select>
                </div>
              </div>

              <div className="input-container map">
                <GoogleMap
                  defaultZoom={8}
                  defaultCenter={{ lat: -34.397, lng: 150.644 }}
                />    
              </div>

            </div>

          </div>
        </section>
        <hr />
        <section>
          <div className="container">
            <h2>Compare By Areas</h2>
            <div className="col-lg-8 col-lg-offset-2 col-md-8 col-md-offset-2 col-sm-12 col-xs-12">

              <div className="input-container col-lg-12 col-md-12 col-sm-12 col-xs-12">
                <div className="col-lg-3 col-md-3 col-sm-6 col-xs-12">
                  <div className="input-label">NO. Of Bedrooms</div>
                  <select onChange={this.updateOption} name="nobed">
                    {this.getOptions()}
                  </select>
                </div>
                <div className="col-lg-3 col-md-3 col-sm-6 col-xs-12">
                  <div className="input-label">NO. Of Bathrooms</div>
                  <select onChange={this.updateOption} name="nobath">
                    {this.getOptions()}
                  </select>
                </div>
                <div className="col-lg-3 col-md-3 col-sm-6 col-xs-12">
                  <div className="input-label">NO. Of Toilets</div>
                  <select onChange={this.updateOption} name="notoilets">
                    {this.getOptions()}
                  </select>
                </div>

                <div className="col-lg-3 col-md-3 col-sm-6 col-xs-12">
                  <div className="input-label">Sort</div>
                  <select name="sort" onChange={this.updateOption}>
                    <option value="high">High</option>
                    <option value="low">Low</option>                  
                  </select>
                </div>
              </div>

            </div>

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
    );
  }
}

export default withGoogleMap(App);
