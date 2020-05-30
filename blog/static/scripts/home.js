let
    loadBtn        = document.querySelector('.load-btn'),
    container      = document.querySelector('.article-wrapper'), 
    likeBtns       = document.querySelectorAll('.like-btn'),
    articlesLoaded = 10;

loadBtn.addEventListener('click', getArticles); // Get articles from server
likeBtns.forEach(btn => {
    btn.addEventListener('click', sendLike);
});

/**
 * Get ten articles from DB and increases count of articles
 */
function getArticles() {
    
    loadBtn.textContent = 'Загрузка...';

    fetch(`/loadArticles?count=${articlesLoaded}`, {method: "GET"})
        .then(res => res.json())
        .then(articles => {
            if (articles.length == 0) {
                showMessage('Статей больше нет');
            } else {
                articlesLoaded += articles.length;
                createArticles(articles);
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
 * Create article's card
 * @param {Array} articles array with 10 articles
 */
function createArticles(articles) {
    
    for (let i = 0; i < articles.length; i++) {

        let
            title 	    = articles[i].title,
            url   	    = articles[i].img,
            desc  	    = articles[i].desc,
            created     = articles[i].date,
            author      = articles[i].author_name,
            category    = articles[i].category,
            category_no = articles[i].category_no,
            likes       = articles[i].likes;

        let
            article   = document.createElement(`div`),
            article_content = document.createElement('div'),
            article_title = document.createElement('a'),
            article_desc_a = document.createElement('a'),
            article_desc = document.createElement('p'),
            article_author = document.createElement('a'),
            article_category = document.createElement('a'),
            article_date = document.createElement('p'),
            article_button = document.createElement('button'),
            article_img_a = document.createElement('a'),
            article_img = document.createElement('img');

        article.classList.add('article'),
        article_content.classList.add('article__content'),
        article_title.classList.add('article__title'),
        article_desc.classList.add('article__desc'),
        article_author.classList.add('article__author-name'),
        article_category.classList.add('article-category'),
        article_date.classList.add('article__date'),
        article_button.classList.add('like-btn'),
        article_img.classList.add('article__img');

        article.appendChild(article_content);
        article_img_a.appendChild(article_img);
        article.appendChild(article_img_a);
        article_content.appendChild(article_title);
        article_desc_a.appendChild(article_desc);
        article_content.appendChild(article_desc_a);
        article_content.appendChild(article_author);
        article_content.appendChild(article_category);
        article_content.appendChild(article_date);
        article_content.appendChild(article_button);

        article_img_a.href = article_desc_a.href = article_title.href = '#HereWillBeLinkToArticleNum' + articles[i].id;
        article_img.src = url;
        article_title.textContent = title;
        article_desc.textContent = desc;
        article_author.href = '#HereWillBeLinkToAuthor';
        article_author.textContent = author;
        article_category.href = 'category/?id=' + category_no;
        article_category.textContent = category;
        article_date = created;

        article_button.innerHTML = `<?xml version="1.0" ?><svg height="24" version="1.1" width="24" xmlns="http://www.w3.org/2000/svg" xmlns:cc="http://creativecommons.org/ns#" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"><g transform="translate(0 -1028.4)"><path d="m7 1031.4c-1.5355 0-3.0784 0.5-4.25 1.7-2.3431 2.4-2.2788 6.1 0 8.5l9.25 9.8 9.25-9.8c2.279-2.4 2.343-6.1 0-8.5-2.343-2.3-6.157-2.3-8.5 0l-0.75 0.8-0.75-0.8c-1.172-1.2-2.7145-1.7-4.25-1.7z" fill="#c0392b"/></g></svg>
        <span>${likes}</span>`;
        article_button.addEventListener('click', sendLike);

        container.insertBefore(article, loadBtn);

    }

}

function showMessage(message) {
    el = document.createElement(`p`);
    el.classList.add("load-message");
    el.textContent = message;

    loadBtn.remove();
    container.appendChild(el);
}

function sendLike(e) {
    fetch(`/loadArticles?count=${articlesLoaded}`, {method: "GET"})
    .then(res => res.json())
    .then(articles => {
        if (articles.length == 0) {
            showMessage('Статей больше нет');
        } else {
            articlesLoaded += articles.length;
            createArticles(articles);
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