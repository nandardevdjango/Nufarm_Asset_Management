if (typeof NA$ == 'undefined') {
    window.NA$ = window.$
}

NA$.Input = {
    SelectMultipleChoice: function (kwargs) {
        var container_input = kwargs.container_input,
            input_name = kwargs.input_name,
            input_elm = kwargs.input_elm,
            item_choice = 'item_choice';
        var search_item = '#search_item_' + input_name,
            dropdown_item = '#dropdown_item_' + input_name,
            item_choice_visible = item_choice + ':visible';
        
        function refresh_value_elm () {
            var item_selected = NA$(container_input)
                .children('span.label.label-success.selected-item');
            var data_id = []
            if (item_selected.length) {
                NA$.each(item_selected, function (key, value) {
                    data_id.push(value.dataset.id)
                });
            }
            NA$(input_elm).val(
                JSON.stringify(data_id)
            );
        }
        
        NA$(container_input).click(function (event) {
            event.preventDefault();
            NA$('.item-hover').removeClass('item-hover');
            NA$(dropdown_item + ' li#' + item_choice).first().addClass('item-hover');
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
                if (event.keyCode == 40 || event.key == 'ArrowDown') {
                    var data_id = NA$(dropdown_item + ' .item-hover').data('id');
                    var next_item = NA$(dropdown_item).children('.item-hover')
                        .nextAll('li#' + item_choice_visible).first();
                    if (next_item.length) {
                        next_item.addClass('item-hover');
                    } else {
                        NA$(dropdown_item + ' li#' + item_choice_visible)
                            .first().addClass('item-hover');
                    }
                    
                    NA$('li[data-id="' + data_id + '"]').removeClass('item-hover');
                } else if (event.keyCode == 38 || event.key == 'ArrowUp') {
                    var data_id = NA$(dropdown_item + ' .item-hover').data('id');
                    var prev_item = NA$(dropdown_item + ' .item-hover')
                        .prevAll('li#' + item_choice_visible).first();
                    if (prev_item.length) {
                        prev_item.addClass('item-hover');
                    } else {
                        NA$(dropdown_item + ' li#' + item_choice_visible)
                            .last().addClass('item-hover');
                    }
                    
                    NA$('li[data-id="' + data_id + '"]').removeClass('item-hover');
                } else {
                    var q = this.value;
                    var pattern = new RegExp(q, 'i')
                    NA$(dropdown_item + ' li#' + item_choice).filter(function (index) {
                        return NA$(this).text().match(pattern)
                    }).css('display', 'block');
                    NA$(dropdown_item + ' li#' + item_choice).filter(function (index) {
                        return !NA$(this).text().match(pattern)
                    }).css('display', 'none').removeClass('item-hover');
                    NA$(dropdown_item).children('li#' + item_choice_visible).first()
                        .addClass('item-hover').nextAll().removeClass('item-hover');
                }
            },
            keydown: function (event) {
                if (event.keyCode == 13) {
                    event.preventDefault();
                    event.stopPropagation();
                    NA$(dropdown_item + ' li.item-hover').click();
                    NA$(dropdown_item + ' li#' + item_choice).removeClass('item-hover')
                        .first().addClass('item-hover');
                }
            },
            blur: function () {
                this.value = '';
                NA$(dropdown_item + ' li#' + item_choice).css('display', 'block');
            }
        });

        NA$(document).on('click', dropdown_item + ' li#' + item_choice, function (event) {
            NA.NAEvent.preventDefault(event);
            var fake_input = NA$('#fake_input_' + input_name)
            var item_selected = '<span class="label label-success selected-item" data-id="'
                + NA$(this).data('id') + '">' +
                '<span id="remove_item" class="close-item">x</span>' +
                this.textContent + '</span>';
            NA$(item_selected).insertBefore(fake_input);
            fake_input.focus();
            this.dataset.selected = true;
            refresh_value_elm();
        });

        NA$(document).on('mouseover', dropdown_item + ' li#' + item_choice, function (event) {
            var item = NA$(dropdown_item + ' li.item-hover');
            if (item.length) {
                item.removeClass('item-hover');
            }
            NA$(event.currentTarget).addClass('item-hover');
        });

        NA$(document).on('mouseleave', dropdown_item + ' li#' + item_choice, function (event) {
            if (event.relatedTarget != null) {
                if (event.relatedTarget.tagName.toLocaleLowerCase() == 'p') {
                    NA$(event.currentTarget).removeClass('item-hover');
                }
            }
            return;
        });

        NA$('#fake_input_' + input_name).keydown(function (event) {
            event.preventDefault();
            event.stopPropagation();
            if (event.keyCode == 13) {
                NA$(container_input).click();
            } else if (event.keyCode == 8) {
                $(this).prev().remove();
            }
        });

        NA$(document).on('click', 'span#remove_item', function (event) {
            event.preventDefault();
            event.stopPropagation();
            NA$(this).parent().remove();
            refresh_value_elm();
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
                        success: function(data){
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
                        if (form.checkValidity()){
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
                                    )
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
                                    })
                                    
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
        })
    }
};

// $(document).on("shown.bs.dropdown", ".dropdown", function () {
//     // calculate the required sizes, spaces
//     var $ul = $(this).children(".dropdown-menu");
//     var $button = $(this).children(".dropdown-toggle");
//     var ulOffset = $ul.offset();
//     // how much space would be left on the top if the dropdown opened that direction
//     var spaceUp = (ulOffset.top - $button.height() - $ul.height()) - $(window).scrollTop();
//     // how much space is left at the bottom
//     var spaceDown = $(window).scrollTop() + $(window).height() - (ulOffset.top + $ul.height());
//     var inline_div = NA$(this).parents('.NA-Entry-inlinve-div').offset().top
//     var ul_height = Number($ul.css('height').replace('px', ''));
//     console.log(inline_div);
//     console.log(ul_height);
//     // switch to dropup only if there is no space at the bottom AND there is space at the top, or there isn't either but it would be still better fit
//     if (spaceDown < 0 && (spaceUp >= 0 || spaceUp > spaceDown) || ul_height > inline_div) {
//         $(this).addClass("dropup");
//     }
// }).on("hidden.bs.dropdown", ".dropdown", function() {
//     // always reset after close
//     $(this).removeClass("dropup");
// });