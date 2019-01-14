var placeSearch, autocomplete;
var componentForm = {
  street_number: 'short_name',
  route: 'long_name',
  locality: 'long_name',
  administrative_area_level_1: 'short_name',
  country: 'long_name',
  postal_code: 'short_name'
};

function initAutocomplete() {
  // Create the autocomplete object, restricting the search to geographical
  // location types.
  autocomplete = new google.maps.places.Autocomplete(
      /** @type {!HTMLInputElement} */(document.getElementById('autocomplete')),
      {types: ['geocode']});

  // When the user selects an address from the dropdown, populate the address
  // fields in the form.
  autocomplete.addListener('place_changed', fillInAddress);
}


function fillInAddress() {
  // Get the place details from the autocomplete object.
  var place = autocomplete.getPlace();

  for (var component in componentForm) {
    document.getElementById(component).value = '';
    document.getElementById(component).disabled = false;
  }

  // Get each component of the address from the place details
  // and fill the corresponding field on the form.
  for (var i = 0; i < place.address_components.length; i++) {
    var addressType = place.address_components[i].types[0];
    if (componentForm[addressType]) {
      var val = place.address_components[i][componentForm[addressType]];
      document.getElementById(addressType).value = val;
    }
  }
}

// Bias the autocomplete object to the user's geographical location,
// as supplied by the browser's 'navigator.geolocation' object.
function geolocate() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var geolocation = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };
      var circle = new google.maps.Circle({
        center: geolocation,
        radius: position.coords.accuracy
      });
      autocomplete.setBounds(circle.getBounds());
    });
  }
}


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


