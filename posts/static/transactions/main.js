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



$("#target").change(function() {
    var url = $('#UpdateItemForm').attr('action');
    console.log(url);
    e.preventDefault();
    $.ajax({
        url: url,
        method: "POST",
        data: $(this).val(),
        success: function(response){
            console.log(response)
        }
   })
});


