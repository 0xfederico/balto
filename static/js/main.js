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
