
// Forum replies
function copy_paste_custom(post_id) {   
    var post_div = $(".forum-post#"+post_id);
    var nick = post_div.find(".forum-username").text();
    
    var txt = get_selection(); // quote selection
    if (txt == '') {
        // quote the complete post content
        // FIXME: We should get the markup here (Ajax view?)
        txt = post_div.find(".forum-post-body").text();
        txt = $.trim(txt);
    }
    txt = '[quote=' + nick + ']' + txt + '[/quote]\n';
    paste(txt);
    return false;
}

$(document).ready(function(){
    var $root = $('html, body');

    // Tooltips
    $('[data-tooltip][data-tooltip!=""]').hoverTooltip({wrapperSelector: 'body'});

    // Main nav bar - mobile menu button
    $("#main-nav-bar-button-collapse").sideNav();

    // Main nav bar - Dropdowns
    $("#nav-main .dropdown-button").dropdown({
        belowOrigin: true,
        hover: true,
    });

    // Main nav pushpin
    $('#nav-main').pushpin({ top: $('#nav-main').offset().top });

    // Main nav search
    $('#nav-main-bar-button-search').on('click', function(e){
        e.preventDefault();
        $('#nav-main-search').slideDown('slow');
        $('#nav-main-search').find('input').first().focus();
    });
    $('#main-nav-search-input').focusout(function(){
        if($('#nav-main-search').is(':visible'))
            $('#nav-main-search').slideUp('fast');
    });
    $('#nav-main-bar-button-search-close').on('click', function(e){
        e.preventDefault();
        $('#nav-main-search').slideUp('fast');
    });

    // Hash/Internal Links
    $('a[href*=#]:not([href=#])').on('click', function(e) {
        var findElem = $(this).attr('href');
        if($root.find(findElem).length) {
            e.preventDefault();
            if(window.history)
                history.replaceState({}, '', this.href);
            $root.animate({scrollTop: $(findElem).offset().top-60}, 1000);
        }
    });

    if(window.location.hash !== "") {
        var findElem = window.location.hash;
        if($('body').find(findElem).length) {
            $root.animate({scrollTop: $(findElem).offset().top-60}, 100);
        }
    }

    // Full Screen
    $('.fullscreen-widget').find('.btn-fullscreen').unbind('click').bind('click', function(e) {
        e.preventDefault();
        $(this).parent('.fullscreen-widget').first().addClass('fullscreen').find('.btn-close').unbind('click').bind('click', function(e) {
            e.preventDefault();
            $(this).parent('.fullscreen-widget').first().removeClass('fullscreen');
        });
    });

    // Comment Replies
    $('.comment-reply').click(function() {
        var wasVisible = $(this).siblings('.comment-reply-form').first().is(':visible');
        
        $('.comment-reply-form').hide();
        if(!wasVisible)
            $(this).siblings('.comment-reply-form').show();
    });

    // Forum Poll
    $('.forum-poll-auto .infldset').hide();
    $('.forum-poll-auto').click(function() {
        $('.poll .infldset').slideDown();
    });
       
    $('textarea:not(.markup)').addClass('materialize-textarea');

    $('.field-add-required').find('input, textarea').attr('required', 'required'); 

    $('select').material_select();
});