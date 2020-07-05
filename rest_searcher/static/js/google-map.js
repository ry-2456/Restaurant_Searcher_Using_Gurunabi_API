let restName = "マクドナルド";
let restLat = 35.6811673;
let restLng = 139.7670516;
let restPos = new google.maps.LatLng(restLat, restLng);

let Options = {
  zoom: 15,
  center: restPos,
  MapTypeId: 'roadmap'
};

// マップを作る
let map = new google.maps.Map(document.getElementById('map-canvas'), Options);

// Markerを立てる
let marker = new google.maps.Marker({
  position: restPos,
  map: map,
  title: restName
});
