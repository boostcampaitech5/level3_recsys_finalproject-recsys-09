const ageInput = document.getElementsByName('age')
const youngInput = document.getElementsByName('young')
const platformInput = document.getElementsByName('platform')
const playerInput = document.getElementsByName('players')
const genreInput = document.getElementsByName('genre')
const tagInput = document.getElementsByName('tag')
const submit = document.getElementById('submit')

let validate = {
  "ageInput" : false,
  "platformInput" : false,
  "playerInput" : false,
  "genreInput" : false,
  "tagInput" : false,
}

ageInput.forEach(age => age.addEventListener('input', checkFormValidity));
youngInput.forEach(young => young.addEventListener('input', checkFormValidity));
platformInput.forEach(platform => platform.addEventListener('input', checkFormValidity));
playerInput.forEach(player => player.addEventListener('input', checkFormValidity));
genreInput.forEach(genre => genre.addEventListener('input', checkFormValidity));
tagInput.forEach(tag => tag.addEventListener('input', checkFormValidity));

function checkFormValidity() {
  checkElement();
  if (validate["ageInput"] && validate["platformInput"] && validate["playerInput"] && validate["genreInput"] && validate["tagInput"]) {
    submit.disabled = false; // 제출 버튼 활성화
  } else {
    submit.disabled = true; // 제출 버튼 비활성화
  }
}

function checkElement(){
  // false로 초기화
  let youngValue = false
  let platformValue = false
  let playerValue = false
  let genreValue = false
  let tagValue = false

  if (ageInput[0].checked) {
    validate["ageInput"] = true
  }
  
  if (ageInput[1].checked) {
    youngInput.forEach(function(young){
      if (young.checked) {
        youngValue = true
      }
    })
    validate["ageInput"] = youngValue
  }

  platformInput.forEach(function(platform){
    if (platform.checked) {
      platformValue = true
    }
  })

  playerInput.forEach(function(player){
    if (player.checked) {
      playerValue = true
    }
  })

  genreInput.forEach(function(genre){
      if (genre.checked) {
        genreValue = true // 하나라도 check 되어있으면 true
      }
  })
  
  tagInput.forEach(function(tag){
    if (tag.checked) {
      tagValue = true
    }
  })

  validate["platformInput"] = platformValue
  validate["playerInput"] = playerValue
  validate["genreInput"]= genreValue
  validate["tagInput"] = tagValue
}
