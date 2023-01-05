window.setupNavMenu = function(imageVerticalPadding) {
    var allImagesLoaded = false, marginUpdateNeeded = true;

    $('.sm').smartmenus();

    function setFloatingNavMargin()
    {
        var returnVal = false;
        if($(window).width() >= 768)
        {
            var navTopLevelItems = $('.sm').children();
            var navComputedHeight = parseInt($(navTopLevelItems[0]).css('height'));

            navTopLevelItems.each(function(thisIndex, thisElement) {
                console.log(thisElement);

                var thisElementHeight = parseInt($(thisElement).css('height'));

                console.log(thisElementHeight);

                if(thisElementHeight < navComputedHeight)
                {
                    navComputedHeight = thisElementHeight;
                }
            });

            var currentMarginStyle = $('style#dynamic-content-container-margin').text();
            var newMarginStyle = currentMarginStyle.replace(/margin-top: .*px/, 'margin-top: ' + (navComputedHeight + 8).toString() + 'px')
                .replace(/\sheight: .*px/, '\theight: ' + navComputedHeight.toString() + 'px')
                .replace(/margin: .*px/, 'margin: ' + (-navComputedHeight).toString() + 'px').replace(/max-height: .*px/, 'max-height: ' + (navComputedHeight - 2 * imageVerticalPadding - 5).toString() + 'px');
            $('style#dynamic-content-container-margin').text(newMarginStyle);

            /*
            $('.navbar-image').each(function() {
                $(this).attr('src', $(this).attr('load-src'));
            });
            */

            console.log('Margin set.');
            returnVal = true;
        }

        return returnVal;
    }

    function marginResizeHandler() {
        if(setFloatingNavMargin())
        {
            $(window).off('resize', marginResizeHandler);
        }
    }

    /*
    if(!setFloatingNavMargin())
    {
        console.log('Margin not initially set.');
        $(window).on('resize', marginResizeHandler);
    }
    */

    // marginUpdateNeeded = !setFloatingNavMargin();


    $('.sm').imagesLoaded().always(function() {
        console.log('All images loaded');
        allImagesLoaded = true;

        marginUpdateNeeded = !setFloatingNavMargin();

        if(marginUpdateNeeded)
        {
            $(window).on('resize', marginResizeHandler);
        }
    });


    $('.sm').on('mouseenter.smapi', function(event, item) {
        if($(window).width() >= 768 && event.namespace === 'smapi')
        {
            $(item).children('img.external-link-img').each(function() {
                $(this).attr('src', $(this).attr('data-src-prefix') + 'External-link-white.svg');
            });
        }
    }).on('mouseleave.smapi', function(event, item) {
        if(event.namespace === 'smapi')
        {
            $(item).children('img.external-link-img').each(function() {
                $(this).attr('src', $(this).attr('data-src-prefix') + 'External-link-black.svg');
            });
        }
    });
};