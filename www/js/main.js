var settings = null

function getSettings() {
  var xmlhttp = new XMLHttpRequest();
  var url = window.location.origin + '/api/getSettings.py'

  //event that gets called everytime the request status changes
  xmlhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      set = JSON.parse(this.responseText)
      //update front-end with the new parsed settings
      setVal('firstname', set.voornaam)
      setVal('lastname', set.achternaam)
      setVal('straat', set.straat)
      setVal('huisnummer', set.huisnummer)
    }
  }

  //actually fires the request
  xmlhttp.open("GET", url, true);
  xmlhttp.send();
}

function setVal (el, val) {
    document.getElementById(el).value = val
}

function getVal (el) {
  return document.getElementById('textbox_id').value
}

function updateSettings() {
  var xmlhttp = new XMLHttpRequest();
  var url = window.location.origin + '/api/setSettings.py'

  xmlhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      //succes
    } else if (this.status == 500) {
      //failed
      alert('Failed to update the settings...')
    }
  }

  xmlhttp.open("POST", url, true);
  xmlhttp.send()

}

//gets the settings as soon as the page loads
window.onload = function() {
  getSettings()
}
