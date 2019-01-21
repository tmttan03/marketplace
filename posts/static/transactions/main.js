/*Delete Modal*/
$("a[id='delete-cart-btn']").click(function() {
  var link = $(this).attr('href');
  $('#deleteItemModal').on('show.bs.modal', function (e) {
    //var link = $("#detail-card").attr('href');
    //console.log(link);
    console.log(link);
    $.ajax({
          url: link,
          method: "GET",
          success: function(response){
            //console.log(response);
            $('#deleteItemModal').attr('data-url', link);
            $('#delete-auth-body').html(response);
          }
     })
  });
});


$("a[id='delete-cart-btn']").click(function() {
    var url = $(this).attr('href');
  $(document).on('submit', '#inactive-cart-form', function (e){
      console.log(url);
       $.ajax({
          url: url,
          method: "POST",
          success: function(response){
              console.log(response)
              $('#delete-auth-body').html(response);
          }
     })
  });
});


$('#inactive-cart-form').on('hide.bs.modal', function (e) {
    location.reload();
});


/* Update Post */
$("a[id='edit-cart-btn']").click(function() {
  var link = $(this).attr('href');
  $('#update_cart_modal').on('show.bs.modal', function (e) {
    console.log(link)
    $.ajax({
          url: link,
          method: "GET",
          success: function(response){
            //console.log(response);
            $('#update_cart_modal').attr('data-url', link);
            $('#cart-update-holder').html(response);
          }
     })
  });
 });

$("a[id='edit-cart-btn']").click(function() {
    var url = $(this).attr('href');
$(document).on('submit', '#UpdateCartForm', function (e){
    //var url = $(this).attr("action");
    e.preventDefault();
     $.ajax({
        url: url,
        method: "POST",
        data:  $(this).serialize(),
        success: function(response){
            console.log(response)
            $('#cart-update-holder').html(response);
        }
   })
});
});

$('#update_cart_modal').on('hide.bs.modal', function (e) {
    location.reload();
});


