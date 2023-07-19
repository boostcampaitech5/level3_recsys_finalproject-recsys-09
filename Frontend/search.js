// 자동 완성 기능 구현
const $autoComplete = document.querySelector(".autocomplete");

var $search = document.getElementsByName("search");
//const $search = document.querySelectorAll("input[name=search]");

$search.forEach(search => search.addEventListener('input', makeAutocomplete));

function makeAutocomplete() {
  $search.forEach(function(search){
    let nowIndex = 0;
  
    search.onkeyup = (event) => {
      // 검색어
      const value = search.value.trim().toLowerCase();
      // 자동완성 필터링
      const matchDataList = value
        ? dataList.filter((label) => label.includes(value))
        : [];
  
      switch (event.keyCode) {
        // UP KEY
        case 38:
          nowIndex = Math.max(nowIndex - 1, 0);
          break;
  
        // DOWN KEY
        case 40:
          nowIndex = Math.min(nowIndex + 1, matchDataList.length - 1);
          break;
  
        // ENTER KEY
        case 13:
          search.value = matchDataList[nowIndex] || "";
  
          // 초기화
          nowIndex = 0;
          matchDataList.length = 0;
          break;
          
        // 그외 다시 초기화
        default:
          nowIndex = 0;
          break;
      }
  
      // 리스트 보여주기
      showList(matchDataList, value, nowIndex);
    };
  })
}



const showList = (data, value, nowIndex) => {
  // 정규식으로 변환
  const regex = new RegExp(`(${value})`, "g");
  
  $autoComplete.innerHTML = data
    .map(
      (label, index) => `
      <div class='${nowIndex === index ? "active" : ""}'>
        ${label.replace(regex, "<mark>$1</mark>")}
      </div>
    `
    )
    .join("");
};