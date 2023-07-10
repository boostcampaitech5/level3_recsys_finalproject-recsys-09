//세부 연령 활성화, 비활성화 함수
function fieldsetActive()  {
    const target = document.getElementById('young');
    target.disabled = false;
  }

function fieldsetDisable()  {
    const target = document.getElementById('young');
    target.disabled = true;
  }