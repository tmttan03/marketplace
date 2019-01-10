/*function genericLoadDialog(form_selector, dialog_selector, matchString){
        $.ajax({
            url: $(form_selector).attr('action'),
            type: 'POST',
            data:  $(form_selector).serialize(),
            success: function(data, textStatus, jqXHR){
                if(data.match(matchString)){
                // We got errors in form
                    $(dialog_selector).html(data).modal('show');
                            return false;
                }
                        $(dialog_selector).modal('hide');
            },
        })
    }*/






