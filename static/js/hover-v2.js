/*! Copyright 2015, Rob Warner (https://monsterprojects.org)
 * Version: 2.1.2
 */
if(typeof jQuery === 'undefined') {
  throw new Error('jQuery is required for this addons')
}
(function($){
    'use strict';
    $.fn.hoverTooltip = function(useroptions){
        // Define options and extend with user
        var options = {
            wrapperSelector: 'body',
            dataSelector: 'data-tooltip',
            offsetYBelow: 25,
            offsetYAbove: 8,
            offsetX: 5,
            pinnable: false
        };
        $.extend(options, useroptions);

        // Tooltip ID/Selector
        var tooltipID = 'hoverTooltip';
        var tooltipSelector = '#'+tooltipID;

        var $Items = this;

        // Append the tooltip element
        var appendTooltip = function() {
            if(!$(tooltipSelector).length)
                $('body').append('<div id="'+tooltipID+'" style="display: none; position: absolute; top: 0; left: 0; font-size: 0.9em; z-index: 9999999; background-color:rgba(10,10,10,0.9); color: #FFF; text-align: center; padding: 8px; border-radius: 2px; max-width: 400px;"></div>');
        };

        // Get tooltip measurements
        var getTooltipMes = function() {
            if(!$(tooltipSelector).length)
                return 0;

            var Measurements = {};

            if($(tooltipSelector).is(':visible')) {
                // Take its measurement
                Measurements.outerWidth = $(tooltipSelector).outerWidth();
                Measurements.outerHeight = $(tooltipSelector).outerHeight();
            } else {
                // Make a clone
                var $Clone = $(tooltipSelector).clone().css('position', 'absolute').css('top', '-800').css('display', 'block').appendTo('body');

                // Take its measurement
                Measurements.outerWidth = $Clone.outerWidth();
                Measurements.outerHeight = $Clone.outerHeight();

                // Remove the clone
                $Clone.remove();
            }

            // Return measurement
            return Measurements;
        };

        // Do tooltips
        this.runTooltips = function() {
            appendTooltip();

            var $Tooltip = $(tooltipSelector);
            var $Wrapper = $(options.wrapperSelector);

            // Loop items
            $Items.each(function() {
                var $Item = $(this);

                // Does item data exist
                if(typeof $Item.attr(options.dataSelector) == 'undefined' || $Item.attr(options.dataSelector).length < 1) {
                    return true;
                }

                // Add cursor style
                if($Item.prop('tagName') !== 'A' && $Item.prop('tagName') !== 'BUTTON' && $Item.prop('tagName') !== 'INPUT') {
                    $Item.css('cursor', 'help');
                }

                // Pin tooltip
                if(options.pinnable === true) {
                    $Item.unbind('click').on('click', function(e) {
                        if(typeof $Tooltip.attr('data-tooltip-pinned') != 'undefined' && $Tooltip.attr('data-tooltip-pinned') == 'pinned') {
                            $Tooltip.removeAttr('data-tooltip-pinned');
                        } else if(typeof $Tooltip.attr('data-tooltip-pinned') == 'undefined') {
                            $Tooltip.attr('data-tooltip-pinned', 'pinned');
                        }
                        e.stopPropagation();
                    });
                }

                // Don't close tooptip on click
                if(options.pinnable === true) {
                    $Tooltip.unbind('click').on('click', function(e){
                        e.stopPropagation();
                    });
                }

                // Close tooltip when clicked off
                if(options.pinnable === true) {
                    $('body').unbind('click').on('click', function(e){
                        if(typeof $Tooltip.attr('data-tooltip-pinned') != 'undefined' && $Tooltip.attr('data-tooltip-pinned') == 'pinned') {
                            $Tooltip.removeAttr('data-tooltip-pinned');
                            $Tooltip.finish();
                            $Tooltip.hide(0);
                            $Tooltip.html('');
                            $Tooltip.css({ left: 0 });
                        }
                    });
                }

                // On hover
                $Item.unbind('mousemove').on('mousemove', function(mouse) {
                    // Pinned?
                    if(options.pinnable === true && typeof $Tooltip.attr('data-tooltip-pinned') != 'undefined' && $Tooltip.attr('data-tooltip-pinned') == 'pinned') {
                        return false;
                    }

                    // Set content
                    $Tooltip.html($Item.attr(options.dataSelector));

                    // Get measurements
                    var tooltipMeasure = getTooltipMes();

                    // Y position
                    var NewY = (mouse.pageY + options.offsetYBelow);

                    // Would box go outside of content
                    if((NewY + tooltipMeasure.outerHeight) > ($Wrapper.offset().top + $Wrapper.height())) {
                        NewY = ((mouse.pageY - tooltipMeasure.outerHeight) - options.offsetYAbove);
                    }

                    // X position
                    var NewX = ((mouse.pageX - Math.ceil(tooltipMeasure.outerWidth / 2)) + options.offsetX);

                    // Would box go outside of content - Right
                    if((NewX + tooltipMeasure.outerWidth) > ($Wrapper.offset().left + $Wrapper.width())) {
                        NewX = (($Wrapper.offset().left + $Wrapper.width()) - tooltipMeasure.outerWidth);
                    }

                    // Would box go outside of content - Left
                    if(NewX < $Wrapper.offset().left) {
                        NewX = $Wrapper.offset().left;
                    }

                    // Show/Move box
                    if(!$Tooltip.is(":visible")) {
                        $Tooltip.finish();
                        $Tooltip.css({ top: NewY, left: NewX, opacity: 0 });
                        $Tooltip.show(0).animate({opacity: 1}, 400);
                    } else {
                        $Tooltip.css({ top: NewY, left: NewX });
                    }
                });

                // On leave
                $Item.unbind('mouseleave').on('mouseleave', function() {
                    // Pinned?
                    if(options.pinnable === true && typeof $Tooltip.attr('data-tooltip-pinned') != 'undefined' && $Tooltip.attr('data-tooltip-pinned') == 'pinned') {
                        return false;
                    }

                    // Finish animations and hide
                    $Tooltip.finish();
                    $Tooltip.hide(0);
                    $Tooltip.html('');
                    $Tooltip.css({ left: 0 });
                });
            });

        };

        // Trigger tooltips
        $(document).ready(function(e){
            $Items.runTooltips();
        });

        return this;
    };
})(jQuery);
