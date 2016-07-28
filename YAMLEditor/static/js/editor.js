jQuery.fn.clickToggle = function(a,b) {
  function cb(){ [b,a][this._tog^=1].call(this); }
  return this.on("click", cb);
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
        message = alert('sent');
    },
    failure: function(data) {
        message = alert('File could not be updated right now.');
    },
    });
    return message;
};

$(document).ready(function (){
    $("button.edit").clickToggle(function() {
        // $("body *").not("script").attr('contentEditable', 'true').addClass('editable');
        var editables = $('[data]');
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
    },
    function() {
        $("body *").removeAttr('contentEditable').removeClass('editable');
        $(this).removeClass('btn-success').addClass('btn-danger');
    });

});
