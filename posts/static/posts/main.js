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






