var settings = null

function getSettings() {
  var xmlhttp = new XMLHttpRequest();
  var url = window.location.origin + '/api/getSettings.py'

  //event that gets called everytime the request status changes
  xmlhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      set = JSON.parse(this.responseText)
      //update front-end with the new parsed settings

      //user settings
      setVal('firstname', set.voornaam)
      setVal('lastname', set.achternaam)
      setVal('straat', set.straat)
      setVal('huisnummer', set.huisnummer)
      setVal('postcode', set.postcode)
      setVal('woonplaats', set.woonplaats)
      setVal('klas', set.klas)

      //vervoer settings
      setCheckVal('bus', set.byBus)
      setCheckVal('tram', set.byTram)
      setCheckVal('trein', set.byTrain)
      setCheckVal('veerboot', set.byFerry)
      setCheckVal('metro', set.bySubway)

      //alar settings
      setVal('uurkleur', set.kleur_primary)
      setVal('minuutkleur', set.kleur_secondary)
      setVal('alarmvolume', set.alarmVolume)
      setVal('extrawektijd', set.snoozeBuffer)

      //radio buttons
      switch (set.geslacht) {
        case 'M':
          setCheckVal('genderM', true)
          setCheckVal('genderF', false)
          setCheckVal('genderO', false)
          break;
        case 'F':
          setCheckVal('genderF', true)
          setCheckVal('genderM', false)
          setCheckVal('genderO', false)
          break;
        default:
          setCheckVal('genderO', true)
          setCheckVal('genderM', false)
          setCheckVal('genderF', false)
      }

      switch (set.vervoer) {
        case 'OV':
          setCheckVal('ov', true)
          setCheckVal('lopend', false)
          setCheckVal('fiets', false)
          setCheckVal('auto', false)
          break;
        case 'Lopend':
          setCheckVal('lopend', true)
          setCheckVal('ov', false)
          setCheckVal('fiets', false)
          setCheckVal('auto', false)
          break;
        case 'Fiets':
          setCheckVal('fiets', true)
          setCheckVal('lopend', false)
          setCheckVal('ov', false)
          setCheckVal('auto', false)
          break;
        case 'Auto':
          setCheckVal('auto', true)
          setCheckVal('lopend', false)
          setCheckVal('fiets', false)
          setCheckVal('ov', false)
          break;

      }
    }
  }

  //actually fires the request
  xmlhttp.open("GET", url, true);
  xmlhttp.send();
}

function setVal (el, val) {
    document.getElementById(el).value = val
}

function setCheckVal(el, val) {
  document.getElementById(el).checked = val
}

function getVal (el) {
  return document.getElementById(el).value;
}

function getCheckVal(el) {
  return document.getElementById(el).checked;
}

function updateSettings() {
  var xmlhttp = new XMLHttpRequest();
  var url = window.location.origin + '/api/setSettings.py'


  xmlhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      //succes
      alert('Updated settings')
      getSettings() // refreshes them from database to ensure it updated
    } else if (this.status == 500) {
      //failed
      alert('Failed to update the settings...')
    }
  }

 var settings = {
   'voornaam': getVal('firstname'),
   'achternaam': getVal('lastname'),
   'straat': getVal('straat'),
   'postcode': getVal('postcode'),
   'huisnummer': getVal('huisnummer'),
   'wooonplaats': getVal('woonplaats'),
   'klas': getVal('klas'),

   'byBus': getCheckVal('bus'),
   'byTrain': getCheckVal('trein'),
   'byFerry': getCheckVal('veerboot'),
   'byTram': getCheckVal('tram'),
   'bySubway': getCheckVal('metro'),

   'kleur_primary': getVal('uurkleur'),
   'kleur_secondary': getVal('minuutkleur'),
   'alarmVolume': getVal('alarmvolume'),
   'snoozeBuffer': getVal('extrawektijd')
 }

 //vervoer
 if (getCheckVal('lopend')) {
   settings.vervoer = 'lopend'
 } else if (getCheckVal('fiets')) {
   settings.vervoer = 'fiets'
 } else if (getCheckVal('auto')) {
   settings.vervoer = "auto"
 } else {
   //defaults to OV
   settings.vervoer = 'OV'
 }

 //gender
 if (getCheckVal('genderM')) {
   settings.geslacht = 'M'
 } else if (getCheckVal('genderF')) {
  settings.geslacht = 'F'
 } else {
   //defaults to other
   settings.geslacht = 'O'
 }

 var params = '';

 for(var key in settings) {
   params += key + '=' + settings[key] + '&'
}

  params = params.slice(0, -1)

  xmlhttp.open("POST", url, true);
  xmlhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xmlhttp.send(params)

}

//gets the settings as soon as the page loads
window.onload = function() {
  getSettings()
}
