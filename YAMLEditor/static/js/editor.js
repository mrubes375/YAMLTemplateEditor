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


function ChangeTemplateValue(tag, new_context) {
    var message;
    $.ajax({
    url: 'http://localhost:8000/update/context/',
    type: 'POST', // This is the default though, you don't actually need to always mention it
    data: JSON.stringify({
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

$(document).ready(function (){
    $("button.edit").clickToggle(function() {
        var editables = $('[data]');
        $('a').not('.dropdown-toggle').prop('disabled', true);
        editables.attr('contentEditable', 'true');
        editables.click(function(event){
            var tag = $(event.target).attr('data');
            $(this).keyup(function(event){
                if (event.ctrlKey && event.which==83 ) {
                    var new_context = $(event.target).text();
                    ChangeTemplateValue(tag, new_context);
                };
            })
        });
        $(this).removeClass('btn-danger').addClass('btn-success');
        $(this).after('<h6 class="howtoSave" style="margin-top: 5px; margin-right: 10px; line-height: 1.4;">Press <kbd><kbd>ctrl</kbd> + <kbd>s</kbd></kbd> to save change</h6>');
    },
    function() {
        $("body *").removeAttr('contentEditable').removeClass('editable');
        $('a').not('.dropdown-toggle').prop('disabled', false);
        $(this).removeClass('btn-success').addClass('btn-danger');
        $('.howtoSave').remove();
    });

});
