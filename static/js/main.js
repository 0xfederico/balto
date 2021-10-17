//generic filter of elements
function filterElements(input) {
    let inp = input.value.toLowerCase();
    let table = document.querySelectorAll(".table")[0];
    let rows = table.tBodies[0].children;
    for (let i = 0; i < rows.length; i++){
        if (inp.length == 0)
            rows[i].style.display = "table-row";
        else {
            let columns = rows[i].children;
            for (let j = 0; j < columns.length; j++){
                if (columns[j].textContent.toLowerCase().includes(inp)){
                    rows[i].style.display = "table-row";
                    break;
                }
                else
                    rows[i].style.display = "none";
            }
        }
    }
}

//FilteredSelectMultiple filter elements
function FSM_filter(input, choose_all, deselect_all) {
  let inp = input.value.toLowerCase();
  let list_group_container = document.querySelectorAll("#list-group-scrollbar-container")[0];
  let list_group = list_group_container.children[0].children;

  if (choose_all) {
    for (let i = 0; i < list_group.length - 1; i++)
      list_group[i].firstChild.checked = true;
    return;
  }

  if (deselect_all) {
    for (let i = 0; i < list_group.length; i++)
      list_group[i].firstChild.checked = false;
    return;
  }

  for (let i = 0; i < list_group.length; i++) {
    if (list_group[i].tagName == "LABEL") {
      if (inp.length == 0)
        list_group[i].style.display = "flex";
      else {
        if (list_group[i].textContent.toLowerCase().includes(inp))
          list_group[i].style.display = "flex";
        else
          list_group[i].style.display = "none";
      }
    }
  }
}

//FilteredSelectMultiple clear filter
function FSM_clear_input() {
  let input = document.querySelectorAll("#list-group-input-search")[0];
  input.value = '';
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

//retrieve csrf token
function getCSRFCookie() {
    name = "csrftoken";
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// these HTTP methods do not require CSRF protection
function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

//mark notification as read
function notification_read(post_url, pk) {
    let csrftoken = getCSRFCookie();
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $.ajax({
      type: "POST",
      url: post_url,
      data: {
        'notification_pk': pk
      },
    });
}

//notify user
function notify_user(title, textbody, img, onclose_url, onclose_pk, onclick_url) {
  // Let's check if the browser supports notifications
  if (!("Notification" in window)) {
    alert("This browser does not support desktop notification");
  }
  // Let's check whether notification permissions have already been granted
  else if (Notification.permission === "granted") {
    // If it's okay let's create a notification
    var notify = new Notification(title, {
      body: textbody,
      icon: img,
    });
    notify.onclose = function() {
      notification_read(onclose_url, onclose_pk);
    };
    notify.onclick = function(event) {
      notification_read(onclose_url, onclose_pk);
      window.location.replace(onclick_url);
    }
  }
  // Otherwise, we need to ask the user for permission
  else if (Notification.permission !== "denied") {
    Notification.requestPermission().then(function(permission) {
      // If the user accepts, let's create a notification
      var notify = new Notification(title, {
        body: textbody,
        icon: img,
      });
      notify.onclose = function() {
        notification_closed(onclose_url, onclose_pk);
      };
      notify.onclick = function(event) {
        notification_read(onclose_url, onclose_pk);
        window.location.replace(onclick_url);
      }
    });
  }

  // At last, if the user has denied notifications, and you
  // want to be respectful there is no need to bother them any more.
}
