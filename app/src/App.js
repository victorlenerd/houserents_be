import React, { Component } from 'react';
import './App.css';

import Header from './components/header';
import Footer from './components/footer';
import Source from './components/source';

class App extends Component {
  render() {
    return (
      <div className="App">
        <Header />
        <section>
          <div className="container">
            <h2>Discover By Address</h2>
          </div>
        </section>
        <hr />
        <section>
          <div className="container">
            <h2>Compare By Areas</h2>
          </div>
        </section>
        <Source />
        <Footer />
      </div>
    );
  }
}

export default App;
