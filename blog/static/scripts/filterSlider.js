let
    filterPrev        = document.querySelector('.filters-wrapper .prev'),
    filterNext        = document.querySelector('.filters-wrapper .next'),
    filterSlider      = document.querySelector('.filters__inner'),
    filterLinks       = document.querySelectorAll('.link-container'),
    filterWidth       = document.querySelector('.filters').clientWidth,
    actualSliderWidth = 0,
    delta             = 0,
    pressHoldDuration,
    timerID;

// Calculate real width slider with filters and margins
filterLinks.forEach(link => {
    actualSliderWidth += link.clientWidth;
    actualSliderWidth += 20;
});

actualSliderWidth -= 20;

filterSlider.style.width = actualSliderWidth + `px`; // Set container width = with of all filters

filterNext.addEventListener("mousedown", pressDown, false);
filterNext.addEventListener("mouseup", notPressDown, false);
filterNext.addEventListener("mouseleave", notPressDown, false);
filterPrev.addEventListener("mousedown", pressDown, false);
filterPrev.addEventListener("mouseup", notPressDown, false);
filterPrev.addEventListener("mouseleave", notPressDown, false);

/**
 * Starts requestAnimationFrame depends on the button class(next or prev)
 * @param {Object} e Event object
 */
function pressDown(e) {
    if (e.button == 2 || e.button == 3) {
        e.preventDefault();
    }

    if (this.classList.contains('next')) {
        
        pressHoldDuration = actualSliderWidth - filterWidth;
        requestAnimationFrame(moveSliderRight);

    } else if (this.classList.contains('prev')) {
    
        pressHoldDuration = 0;
        requestAnimationFrame(moveSliderLeft);

    }

    e.preventDefault();
}

/**
 * Clear animationFrame and change button class on disable if delta has reached the limit
 * @param {Object} e Event object
 */
function notPressDown(e) {
    if (delta + filterWidth == actualSliderWidth) {
        filterNext.classList.add('disabled');
        filterPrev.classList.remove('disabled');
    } else if (delta == 0) {
        filterPrev.classList.add('disabled');
        filterNext.classList.remove('disabled');
    } else {
        filterPrev.classList.remove('disabled');
        filterNext.classList.remove('disabled');
    }

    cancelAnimationFrame(timerID);

    e.preventDefault();
}

/**
 * Moves slider to right until mouse button will up
 */
function moveSliderRight() {
    if (delta < pressHoldDuration) {
        timerID = requestAnimationFrame(moveSliderRight);
        delta+=7;
    } else {
        delta = pressHoldDuration;
    }

    filterSlider.style.transform = `translateX(-${delta}px)`;

}

/**
 * Moves slider to left until mouse button will up
 */
function moveSliderLeft() {
    if (delta > pressHoldDuration) {
        timerID = requestAnimationFrame(moveSliderLeft);
        delta-=7;
    } else {
        delta = pressHoldDuration;
    }

    filterSlider.style.transform = `translateX(-${delta}px)`;

}