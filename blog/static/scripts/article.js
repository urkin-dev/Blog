let
    loadBtn        = document.querySelector('.load-btn'),
    container      = document.querySelector('.comments'), 
    likeBtn        = document.querySelector('.like-btn'),
    commentsLoaded = document.querySelectorAll(`.comments .comment`).length,
    commentForm    = document.querySelector('.comments__form'),
    deleteBtns     = document.querySelectorAll('.comments .delete_comment');

if (commentsLoaded >= 10) {
    loadBtn.style.display = 'flex';
}

loadBtn.addEventListener('click', getComments); // Get comments from server
likeBtn.addEventListener('click', sendLike);

deleteBtns.forEach(btn => {
    btn.addEventListener('click', deleteComment)
});

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
            image        = comments[i].image
            author_id    = comments[i].author_id,
            pub_date     = comments[i].pub_date,
            comment_text = comments[i].text;

        let
            comment      = document.createElement('div'),
            about_author = document.createElement('div'),
            about_wrap   = document.createElement('div'),
            text         = document.createElement('p'),
            avatar_a     = document.createElement('a'),
            avatar_img   = document.createElement('img'),
            info         = document.createElement('div'),
            author_name  = document.createElement('a'),
            date         = document.createElement('span');
        
        comment.classList.add('comment');
        about_author.classList.add('comment__about_author');
        about_wrap.classList.add('about_author-wrap')
        text.classList.add('comment-text');
        avatar_a.classList.add('avatar');
        info.classList.add('author-info');
        author_name.classList.add('author-info__name');
        date.classList.add('date');

        comment.appendChild(about_author);
        about_author.appendChild(about_wrap);
        about_wrap.appendChild(avatar_a);
        avatar_a.appendChild(avatar_img);
        about_wrap.appendChild(info);
        info.appendChild(author_name);
        info.appendChild(date);
        comment.appendChild(text);

        comment.setAttribute('data-id', id);
        author_name.textContent = name;
        avatar_img.src          = image;
        author_name.href        = `/profile?id=${author_id}`;
        avatar_a.href           = `/profile?id=${author_id}`;
        date.textContent        = pub_date;
        text.textContent        = comment_text;

        if (comments[i]['show-delete']) {
            delete_p     = document.createElement('p');
            about_author.appendChild(delete_p)
            delete_p.title          = 'Удалить комментари'; 
            delete_p.style          = 'margin: 0'; 
            delete_p.innerHTML = `
                <svg class="delete_comment" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">
                    <path d="M38 12.83L35.17 10 24 21.17 12.83 10 10 12.83 21.17 24 10 35.17 12.83 38 24 26.83 35.17 38 38 35.17 26.83 24z"/>
                </svg>`;

                let btn = delete_p.children[0];

                btn.addEventListener('click', deleteComment);
        }


        container.insertBefore(comment, loadBtn);

    }

}

function deleteComment() {

    const comment = this.parentNode.parentNode.parentNode; // Get comment
    const commentId = comment.dataset.id;

    fetch(`/deleteComment?id=${commentId}`, {method: "GET"})
        .then(res => {
            if (res.status == 404 || res.status == 500) {
                alert('Error');
            } else {
                comment.remove();
            }
        })
        .catch((e) => {
            console.log(e);
            alert('Error');
        });

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
        image        = newComment.image
        name         = newComment.author_name,
        author_id    = newComment.author_id,
        pub_date     = newComment.pub_date,
        comment_text = newComment.text;

    let
        comment      = document.createElement('div'),
        about_author = document.createElement('div'),
        about_wrap   = document.createElement('div'),
        text         = document.createElement('p'),
        avatar_a     = document.createElement('a'),
        avatar_img   = document.createElement('img'),
        info         = document.createElement('div'),
        author_name  = document.createElement('a'),
        date         = document.createElement('span');
    
    comment.classList.add('comment');
    about_author.classList.add('comment__about_author');
    about_wrap.classList.add('about_author-wrap')
    text.classList.add('comment-text');
    avatar_a.classList.add('avatar');
    info.classList.add('author-info');
    author_name.classList.add('author-info__name');
    date.classList.add('date');

    comment.appendChild(about_author);
    about_author.appendChild(about_wrap);
    about_wrap.appendChild(avatar_a);
    avatar_a.appendChild(avatar_img);
    about_wrap.appendChild(info);
    info.appendChild(author_name);
    info.appendChild(date);
    comment.appendChild(text);
 
    comment.setAttribute('data-id', id);
    author_name.textContent = name;
    avatar_img.src = image;
    author_name.href        = `/profile?id=${author_id}`;
    avatar_a.href           = `/profile?id=${author_id}`;
    date.textContent        = pub_date;
    text.textContent        = comment_text;

    if (newComment['show-delete']) {
        delete_p     = document.createElement('p');
        about_author.appendChild(delete_p)
        delete_p.title          = 'Удалить комментари'; 
        delete_p.style          = 'margin: 0'; 
        delete_p.innerHTML = `
            <svg class="delete_comment" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">
                <path d="M38 12.83L35.17 10 24 21.17 12.83 10 10 12.83 21.17 24 10 35.17 12.83 38 24 26.83 35.17 38 38 35.17 26.83 24z"/>
            </svg>`;

        let btn = delete_p.children[0];

        btn.addEventListener('click', deleteComment);
    }

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