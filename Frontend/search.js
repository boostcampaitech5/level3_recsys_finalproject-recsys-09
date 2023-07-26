// 자동 완성 기능 구현
var $autoComplete = document.getElementsByName("autocomplete");
var $search = document.getElementsByName("search");

$search.forEach(search => search.addEventListener('input', makeAutocomplete));

function makeAutocomplete(event) {
  const search = event.target;
  const value = search.value.trim().toLowerCase();
  const matchDataList = value
    ? dataList.filter((label) => label.toLowerCase().includes(value))
    : [];

  showList(matchDataList, value, search);

  $autoComplete.forEach((auto) => {
    auto.addEventListener("click", (event) => {
      if (event.target.tagName === "MARK") {
        const clickedItem = event.target.parentElement.textContent.trim();
        const searchInput = auto.previousElementSibling;
        searchInput.value = clickedItem;
      }
      else {
        const clickedItem = event.target.textContent.trim();
        const searchInput = auto.previousElementSibling;
        searchInput.value = clickedItem;
      }
      auto.innerHTML = ""; // Hide autocomplete results after clicking a suggestion
    });
  });
}

const showList = (data, value, search) => {
  // 정규식으로 변환
  const regex = new RegExp(`(${value})`, "gi");
  const auto = search.nextElementSibling;
  auto.innerHTML = data
    .map(
      (label) => `<div>${label.replace(regex, "<mark>$1</mark>")}</div>`
    )
    .join("");

};