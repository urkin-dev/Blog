let
    filterPrev        = document.querySelector('.filters-wrapper .prev'),
    filterNext        = document.querySelector('.filters-wrapper .next'),
    filterSlider      = document.querySelector('.filters__inner'),
    filterLinks       = document.querySelectorAll('.link-container'),
    filterWidth       = document.querySelector('.filters').clientWidth,
    actualSliderWidth = 0,
    delta             = 0;

// Calculate real width slider with filters and margins
filterLinks.forEach(link => {
    actualSliderWidth += link.clientWidth;
    actualSliderWidth += 20;
});

actualSliderWidth -= 20;

filterSlider.style.width = actualSliderWidth + `px`; // Set container width = with of all filters

filterNext.onmousedown = function(e) {

    if (e.button == 2 || e.button == 3) {
        return false;
    }

    let timer = setInterval(() => {
        if ((delta + filterWidth) >= actualSliderWidth) {
            delta = actualSliderWidth - filterWidth;
            filterSlider.style.transform = `translateX(-${delta}px)`;
            this.classList.add('disabled');
            return false;
        } else {
            delta += 15;
        }
    
        filterPrev.classList.remove('disabled');
        filterSlider.style.transform = `translateX(-${delta}px)`;
    }, 30);

    this.onmouseup = () => { 
        clearInterval(timer);
        return false;
    }

}

filterPrev.onmousedown = function(e) {

    if (e.button == 2 || e.button == 3) {
        return false;
    }

    let timer = setInterval(() => {
        if ((delta) <= 0) {
            filterSlider.style.transform = `translateX(0px)`;
            this.classList.add('disabled');
            return false;
        } else {
            delta -= 15;
        }

        filterNext.classList.remove('disabled');
        filterSlider.style.transform = `translateX(-${delta}px)`;
    }, 30);

    this.onmouseup = () => { 
        clearInterval(timer);
        return false;
    }

}