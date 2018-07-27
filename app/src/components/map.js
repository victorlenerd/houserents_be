import React from 'react';
import { compose, withProps, lifecycle }  from "recompose";
import { withScriptjs, withGoogleMap, GoogleMap, Marker } from "react-google-maps";

const { SearchBox } = require("react-google-maps/lib/components/places/SearchBox");

const Map = compose(
    withProps({
      googleMapURL: "https://maps.googleapis.com/maps/api/js?key=AIzaSyCp3UKASbZkqvCnW3l_RLgM5Ik15JBKpPc&v=3.exp&libraries=places",
      containerElement: <div className="input-container" style={{ height: `300px`, width: '100%', paddingTop: 0, paddingBottom: 0 }} />,
      loadingElement: <div style={{ height: `300px` }} />,
      mapElement: <div style={{ height: `300px` }} />,
      center: { lat: 25.03, lng: 121.6 },
    }),
    lifecycle({
        componentWillMount() {
          const refs = {}
        
          this.setState({
            center: {
                lat: 6.5005, lng: 3.3666
            },
            onMapMounted: ref => {
              refs.map = ref;
            },
            onSearchBoxMounted: ref => {
              refs.searchBox = ref;
            },
            onPlacesChanged: () => {
                const places = refs.searchBox.getPlaces();

                if (places.length > 0) {
                    const place = places[0].geometry.location;
                    refs.map.panTo(place);
                    this.props.onCenterChange(place);
                    this.setState({
                      center: place
                    });
                }
            }
          })
        },
      }),
    withScriptjs,
    withGoogleMap
)(props =>
    <GoogleMap
        ref={props.onMapMounted}
        defaultZoom={15}
        defaultCenter={props.center}>
        <SearchBox
            ref={props.onSearchBoxMounted}
            controlPosition={window.google.maps.ControlPosition.LEFT_TOP}
            onPlacesChanged={props.onPlacesChanged}
        >
        <input
          type="text"
          placeholder="Type address e.g Yaba, adekunle"
          style={{
            boxSizing: `border-box`,
            border: `1px solid transparent`,
            width: `90%`,
            height: `32px`,
            marginLeft: `10px`,
            marginTop: `10px`,
            padding: `0 12px`,
            borderRadius: `3px`,
            boxShadow: `0 2px 6px rgba(0, 0, 0, 0.3)`,
            fontSize: `14px`,
            outline: `none`,
            textOverflow: `ellipses`,
          }}
        />
      </SearchBox>
        <Marker
            position={props.center}
            onClick={props.onToggleOpen}
        >
        </Marker>
    </GoogleMap>
);

export default Map