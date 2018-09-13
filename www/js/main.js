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
      setCheckVal('Bus', set.byBus)
      setCheckVal('Tram', set.byTram)
      setCheckVal('Trein', set.byTrain)
      setCheckVal('Veerboot', set.byFerry)
      setCheckVal('Metro', set.bySubway)

      //alar settings
      setVal('Uurkleur', set.kleur_primary)
      setVal('Minuutkleur', set.kleur_secondary)
      setVal('Alarmvolume', set.alarmVolume)
      setVal('Extrawektijd', set.snoozeBuffer)

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
          setCheckVal('OV', true)
          setCheckVal('Lopend', false)
          setCheckVal('Fiets', false)
          setCheckVal('Auto', false)
          break;
        case 'Lopend':
          setCheckVal('Lopend', true)
          setCheckVal('OV', false)
          setCheckVal('Fiets', false)
          setCheckVal('Auto', false)
          break;
        case 'Fiets':
          setCheckVal('Fiets', true)
          setCheckVal('Lopend', false)
          setCheckVal('OV', false)
          setCheckVal('Auto', false)
          break;
        case 'Auto':
          setCheckVal('Auto', true)
          setCheckVal('Lopend', false)
          setCheckVal('Fiets', false)
          setCheckVal('OV', false)
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
