navigator.geolocation.getCurrentPosition(function(pos){
    document.getElementById("lat").value = pos.coords.latitude;
    document.getElementById("lon").value = pos.coords.longitude;
});