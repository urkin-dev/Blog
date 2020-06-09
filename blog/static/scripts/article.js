let
    loadBtn        = document.querySelector('.load-btn'),
    container      = document.querySelector('.comments'), 
    likeBtn        = document.querySelector('.like-btn'),
    commentsLoaded = document.querySelectorAll(`.comments .comment`).length,
    commentForm    = document.querySelector('.comments__form');

if (commentsLoaded >= 10) {
    loadBtn.style.display = 'flex';
}

loadBtn.addEventListener('click', getComments); // Get comments from server
likeBtn.addEventListener('click', sendLike);

commentForm.onsubmit = function() {

    var articleID = new URL(window.location.href).searchParams.get("id");

    const text = this.elements.text.value;

    const data = {text};

    const csrftoken = getCookie('csrftoken');

    fetch(`${articleID}/leave_comment/`, {method: "POST", body: JSON.stringify(data), headers: {'Accept': 'application/json',
    'Content-Type': 'application/json', 'X-CSRFToken': csrftoken}})
        .then(res => res.json())
        .then(comment => {
            if (comment.authenticated == false) {
                window.location.href = '/login/';
            } else {
                updateComments(comment);
            }
        })
        .catch(err => console.log(err));
    
    this.elements.text.value = ``;
    
    return false;

}

/**
 * Get ten comments of current article from DB and increases count of comments
 */
function getComments() {
    
    loadBtn.textContent = 'Загрузка...';

    fetch(`/loadComments?count=${commentsLoaded}`, {method: "GET"})
        .then(res => res.json())
        .then(comments => {
            if (comments.length == 0) {
                showMessage('Комментариев больше нет');
            } else {
                commentsLoaded += comments.length;
                createComments(comments);
                loadBtn.innerHTML = `Загрузить ещё
                <svg width="21" height="21" viewBox="0 0 21 21">
                    <path d="M4 7.33L10.03 14l.5.55.5-.55 5.96-6.6-.98-.9-5.98 6.6h1L4.98 6.45z" fill-rule="evenodd"></path>
                </svg>`
            }
        })
        .catch((e) => {
            console.log(e);
            showMessage('Произошла ошибка');
        });

}

/**
 * Create comment's card
 * @param {Array} comments array with 10 comments
 */
function createComments(comments) {
    
    for (let i = 0; i < comments.length; i++) {

        let
            id           = comments[i].id,
            name         = comments[i].author_name,
            pub_date     = comments[i].pub_date,
            comment_text = comments[i].text;

        let
            comment      = document.createElement('div'),
            about_author = document.createElement('div'),
            text         = document.createElement('p'),
            avatar_a     = document.createElement('a'),
            avatar_img   = document.createElement('img'),
            info         = document.createElement('div'),
            author_name  = document.createElement('a'),
            date         = document.createElement('span');
        
        comment.classList.add('comment');
        about_author.classList.add('about_author');
        text.classList.add('comment-text');
        avatar_a.classList.add('avatar');
        info.classList.add('author-info');
        author_name.classList.add('author-info__name');
        date.classList.add('date');

        comment.appendChild(about_author);
        about_author.appendChild(avatar_a);
        avatar_a.appendChild(avatar_img);
        about_author.appendChild(info);
        info.appendChild(author_name);
        info.appendChild(date);
        comment.appendChild(text);

        author_name.textContent = name;
        date.textContent        = pub_date;
        text.textContent        = comment_text;

        container.insertBefore(comment, loadBtn);

    }

}

/**
 * Insert new comment before others
 * @param {Object} newCOmment new comment from server
 */
function updateComments(newComment) {
    
    let message = document.querySelector('.no-comments');

    if (message) {
        message.style.display = 'none';
    }

    let
        id           = newComment.id,
        name         = newComment.author_name,
        pub_date     = newComment.pub_date,
        comment_text = newComment.text;

    let
        comment      = document.createElement('div'),
        about_author = document.createElement('div'),
        text         = document.createElement('p'),
        avatar_a     = document.createElement('a'),
        avatar_img   = document.createElement('img'),
        info         = document.createElement('div'),
        author_name  = document.createElement('a'),
        date         = document.createElement('span');
    
    comment.classList.add('comment');
    about_author.classList.add('about_author');
    text.classList.add('comment-text');
    avatar_a.classList.add('avatar');
    info.classList.add('author-info');
    author_name.classList.add('author-info__name');
    date.classList.add('date');

    comment.appendChild(about_author);
    about_author.appendChild(avatar_a);
    avatar_a.appendChild(avatar_img);
    about_author.appendChild(info);
    info.appendChild(author_name);
    info.appendChild(date);
    comment.appendChild(text);

    author_name.textContent = name;
    date.textContent        = pub_date;
    text.textContent        = comment_text;

    container.insertBefore(comment, document.querySelectorAll('.comment')[0]);
}

function showMessage(message) {
    el = document.createElement(`p`);
    el.classList.add("load-message");
    el.textContent = message;

    loadBtn.remove();
    container.appendChild(el);
}

function sendLike(e) {
    alert("Not working yet)");
}

// TODO: Get it
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