(function ($) {
  $.fn.fieldSelect = function(settings) {
    var $settings = {
        field_name: 'Object',
        max_levels: 3,
        add_parents: true
    };
    if (settings) {
        $.extend($settings, settings);
    }

    function setup_cache(select) {
        var options = {}
            cache = [];

        select.find('option').each(function (idx, el) {
            el = $(el);
            options[el.attr('value')] = {
                value: el.attr('value'),
                verbose_label: el.text(),
                label: el.data('label'),
                parent: el.data('parent'),
                title: el.attr('title'),
                children: []
            }
        });
        $.each(options, function (val, data) {
            if (data.parent && options[data.parent]) {
                options[data.parent].children.push(data);
            } else {
                cache.push(data);
            }
        });
        return {root: cache, all: options};
    }
    function is_choosen(option, choosen_select) {
        return choosen_select.find('option[value='+option.value+']').length > 0;
    }
    function is_available(option, choosen_select) {
        var available = choosen_select.find('option[value='+option.value+']').length==0;
        $.each(option.children, function(idx, option) {
            if (is_available(option, choosen_select)) {
                available = true;
            }
        });
        return available;
    }
    function update_select(choosen_select, select, options, keep, verbose_label) {
        var currently_selected = select.find('option:selected').val();
        if (!keep) select.children().remove();
        $.each(options, function (idx, option) {
            if (is_available(option, choosen_select)
                && (!is_choosen(option, choosen_select) || choosen_select != select)) {
                var opt = $('<option />')
                        //.attr('title', option.title)
                        .val(option.value)
                        .text(verbose_label ? option.verbose_label : option.label);
                if (option.value == currently_selected) {
                    opt.attr('selected', 'selected');
                }
                select.append(opt);
            }
        })
        return select;
    }

    return this.each(function() {
        var choosen_select = $(this).attr('size', 15),
            container = $('<div/>', {'class': "field-selector-available"}).insertBefore(choosen_select),
            current_level,
            level_count, levels =[],
            cache = setup_cache(choosen_select);

        choosen_select.find('option:not(:selected)').remove();

        function traverse(options, level) {
            var max = level;
            $.each(options, function (idx, option) {
                if (option.children) {
                    max = Math.max(max, traverse(option.children, level+1));
                }
            })
            return max;
        }
        level_count = Math.min($settings.max_levels, traverse(cache.root, 0));
        current_level = level_count;

        while (current_level) {
            var new_select = $('<select/>', {'size': 15}).addClass('filtered').data('level', current_level);
            if (current_level == level_count) {
                new_select.attr('multiple', 'multiple');
            }
            container.prepend(new_select)
            levels.push(new_select);
            if (current_level < level_count) {
                (function (select, next_level) {
                    select.change(function() {
                        var level_to_clean = next_level + 1,
                            data = cache.all[select.find(':selected').val()];
                        if (data) {
                            update_select(choosen_select, levels[next_level], data.children);
                            while (level_to_clean < level_count) {
                                update_select(choosen_select, levels[level_to_clean++], []);
                            }
                        }
                    });
                })(new_select, current_level);
            }
            (function (select, current_level) {
                select.dblclick(function(e) {
                    if ($settings.add_parents) {
                        var level_to_add = current_level - 1;
                        while (level_to_add>=0) {
                            levels[level_to_add--].find(':selected').each(function() {
                                var el = $(this),
                                    data = cache.all[el.val()];
                                if (data) {
                                    update_select(choosen_select, choosen_select, [data], true, true);
                                }
                                if (!is_available(data, choosen_select)) {
                                    el.remove()
                                }
                            });
                        }
                    } else {
                        var el = $(this),
                            data = cache.all[el.val()];
                        if (data) {
                            update_select(choosen_select, choosen_select, [data], true, true);
                        }
                        if (!is_available(data, choosen_select)) {
                            el.remove()
                        }
                    }
                })
            })(new_select, current_level);

            current_level --;
        }
        levels.reverse();
        update_select(choosen_select, levels[0], cache.root);

        function remove_from_choosen() {
            choosen_select.find('option:selected').remove();
            var current_level = 0, data;
            while (current_level < level_count - 1) {
                data = cache.all[levels[current_level].find(':selected').val()];
                if (data) {
                    update_select(choosen_select, levels[current_level+1], data.children);
                }
                current_level ++;
            }
        }
        function add_to_choosen() {
            container.find('option:selected').each(function() {
                var el = $(this),
                    data = cache.all[el.val()];
                if (data) {
                    update_select(choosen_select, choosen_select, [data], true, true);
                }
            });
            container.find('option:selected').each(function() {
                var el = $(this),
                    data = cache.all[el.val()];
                if (!is_available(data, choosen_select)) {
                    el.remove();
                }
            });
        }

        choosen_select.wrap('<div class="field-selector-choosen" />').parent()
            .prepend(
                $('<p/>')
                    .text(gettext('Select your choice(s) and click '))
                    .append($('<img/>', {src: $settings.admin_media+'img/admin/selector-add.gif', alt: 'Add'}))
            )
            .prepend('<h2>Chosen '+$settings.field_name+'</h2>');
        container.prepend('<p> - no search -</p>');
        container.prepend('<h2>Available '+$settings.field_name+'</h2>');
        $('<ul>', {'class': "selector-chooser field-chooser"})
            .append($('<li/>').append($('<a/>', {'class':"selector-add"}).text('Add').click(add_to_choosen)))
            .append($('<li/>').append($('<a/>', {'class':"selector-remove"}).text('Remove').click(remove_from_choosen)))
            .insertAfter(container);
        choosen_select.find('option').removeAttr('selected');
        choosen_select.dblclick(remove_from_choosen);
        choosen_select.parents('form').submit(function() {
            choosen_select.find('option').attr('selected', 'selected');
        });
    });
  }
})($);
