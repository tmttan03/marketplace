/* Create Post */
$('#new_post_modal').on('show.bs.modal', function (e) {
   var url = $(this).data("url");
   $.ajax({
        url: url,
        method: "GET",
        success: function(response){
            $('#new-post').html(response);
        }
   })
});

$(document).on('submit', '#post-create-form', function (e){
    var url = $(this).attr("action");
    e.preventDefault();
     $.ajax({
        url: url,
        method: "POST",
        data:  $(this).serialize(),
        success: function(response){
            console.log(response);
            $('#new-post').html(response);
        }
   })
});


/* Update Post */
$("a[id='edit-btn']").click(function() {
  var link = $(this).attr('href');
/*Detail Modal*/
  $('#update_post_modal').on('show.bs.modal', function (e) {
    //var link = $("#detail-card").attr('href');
    console.log(link);
    $.ajax({
          url: link,
          method: "GET",
          success: function(response){
            //console.log(response);
            $('#update_post_modal').attr('data-url', link);
            $('#update-post').html(response);
          }
     })
  });
 });

$("a[id='edit-btn']").click(function() {
    var url = $(this).attr('href');
$(document).on('submit', '#UpdateForm', function (e){
    //var url = $(this).attr("action");
    e.preventDefault();
     $.ajax({
        url: url,
        method: "POST",
        data:  $(this).serialize(),
        success: function(response){
            $('#update-post').html(response);
        }
   })
});
});




$("a[id='detail-card']").click(function() {
  var link = $(this).attr('href');
/*Detail Modal*/
  $('#detailModal').on('show.bs.modal', function (e) {
    //var link = $("#detail-card").attr('href');
    console.log(link);
    $.ajax({
          url: link,
          method: "GET",
          success: function(response){
            //console.log(response);
            $('#detailModal').attr('data-url', link);
            $('#content-product').html(response);
          }
     })
  });
});






