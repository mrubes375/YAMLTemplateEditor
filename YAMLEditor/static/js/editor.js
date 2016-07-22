var containsUpdate = window.location.pathname.indexOf('update')!=-1;
// var top_path = path.substring(1, 7);
if (containsUpdate) {
    $(".edit").toggle(function() {
        $("body *").attr('contentEditable', 'true');
        $(this).removeClass('btn-danger');
        $(this).addClass('btn-success');
        console.log(this);
    }, function() {
        $("body *").removeAttr('contentEditable');
        $(this).removeClass('btn-success');
        $(this).addClass('btn-danger');
        console.log(this);
    });
}

// console.log($("body *").attr('contentEditable'));
// if (!containsUpdate) {
//     $("body *").mousedown(function() {
//         $(this).attr('contentEditable', 'true');
// })};
