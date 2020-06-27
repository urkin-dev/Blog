let 
    closeBtn = document.querySelector('.close'),
    editForm = document.querySelector('.edit-form');

closeBtn.addEventListener('click', () => window.location.href = `/profile?id=${id}`);

let load = document.querySelector('.svg-photo');
load.addEventListener('click', () => alert('Not working yet'));

editForm.onsubmit = function() {

    const username = this.elements.username.value;
    const bio      = this.elements.bio.value;

    const data = {username, bio};

    const csrftoken = getCookie('csrftoken');

    fetch(`/profile/save`, {method: "POST", body: JSON.stringify(data), headers: {'Accept': 'application/json',
    'Content-Type': 'application/json', 'X-CSRFToken': csrftoken}})
        .then(res => {
            if (res.status == 404 || res.status == 500) {
                showError(res.statusText);
            } else {
                return res.json();
            }
        })
        .then(data => {
            window.location.href = `/profile?id=${id}`;
        })
        .catch(e => console.log(e));

    return false;

}

function showError(e) {

    if (document.querySelector('.edit-error')) {
        return;
    }

    let p = document.createElement('p');
    p.classList.add('edit-error');

    p.textContent = 'Произошла ошибка';

    editForm.appendChild(p);
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}