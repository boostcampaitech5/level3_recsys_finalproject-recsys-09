const ageInput = document.getElementsByName('age')
const youngInput = document.getElementsByName('young')
const platformInput = document.getElementsByName('platform')
const playerInput = document.getElementsByName('players')
const genreInput = document.getElementsByName('genre')
const tagInput = document.getElementsByName('tag')
const gameInput = document.getElementById('search')
const submit = document.getElementById('submit')

function checkFormValidity() {
    if (ageInput.value && youngInput.value && platformInput.value && playerInput.value && genreInput.value && tagInput.value && gameInput.value) {
      submit.disabled = false; // 제출 버튼 활성화
    } else {
      submit.disabled = true; // 제출 버튼 비활성화
    }
}

submit.disabled = true;

ageInput.addEventListener('input', checkFormValidity);
youngInput.addEventListener('input', checkFormValidity);
platformInput.addEventListener('input', checkFormValidity);
playerInput.addEventListener('input', checkFormValidity);
genreInput.addEventListener('input', checkFormValidity);
tagInput.addEventListener('input', checkFormValidity);
gameInput.addEventListener('input', checkFormValidity);

checkFormValidity();