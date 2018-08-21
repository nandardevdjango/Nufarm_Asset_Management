if (typeof NA$ == 'undefined') {
    window.NA$ = window.$;
}

NA$.Input = {
    SelectMultipleChoice: function (kwargs) {
        var container_input = kwargs.container_input,
            input_name = kwargs.input_name,
            input_elm = kwargs.input_elm,
            item_choice = 'item_choice';
        var search_item = '#search_item_' + input_name,
            dropdown_item = '#dropdown_item_' + input_name,
            item_choice_visible = item_choice + ':visible',
            fake_input = '#fake_input_' + input_name;
        
        (function (elm) {
            NA$(elm).addClass('which_used_this');
            NA$(container_input)[0].dataset.input = input_elm;
            NA$('<li id="no_result" style="display:none"><p>No results found</p></li>')
                .insertAfter(NA$(search_item).parent('li'));
            if (NA$(elm).val() != "") { 
                var value = NA$(elm).val().split(',');
                console.log(value)
                for (var i = 0; i < value.length; i++) { 
                    var item = NA$('li#item_choice[data-id="' + value[i] + '"]');
                    appendItem(value[i], item.text());
                    item[0].dataset.selected = true;
                }
            }
        })(input_elm);

        function refresh_value_elm (input_element) {
            var item_selected = NA$('ul.container-multiselect[data-input="' + input_element + '"]')
                .children('span.label.label-success.selected-item');
            var data_id = [];
            if (item_selected.length) {
                NA$.each(item_selected, function (key, value) {
                    data_id.push(value.dataset.id);
                });
            }
            NA$(input_element).val(
                String(data_id)
            );
        }

        function checkInView(elem) {
            var container = NA$(dropdown_item);
            var contHeight = container.height();
            
            var elemTop = NA$(elem).offset().top - container.offset().top;
            var elemBottom = elemTop + NA$(elem).height();
            
            var isTotal = (elemTop >= 0 && elemBottom <=contHeight);            
            return  isTotal;
        }

        function appendItem (id, text) { 
            var item_selected = '<span class="label label-success selected-item" data-id="' +
                id + '">' +
                '<span id="remove_item" class="close-item">x</span>' +
                text + '</span>';
            NA$(item_selected).insertBefore(NA$(fake_input));
        }

        function SelectItem (event) { 
            event.preventDefault();
            event.stopPropagation();
            event.stopImmediatePropagation();
            var item_added = [];
            NA$.each(NA$('input.which_used_this'),
                function (index, elm) {
                    var value = elm.value.split(',');
                    if (value.length) {
                        for (var i = 0; i < value.length; i++) { 
                            item_added.push(value[i]);
                        }
                    }
                }
            );
            if (item_added.indexOf(this.dataset.id) > -1) {
                return false;
            }
            appendItem(this.dataset.id, this.textContent);
            var item_selected = '<span class="label label-success selected-item" data-id="' +
                this.dataset.id + '">' +
                '<span id="remove_item" class="close-item">x</span>' +
                this.textContent + '</span>';
            NA$(item_selected).insertBefore(NA$(fake_input));
            NA$(fake_input).focus();
            NA$.each($('li#item_choice[data-id="' + this.dataset.id + '"]'),
                function (index, elm) {
                    elm.dataset.selected = true;
                }
            );

            refresh_value_elm(
                NA$(this).parents('.select-multiple').prev().data('input')
            );
            NA$(this).parents('.dropdown').removeClass('open');
            return false;
        }
        
        NA$(container_input).click(function (event) {
            event.preventDefault();
            NA$(search_item).val('');
            NA$(dropdown_item + ' li#' + item_choice).css('display', 'block');
            NA$('#no_result').css('display', 'none');

            NA$('.item-hover').removeClass('item-hover');
            var items = NA$(dropdown_item + ' li#' + item_choice + ':not([data-selected="true"])');
            if (NA$(this).next()[0].dataset.reversed == "true") { 
                items.last().addClass('item-hover');
            } else {
                items.first().addClass('item-hover');
            }
            setTimeout(function () {
                NA$(search_item).focus();
            }, 100);
        });
        
        NA$(search_item).on({
            click: function (event) {
                event.preventDefault();
                event.stopPropagation();
            },
            keyup: function (event) {
                if (event.keyCode != 40 && event.keyCode != 38 && event.keyCode != 13) {
                    event.preventDefault();
                    event.stopPropagation();
                    event.stopImmediatePropagation();
                    var q = this.value;
                    if (q.match('\\\\')) { 
                        q = '\\\\';
                    }
                    var pattern = new RegExp(q, 'i');

                    var item_match = NA$(dropdown_item + ' li#' + item_choice).filter(function (index) {
                        return NA$(this).text().match(pattern);
                    });
                    if (item_match.length) {
                        item_match.css('display', 'block');
                        NA$(dropdown_item + ' li#no_result').css('display', 'none');
                    } else {
                        NA$(dropdown_item + ' li#no_result').css('display', 'block');
                    }

                    NA$(dropdown_item + ' li#' + item_choice).filter(function (index) {
                        return !NA$(this).text().match(pattern);
                    }).css('display', 'none').removeClass('item-hover');

                    NA$(dropdown_item).children('li#' + item_choice_visible +
                        ':not([data-selected="true"])').first()
                        .addClass('item-hover').nextAll().removeClass('item-hover');
                    return false;
                }
            },
            keydown: function (event) {
                if (event.keyCode == 40 || event.keyCode == 38 || event.keyCode == 13) {
                    event.preventDefault();
                    event.stopPropagation();
                    event.stopImmediatePropagation();
                    var bottom_dropdown = NA$(dropdown_item).height();
                    if (event.keyCode == 40 || event.key == 'ArrowDown') {
                        var data_id = NA$(dropdown_item + ' .item-hover').data('id');
                        var next_item = NA$(dropdown_item).children('.item-hover')
                            .nextAll('li#' + item_choice_visible + ':not([data-selected="true"])')
                            .first();
                        if (next_item.length) {
                            next_item.addClass('item-hover');
                            if (!checkInView(next_item)) {
                                NA$(dropdown_item).animate({
                                    scrollTop: bottom_dropdown - next_item.height()
                                }, "fast");
                            }
                        } else {
                            NA$(dropdown_item + ' li#' + item_choice_visible +
                                ':not([data-selected="true"])')
                                .first().addClass('item-hover');
                            
                            NA$(dropdown_item).animate({ scrollTop: 0 }, "fast");
                        }
                        
                        NA$('li[data-id="' + data_id + '"]').removeClass('item-hover');
                    } else if (event.keyCode == 38 || event.key == 'ArrowUp') {
                        var data_id = NA$(dropdown_item + ' .item-hover').data('id');
                        var prev_item = NA$(dropdown_item + ' .item-hover')
                            .prevAll('li#' + item_choice_visible + ':not([data-selected="true"])')
                            .first();
                        if (prev_item.length) {
                            prev_item.addClass('item-hover');
                            if (prev_item.prev().length) {
                                if (!checkInView(prev_item.prev())) {
                                    NA$(dropdown_item).animate({
                                        scrollTop: prev_item.height()
                                    }, "fast");
                                }
                            } else {
                                NA$(dropdown_item).animate({
                                    scrollTop: 0
                                }, "fast");
                            }
                            
                        } else {
                            NA$(dropdown_item + ' li#' + item_choice_visible +
                                ':not([data-selected="true"])')
                                .last().addClass('item-hover');
                            
                            NA$(dropdown_item).animate({
                                scrollTop: bottom_dropdown
                            }, "fast");
                        }
                        
                        NA$('li[data-id="' + data_id + '"]').removeClass('item-hover');
                    }
                    else if (event.keyCode == 13) {
                        
                        if (NA$(dropdown_item).children('li.item-hover#' + item_choice_visible).length) {
                            NA$(dropdown_item + ' li.item-hover').click();
                        } else { 
                            return false;
                        }
                        
                        NA$(dropdown_item + ' li#' + item_choice).removeClass('item-hover')
                            .first().addClass('item-hover');
                        setTimeout(function () {
                            NA$(container_input).click();
                        }, 180);
                    }
                    return false;
                }
            }
        });

        NA$(document).on('click', dropdown_item + ' li#' + item_choice, SelectItem);

        NA$(document).on('mouseover', dropdown_item + ' li#' + item_choice, function (event) {
            if (event.currentTarget.dataset.selected == "true") { 
                return false;
            }
            var item = NA$(dropdown_item + ' li.item-hover');
            if (item.length) {
                item.removeClass('item-hover');
            }
            NA$(event.currentTarget).addClass('item-hover');
            return false;
        });

        NA$(document).on('mouseleave', dropdown_item + ' li#' + item_choice, function (event) {
            if (event.relatedTarget != null) {
                if (event.relatedTarget.tagName.toLocaleLowerCase() == 'p') {
                    if (event.currentTarget.dataset.selected == "true") { 
                        return false;
                    }
                    NA$(event.currentTarget).removeClass('item-hover');
                }
            }
            return false;
        });

        NA$(fake_input).keydown(function (event) {
            event.preventDefault();
            event.stopPropagation();
            if (event.keyCode == 13) {
                NA$(container_input).click();
            } else if (event.keyCode == 8) {
                NA$(this).prev().children('span#remove_item').click();
            }
        });

        NA$(document).on('click', 'span#remove_item', function (event) {
            event.preventDefault();
            event.stopPropagation();
            event.stopImmediatePropagation();
            var id = NA$(this).parent().data('id');
            
            NA$.each($('li#item_choice[data-id="' + id + '"]'),
                function (index, elm) {
                    elm.dataset.selected = false;
                }
            );
            var input_name = NA$(this).parents('.container-multiselect').data('input');
            NA$(this).parent().remove();
            refresh_value_elm(input_name);
            
            return false;
        });

        $('#entry_' + input_name).click(function () {
            BootstrapDialog.show({
                draggable: true,
                type: BootstrapDialog.TYPE_SUCCESS,
                size: BootstrapDialog.SIZE_SMALL,
                title: 'Entry Equipment',
                cssClass: 'dialog-entry-equipment',
                message: (function () {
                    var container_form = $('<div></div>');
                    NA$.ajax({
                        url: 'add_equipment/',
                        success: function (data) {
                            container_form.append($(data));
                        }
                    });
                    return container_form;
                })(),
                closable: false,
                animate: true,
                closeByBackdrop: false,
                closeByKeyboard: false,
                buttons: [{
                    label: 'Cancel',
                    cssClass: 'btn-default',
                    action: function (dialogRef) {
                        dialogRef.close();
                    }
                }, {
                    label: 'OK',
                    cssClass: 'btn-success',
                    action: function (dialogRef) {
                        var form = NA$('#entry_equipment_form')[0];
                        if (form.checkValidity()) {
                            NA$.ajax({
                                url: 'add_equipment/',
                                method: 'POST',
                                data: {
                                    name_app: NA$('#id_name_app').val().trim()
                                },
                                beforeSend: function (xhr) {
                                    xhr.setRequestHeader(
                                        'X-CSRFToken',
                                        form.children[0].value
                                    );
                                },
                                success: function (data) {
                                    
                                    NA$.ajax({
                                        url: 'equipment/list/',
                                        success: function (data) {
                                            var dropdowns = NA$('.container-multiselect').next();
                                            NA$.each(dropdowns, function (index, dropdown) {
                                                NA$(dropdown).children('li#item_choice').remove();
                                                NA$.each(data, function (index, obj) {
                                                    NA$(dropdown).append(
                                                        NA$('<li id="item_choice" data-id="' + obj.idapp +
                                                            '" data-selected="false" class="item-hover" style="display: block;"><p>' +
                                                            obj.name_app + '</p></li>')
                                                    );
                                                });
                                            });
                                        }
                                    });
                                    
                                    dialogRef.close();
                                }
                            });
                        } else {
                            NA$('input#submit_entry_equipment').click();
                            return false;
                        }
                    }
                }]
            });
        });
    }
};
NA$.Element = {};
NA$.Element.Position = {
    GetPositionToSpecificParent: function (elm, specific_parent, top = NA$(elm).height()) {
        top += NA$(elm).position().top - NA$(elm).parent().position().top;
        if (NA$(elm)[0] == NA$(specific_parent)[0]) { 
            return top;
        }
        return this.GetPositionToSpecificParent(NA$(elm).parent(), specific_parent, top);
    }
};

NA$.Element.Dropdown = {
    SetAutoDropUp: function (kwargs) {
        this.container_dropdown = kwargs.container_dropdown;
        this.crazy_ancestor = kwargs.crazy_ancestor;
    }
};

NA$(document).on("shown.bs.dropdown", "#dropdown_select_multiple", function (event) {
    // calculate the required sizes, spaces

    event.preventDefault();
    container_dropdown = NA$(this).parents(NA$.Element.Dropdown.container_dropdown);
    if (container_dropdown.length) {
        var current_position = NA$.Element.Position.GetPositionToSpecificParent(
            container_dropdown,
            NA$.Element.Dropdown.crazy_ancestor
        );
        
        var parent = NA$(this).parents(NA$.Element.Dropdown.crazy_ancestor);
        var current_position = (parent[0].scrollHeight - parent.scrollTop()) - current_position;
        var $ul = NA$(this).children(".dropdown-menu");
        var $button = NA$(this).children(".dropdown-toggle");
        var ulOffset = $ul.offset();
        // how much space would be left on the top if the dropdown opened that direction
        var spaceUp = (ulOffset.top - $button.height() - $ul.height()) - NA$(window).scrollTop();
        // how much space is left at the bottom
        var spaceDown = NA$(window).scrollTop() + NA$(window).height() - (ulOffset.top + $ul.height());
        // switch to dropup only if there is no space at the bottom AND there is space at the top, or there isn't either but it would be still better fit
        if (spaceDown < 0 && (spaceUp >= 0 || spaceUp > spaceDown) || current_position < $ul[0].scrollHeight) {
            NA$(this).addClass("dropup");
            if ($ul[0].dataset.reversed != "true") {
                $ul.append($ul.children("li").get().reverse());
            }
            
            if (NA$(this).hasClass('dropup')) { 
                $ul[0].dataset.reversed = true;
                $ul.children().last().children('input').css({
                    'borderTop': '',
                    'borderBottom': '0'
                });
            }
        } else {
            if (typeof $ul[0].dataset.reversed != undefined && $ul[0].dataset.reversed == "true") {
                $ul[0].dataset.reversed = false;
                $ul.append($ul.children("li").get().reverse());
             }
            
        }
    }
    
}).on("hidden.bs.dropdown", ".dropdown", function() {
    // always reset after close
    NA$(this).removeClass("dropup");
});