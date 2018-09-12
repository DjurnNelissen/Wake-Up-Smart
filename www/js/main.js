function getSettings() {
  var xmlhttp = new XMLHttpRequest();
  var url = window.location.origin + '/api/getSettings.py'

  //event that gets called everytime the request status changes
  xmlhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var settings = JSON.parse(this.responseText)
      //update front-end with the new parsed settings
    }
  }

  //actually fires the request
  xmlhttp.open("GET", url, true);
  xmlhttp.send();
}

//gets the settings as soon as the page loads
window.onload = function() {
  getSettings()
}
