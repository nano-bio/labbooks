$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
  }
});
const spinnerLS = $('#spinner-laser-scan')
const gL = new Dygraph(document.getElementById("laser-scan-div"), [[0, 0]], {
  legend: 'always', labels: ['laser-related', `ID ${measurementId}`]
});
let backgroundMode = '';
let sectionsForeground = [];
let sectionsBackground = [];
let massColumn;
let xStart;
let xEnd;

initializeSectionsInputs()
getInputValues()
if (buildSectionsFormula())
  plotLaserScan()

$('#sectionsSettings').change(function () {
  getInputValues()
  if (buildSectionsFormula())
    plotLaserScan()
})

// Sections Settings
// --------------------------------------------------

function initializeSectionsInputs() {
  // mass
  const cookieMass = Cookies.get(experiment + 'LaserScanMass')
  if (cookieMass && typeof cookieMass === "string") $('#laser-scan-input-mass').val(cookieMass)

  // x start & x end
  xStart = Cookies.get(experiment + 'LaserScanXStart')
  if (xStart && typeof xStart === "string") $('#laser-scan-input-x-start').val(xStart)
  xEnd = Cookies.get(experiment + 'LaserScanXEnd')
  if (xEnd && typeof xEnd === "string") $('#laser-scan-input-x-end').val(xEnd)

  // background mode
  backgroundMode = Cookies.get(experiment + 'LaserScanBackgroundMode') || 'divide';
  $(`input:radio[value=${backgroundMode}]`).prop('checked', true);

  // sections foreground
  const cookieSectionsForeground = Cookies.get(experiment + 'LaserScanSectionsForeground')
  if (cookieSectionsForeground && typeof cookieSectionsForeground === "string") {
    sectionsForeground = cookieSectionsForeground.split(',')
  } else {
    sectionsForeground = ['0']
  }
  $("input[type='checkbox'][name='sectionsForeground']").each(function () {
    if (sectionsForeground.includes($(this).val())) {
      $(this).prop('checked', true)
    }
  })

  // sections background
  const cookieSectionsBackground = Cookies.get(experiment + 'LaserScanSectionsBackground')
  if (cookieSectionsBackground && typeof cookieSectionsBackground === "string") {
    sectionsBackground = cookieSectionsBackground.split(',')
  } else {
    sectionsBackground = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
  }
  $("input[type='checkbox'][name='sectionsBackground']").each(function () {
    if (sectionsBackground.includes($(this).val())) {
      $(this).prop('checked', true)
    }
  })
}

function plotLaserScan() {
  spinnerLS.show('slow');

  $.post(url, {
    experiment: experiment,
    massColumn: massColumn,
    measurementId: measurementId,
    xStart: xStart,
    xEnd: xEnd,
    sectionsForeground: sectionsForeground.join(','),
    sectionsBackground: sectionsBackground.join(','),
    backgroundMode: backgroundMode
  }).done(function (data) {
    gL.updateOptions({'file': data.data});
  }).fail(function () {
    const text = (backgroundMode === 'divide') ? 'Maybe you try to divide by zero?' : 'Something went wrong'
    $.toast({
      heading: 'Error', text, showHideTransition: 'fade', icon: 'warning'
    })
  }).always(function () {
    spinnerLS.hide();
  });
}

function getInputValues() {
  massColumn = $('#laser-scan-input-mass').val();
  xStart = $('#laser-scan-input-x-start').val();
  xEnd = $('#laser-scan-input-x-end').val();

  sectionsForeground = []
  $("input[name=sectionsForeground]:checkbox:checked").each(function () {
    sectionsForeground.push($(this).val())
  });

  sectionsBackground = []
  $("input[name=sectionsBackground]:checkbox:checked").each(function () {
    sectionsBackground.push($(this).val())
  });

  backgroundMode = $("input[name='background-mode']:checked").val()

  Cookies.set(experiment + 'LaserScanMass', massColumn, {expires: 365})
  Cookies.set(experiment + 'LaserScanXStart', xStart, {expires: 365})
  Cookies.set(experiment + 'LaserScanXEnd', xEnd, {expires: 365})
  Cookies.set(experiment + 'LaserScanBackgroundMode', backgroundMode, {expires: 365})
  Cookies.set(experiment + 'LaserScanSectionsForeground', sectionsForeground.join(','), {expires: 365})
  Cookies.set(experiment + 'LaserScanSectionsBackground', sectionsBackground.join(','), {expires: 365})
}

function buildSectionsFormula() {
  let noError = true;

  $('#result-formula').text(() => {
    let returnString = ""
    if (sectionsForeground.length === 0) {
      noError = false;
      return "Select at least 1 section for the foreground!"
    }
    if (sectionsForeground.length === 1) {
      returnString = `Section(${sectionsForeground[0]})`
    } else {
      returnString = `Mean(${sectionsForeground.map(el => `Section(${el})`).join(", ")})`
    }

    let backgroundModeString = "";
    if (backgroundMode === 'none') {
      $('#sectionsBackground').css('visibility', 'hidden');
      return returnString
    } else {
      $('#sectionsBackground').css('visibility', 'visible');
      if (backgroundMode === 'diff') {
        backgroundModeString = " - "
      } else if (backgroundMode === 'divide') {
        backgroundModeString = " / "
      }
    }
    returnString += ` ${backgroundModeString} `

    if (sectionsBackground.length === 0) {
      noError = false;
      return "Select at least 1 section for the background!"
    }
    if (sectionsBackground.length === 1) return returnString + `Section(${sectionsBackground[0]})`
    return returnString + `Mean(${sectionsBackground.map(el => `Section(${el})`).join(", ")})`
  })
  return noError
}