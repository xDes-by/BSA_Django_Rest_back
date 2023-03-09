$(window).on('beforeunload', function () {
    $(window).scrollTop(0);
});

$(document).ready(function () {
    let zSpacing = -1000,
        lastPos = zSpacing / 5,
        $frames = $('.frame'),
        zVals = [];

    $(window).scroll(function () {
        let top = $(document).scrollTop(),
            delta = lastPos - top;

        lastPos = top;

        $frames.each(function (i) {
            zVals.push((i * zSpacing) + zSpacing);
            zVals[i] += delta * -5.5;
            let transform = `translateZ(${zVals[i]}px)`,
                opacity = zVals[i] < Math.abs(zSpacing) / 1.8 ? 1 : 0;
            $(this).attr('style', `transform: ${transform}; opacity: ${opacity}`);
        });
    });
    $(window).scrollTop(1);
});

$('.soundbutton').click(function () {
    $(this).toggleClass('paused');
    if ($('.audio').prop('paused')) {
        $('.audio').trigger('play');
    } else {
        $('.audio').trigger('pause');
    }
});

$(window).focus(function () {
    if ($('.soundbutton').hasClass('paused')) {
        $('.audio').trigger('pause');
    } else {
        $('.audio').trigger('play');
    }
});

$(window).blur(function () {
    $('.audio').trigger('pause');
});