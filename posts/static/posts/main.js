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

$('#new_post_modal').on('hide.bs.modal', function (e) {
    location.reload();
})

/* Update Post */
$("a[id='edit-btn']").click(function() {
  var link = $(this).attr('href');
  $('#update_post_modal').on('show.bs.modal', function (e) {
    //var link = $("#detail-card").attr('href');
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
            console.log(response)
            $('#update-post').html(response);
        }
   })
});
});

$('#update_post_modal').on('hide.bs.modal', function (e) {
    location.reload();
});

/*Detail Modal*/
$("a[id='detail-card']").click(function() {
  var link = $(this).attr('href');
  $('#detailModal').on('show.bs.modal', function (e) {
    console.log(link);
    $.ajax({
          url: link,
          method: "GET",
          success: function(response){
            console.log(response);
            $('#detailModal').attr('data-url', link);
            $('#content-product').html(response);
          }
     })
  });
});


/*Delete Modal*/
$("a[id='delete-btn']").click(function() {
  var link = $(this).attr('href');
  $('#deleteModal').on('show.bs.modal', function (e) {
    //var link = $("#detail-card").attr('href');
    //console.log(link);
    console.log(link);
    $.ajax({
          url: link,
          method: "GET",
          success: function(response){
            //console.log(response);
            $('#deleteModal').attr('data-url', link);
            $('#warning-body').html(response);
          }
     })
  });
});


//var csrftoken = Cookies.get('csrftoken');
$("a[id='delete-btn']").click(function() {
    var url = $(this).attr('href');
  $(document).on('submit', '#inactive-form', function (e){
      //var url = $(this).attr("action");
      console.log(url);
     // e.preventDefault();
       $.ajax({
          url: url,
          method: "POST",
          //headers:{"HTTP_X_CSRF_TOKEN":csrftoken},
          success: function(response){
              console.log(response)
              $('#warning-body').html(response);
          }
     })
  });
});


$('#inactive-form').on('hide.bs.modal', function (e) {
    location.reload();
});


