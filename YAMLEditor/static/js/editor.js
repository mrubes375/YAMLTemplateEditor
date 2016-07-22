var containsUpdate = window.location.pathname.indexOf('update')!=-1;
// var top_path = path.substring(1, 7);
if (!containsUpdate) {
    $("body *").mousedown(function() {
        $(this).attr('contentEditable', 'true');
})};
