function init() {
    $('.item p').css('fontSize', $('.item').height() / 10);
    if ($('.item').length > 0) $('.title').css('height', $('.item').width() / 2);
    else $('.title').css('height', $(window).height() / 5);
    $('.title img').css('marginLeft', ($('.title').width() - $('.title img').width()) / 2);
    $('.title b').css('marginLeft', ($('.title').width() - $('.title b').width()) / 2);

    if ($('.my-video').length <= 0) {
        $('.area_items').each(function () {
            $('.item').css('marginLeft', 5); //init marginLeft
            var item_width = $('.item').width() + parseInt($('.item').css('marginLeft'));
            var lines = Math.ceil($(this).children().length / parseInt($(window).width() / item_width));
            $(this).css('height', ($('.item').height() + parseInt($('.item').css('marginTop'))) * lines);

            var new_marLeft = $('.area_items').width() - ($('.item').width() * parseInt($(window).width() / item_width));
            new_marLeft = new_marLeft / (parseInt($(window).width() / item_width) + 1);
            if (new_marLeft > 5) $('.item').css('marginLeft', new_marLeft);
        });
    } else {
        if ($(window).height() > $(window).width()) {
            //竖屏
            $('.title b').show();
            $('.my-video').css('width', $(window).width());
            $('.my-video').css('height', parseInt($(window).width() / 1.7));
            $('.my-video').css('marginLeft', 0);
            $('.my-video').css('marginTop', 20);
        } else {
            //横屏
            $('.title b').hide();
            $('.my-video').css('height', parseInt($(window).height() / 1.5));
            $('.my-video').css('width', parseInt($(window).height() * 1.7));
            $('.my-video').css('marginLeft', ($(window).width() - $('.my-video').width()) / 2);
            $('.my-video').css('marginTop', 0);
        }
    }
}

$(document).ready(function () {
    if ($('.my-video').length <= 0) {
        $('.area_title').click(function () {
            $(this).nextAll('.area_items').slideToggle(100);
        });
        $(function () {
            $("img.lazy").lazyload({threshold: 200});
        });
    }

    init();

    if ($('.my-video').length > 0) {
        var player = videojs('my-video');
        player.on('fullscreenchange', function () {
            init();
        });
    }
})
;

$(window).resize(function () {
    init()
});