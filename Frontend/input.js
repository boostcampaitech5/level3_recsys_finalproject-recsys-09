//세부 연령 활성화, 비활성화 함수
function fieldsetActive()  {
    const target = document.getElementById('young');
    target.disabled = false;
  }

function fieldsetDisable()  {
    const target = document.getElementById('young');
    target.disabled = true;

    const young = document.getElementsByName('young')
    young.forEach((checkbox) => {
      checkbox.checked = false;
    })
  }

//전체 선택 함수
function selectAll(selectAll)  {
  const checkboxes 
        = document.getElementsByName('genre');
  
  checkboxes.forEach((checkbox) => {
    checkbox.checked = selectAll.checked;
  })
}

function checkSelectAll()  {
  // 전체 체크박스
  const checkboxes 
    = document.querySelectorAll('input[name="genre"]');
  // 선택된 체크박스
  const checked 
    = document.querySelectorAll('input[name="genre"]:checked');
  // select all 체크박스
  const selectAll 
    = document.querySelector('input[name="selectall"]');
  
  if(checkboxes.length === checked.length)  {
    selectAll.checked = true;
  }else {
    selectAll.checked = false;
  }

}


//난이도 하나만 체크되도록
function hardLevelSelect() {
  const target = document.getElementById('easy');
  target.checked = false;
}

function easyLevelSelect() {
  const target = document.getElementById('hard');
  target.checked = false;
}

//tag 상관없음 함수
function dontCare() {
  const checkboxes = document.getElementsByName('tag');
  const dontcare = document.getElementById('none');

  checkboxes.forEach((checkbox) => {
    checkbox.checked = false;
  })

  dontcare.checked = true;
  
}

//tag 선택시 상관없음 항목이 체크 안되도록 하는 함수
function dontCareDisable() {
  const dontcare = document.getElementById('none');
  dontcare.checked = false;
}