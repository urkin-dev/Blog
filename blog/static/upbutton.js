let arrow = document.querySelector('.updown');

window.onload = function (e) {
    let pageY = window.pageYOffset || document.documentElement.scrollTop;
    let innerHeight = document.documentElement.clientHeight;

    checkScroll(pageY, innerHeight);
}

window.onscroll = function(e) {
    let pageY = window.pageYOffset || document.documentElement.scrollTop;
    let innerHeight = document.documentElement.clientHeight;

    checkScroll(pageY, innerHeight);
}

arrow.onclick = function (e) {
    let pageY = window.pageYOffset || document.documentElement.scrollTop;

    if (arrow.classList.contains('up')) {
        pageYLabel = pageY;
        window.scrollTo(0, 0);
        this.classList.remove('up');
    }
}

function checkScroll(pageY, innerHeight) {
    if (arrow.classList.contains('up')) {
        if (pageY < innerHeight) {
            arrow.classList.remove('up');
        }
    } else {
        if (pageY > innerHeight) {
            arrow.classList.add('up');
        }
    }
}