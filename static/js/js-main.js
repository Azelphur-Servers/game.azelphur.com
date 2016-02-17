
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
        constrain_width: false,
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

    // Modal
    $('.modal-trigger').leanModal();

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
       
    // Add material class to textareas
    $('textarea:not(.markup)').addClass('materialize-textarea');

    // Add 'requried' attribtue to form elements
    $('.field-add-required').find('input, textarea').attr('required', 'required'); 

    // Init material select's
    $('select').material_select();


    // Server Updater
    var serverUpdateInterval = 15000;
    var serverUpdateURL = '/game_info/server/';

    var serverUpdateTimer = 0;
    var serverUpdateLast = 0;

    // Visibility
    if(document.addEventListener)
        document.addEventListener("visibilitychange", visibilityChanged);

    function visibilityChanged() {
        clearTimeout(serverUpdateTimer);
        if(!document.hidden) {
            serverUpdateTimer = setInterval(function(){UpdateServerBar();}, serverUpdateInterval);
            
            if(serverUpdateLast > 0 && (Math.floor(Date.now() / 1000) - serverUpdateLast) >= serverUpdateInterval)
                UpdateServerBar();
        }
    }

    // Server block update function
    function UpdateServerBar() {
        var $ServerElem = $('#content-side .side-server-list');
        if(!$ServerElem.length)
            return false;

        var shouldUpdateTooltips = false;
        serverUpdateLast = Math.floor(Date.now() / 1000);

        // Get JSON data and loop over it
        $.getJSON(serverUpdateURL, function(data) {
            $.each(data, function() {
                if(!$ServerElem.find('[data-serverid="'+this.id+'"]').length)
                    return;

                var $ServerBlock = $ServerElem.find('[data-serverid="'+this.id+'"]').first();

                // Online/Offline Status
                if($ServerBlock.find('.server-status').length) {
                    var $InfoElm = $ServerBlock.find('.server-status').first();
                    if(this.up == true && $InfoElm.hasClass('offline')) {
                        $InfoElm.removeClass('offline').addClass('online').text('Online');
                    } else if(this.up == false && $InfoElm.hasClass('online')) {
                        $InfoElm.removeClass('online').addClass('offline').text('Offline');
                    }
                    $InfoElm = null;
                }
                // Title
                if($ServerBlock.find('.server-info-name').length) {
                    var $InfoElm = $ServerBlock.find('.server-info-name').first();
                    if(this.up == true && !$InfoElm.find('a').length) {
                        $InfoElm.html($('<a>').attr('href', 'steam://connect/'+this.host+(this.port == 27015?'':':'+this.port)).attr('data-tooltip', 'Connect to this server').text(this.title));
                        shouldUpdateTooltips = true;
                    } else if(this.up == true && $InfoElm.find('a').first().text() != this.title) {
                        $InfoElm.find('a').first().text(this.title);
                    } else if(this.up == false && $InfoElm.find('a').length) {
                        $InfoElm.text(this.title);
                    } else if(this.up == false && $InfoElm.text() != this.title) {
                        $InfoElm.text(this.title);
                    }
                    $InfoElm = null;
                }
                // Map
                if($ServerBlock.find('.server-info-map').length) {
                    var $InfoElm = $ServerBlock.find('.server-info-map').first();
                    if(this.info === null || this.info.map === null) {
                        if($InfoElm.text() != 'Unknown')
                            $InfoElm.text('Unknown');
                    } else {
                        if(this.up == true && $InfoElm.text() != this.info.map) {
                             $InfoElm.text(this.info.map);
                         } else if(this.up == false && $InfoElm.text() != 'Unknown') {
                             $InfoElm.text('Unknown');
                         }
                    }
                    $InfoElm = null;
                }
                // Players
                if($ServerBlock.find('.server-info-players').length) {
                    var $InfoElm = $ServerBlock.find('.server-info-players').first();
                    if(this.info === null || this.info.player_count === null || this.info.max_players === null) {
                        if($InfoElm.text() != '0 / 0')
                            $InfoElm.text('0 / 0');
                    } else {
                        if(this.up == true) {
                             $InfoElm.text(this.info.player_count+' '+((this.info.bot_count !== null && this.info.bot_count === null > 0)?'('+this.info.bot_count+') ':'')+'/ '+this.info.max_players);
                         } else if(this.up == false && $InfoElm.text() != '0 / 0') {
                             $InfoElm.text('0 / 0');
                         }
                    }
                    $InfoElm = null;
                }
            });

            // Have links with tooltips been changed?
            if(shouldUpdateTooltips) {
                $('[data-tooltip][data-tooltip!=""]').hoverTooltip({wrapperSelector: 'body'});
            }
        });
    }

    // Init 
    serverUpdateTimer = setInterval(function(){UpdateServerBar();}, serverUpdateInterval);
});