jQuery.fn.clickToggle = function(a,b) {
  function cb(){ [b,a][this._tog^=1].call(this); }
  return this.on("click", cb);
};

String.prototype.format = function () {
  var i = 0, args = arguments;
  return this.replace(/{}/g, function () {
    return typeof args[i] != 'undefined' ? args[i++] : '';
  });
};

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

$.fn.editable.defaults.mode = 'inline';


function ChangeTemplateValue(tag, new_context) {
    var message;
    $.ajax({
    url: 'http://localhost:8000/update/context/',
    type: 'POST',
    data: JSON.stringify({
        CSRF: getCookie('csrftoken'),
        tag: tag,
        new_context: new_context,
    }),
    contentType: "application/json; charset=utf-8",
    success: function(data) {
        message = alert('{} translation has been updated'.format(tag));
    },
    failure: function(data) {
        message = alert('File could not be updated right now.');
    },
    });
    return message;
};

var editables = $('[data]');

$(document).ready(function (){
    $('[data]').css('color', 'white');
    $("button.edit").clickToggle(function() {
        editables.editable();
        editables.on('save', function(e, editable){
            var new_context = editable.newValue;
            var tag = $(this).attr('data');
            ChangeTemplateValue(tag, new_context);
        })
        $(this).removeClass('btn-danger').addClass('btn-success');

    },
    function() {
        $("body *").removeAttr('contentEditable').removeClass('editable');
        $(this).removeClass('btn-success').addClass('btn-danger');
        $('.howtoSave').remove();
        editables.editable('destroy');
    });

});
