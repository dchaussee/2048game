/* Melissa Kaufman-Gomez
mhk2149 */

var key = "AIzaSyAT8Ir0WUSjGsXh6dl3x6a_NGQob5NIzyc";
var url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?";
var url2 = "https://maps.googleapis.com/maps/api/geocode/json?"
var latLon = {};
var map;
var infowindow;

function apiCall() {

	var address = document.getElementById("address").value;
	$.ajax({
		url: url2,
		data: {
			address: address,
			key: key
		},
	    type: 'GET',
		success: function(res) {
			latLon = res.results[0].geometry.location;
			console.log(latLon);		
		}
	});
	// initialize();
}

function initialize() {
	  
	map = new google.maps.Map(document.getElementById('map'), {
		center: latLon,
		zoom: 15
	});

	infowindow = new google.maps.InfoWindow();

	var service = new google.maps.places.PlacesService(map);
	service.nearbySearch({
		location: latLon,
		radius: 500
	}, callback);


	google.maps.event.addListener(marker, 'click', function() {
		infowindow.setContent(place.name);
		infowindow.open(map, this);
	});
}


function callback(results, status) {
	if (status === google.maps.places.PlacesServiceStatus.OK) {
		for (var i = 0; i < results.length; i++) {
			createMarker(results[i]);
		}
	}
}

function createMarker(place) {
	var placeLoc = place.geometry.location;
	var marker = new google.maps.Marker({
  		map: map,
  		position: place.geometry.location
	});
}
