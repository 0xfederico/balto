//generic filter of elements
function filterElements(input) {
  let inp = input.value.toLowerCase();
  let table = document.querySelectorAll(".table")[0];
  let rows = table.tBodies[0].children;
  for (let i = 0; i < rows.length; i++) {
    if (inp.length == 0) {
      rows[i].style.display = "table-row";
    }
    else {
      let columns = rows[i].children;
      for (let j = 0; j < columns.length; j++) {
        if (columns[j].textContent.toLowerCase().includes(inp)) {
          rows[i].style.display = "table-row";
          break;
        }
        else {
          rows[i].style.display = "none";
        }
      }
    }
  }
}

//search page column filer
function filterBy(input, predicate) {
  let search_user_value = document.querySelector("#search-user").value.toLowerCase();
  let search_animal_value = document.querySelector("#search-animal").value.toLowerCase();
  let search_activity_value = document.querySelector("#search-activity").value.toLowerCase();
  let table = document.querySelector("#results-table");
  let user_clean = search_user_value.length == 0;
  let animal_clean = search_animal_value.length == 0;
  let activity_clean = search_activity_value.length == 0;
  let rows = table.tBodies[0].children;

  for (let i = 0; i < rows.length; i++) {
    if (user_clean && animal_clean && activity_clean) {
      rows[i].style.display = "table-row";
    }
    else {
      let columns = rows[i].children;
      if ((user_clean || columns[1].textContent.toLowerCase().includes(search_user_value)) &&
          (animal_clean || columns[2].textContent.toLowerCase().includes(search_animal_value)) &&
          (activity_clean || columns[3].textContent.toLowerCase().includes(search_activity_value))) {
          rows[i].style.display = "table-row";
      }
      else {
        rows[i].style.display = "none";
      }
    }
  }
}

//FilteredSelectMultiple filter elements
function FSM_filter(input, choose_all, deselect_all) {
  let inp = input.value.toLowerCase();
  let list_group_container = input.parentNode.parentNode.parentNode.querySelector('.list-group-scrollbar-container');
  let list_group = list_group_container.children[0].children;

  if (choose_all) {
    for (let i = 0; i < list_group.length - 1; i++) {
      if (list_group[i].style.display != "none") {
        list_group[i].firstChild.checked = true;
      }
    }
    return;
  }

  if (deselect_all) {
    for (let i = 0; i < list_group.length; i++) {
      list_group[i].firstChild.checked = false;
    }
    return;
  }

  for (let i = 0; i < list_group.length; i++) {
    if (list_group[i].tagName == "LABEL") {
      if (inp.length == 0) {
        list_group[i].style.display = "flex";
      }
      else {
        if (list_group[i].textContent.toLowerCase().includes(inp)) {
          list_group[i].style.display = "flex";
        }
        else {
          list_group[i].style.display = "none";
        }
      }
    }
  }
}

//FilteredSelectMultiple clear filter
function FSM_clear_input(button) {
  let input = button.parentNode.parentNode.children[0].children[0];
  input.value = "";
  FSM_filter(input, false, false);
}

//zoom image
function zoomImage(img) {
  let modalImg = document.querySelector("#imgmodal");
  modal.style.display = "block";
  modalImg.src = img.src;
}

function closeModal() {
  let modal = document.querySelector("#modal");
  modal.style.display = "none";
}

//scroll to top
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

//check if it is necessary to keep the notification area
function hide_notification_area() {
  notification_area = document.querySelector("#notifications-area");
  toasts = document.querySelectorAll("#notifications-area .toast");

  c_visible_elements = 0;
  for (let i = 0; i < toasts.length; i++) {
    if (toasts[i].classList.contains("show")) {
      c_visible_elements++;
    }
  }

  if (c_visible_elements <= 1) {
    notification_area.style.display = "none";
  }
}

//automatically show notifications
$(document).ready(function () {
  $(".toast").toast({ delay: 1000 * 60 * 60 * 24 * 365 }); //"no delay"
  $(".toast").toast("show");
});
