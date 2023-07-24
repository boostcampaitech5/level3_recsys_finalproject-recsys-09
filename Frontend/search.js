// 자동 완성 기능 구현
const $autoComplete = document.querySelector(".autocomplete");

var $search = document.getElementsByName("search");

$search.forEach(search => search.addEventListener('input', makeAutocomplete));

function makeAutocomplete() {
  $search.forEach((search) => {
    search.addEventListener("input", (event) => {
      const value = search.value.trim().toLowerCase();
      const matchDataList = value
        ? dataList.filter((label) => label.toLowerCase().includes(value))
        : [];
  
      showList(matchDataList, value);
    });
  });  
  
  $autoComplete.addEventListener("click", (event) => {
    const clickedItem = event.target.textContent;

    if ($autoComplete.previousElementSibling.previousElementSibling.id === "firstsearch") {
      const searchInput = $autoComplete.previousElementSibling.previousElementSibling.previousElementSibling;
      searchInput.value = clickedItem;
    }
    else {
      const searchP = $autoComplete.previousElementSibling.previousElementSibling;
      const searchInput = searchP.querySelector("input");
      searchInput.value = clickedItem;
    }
    $autoComplete.innerHTML = ""; // Hide autocomplete results after clicking a suggestion
  });
}



const showList = (data, value, nowIndex) => {
  // 정규식으로 변환
  const regex = new RegExp(`(${value})`, "gi");
  
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