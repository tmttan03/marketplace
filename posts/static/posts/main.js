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


/*Multiple Upload*/
document.addEventListener("DOMContentLoaded", init, false);
    
function init() {
    document.querySelector('#files').addEventListener('change', handleFileSelect, false);
}


function handleFileSelect(e) {
    //to make sure the user select file/files
    if (!e.target.files) return;

    //To obtain a File reference
    var files = e.target.files;

    // Loop through the FileList and then to render image files as thumbnails.
    for (var i = 0, f; f = files[i]; i++) 
    {
        //instantiate a FileReader object to read its contents into memory
        var fileReader = new FileReader();

        // Closure to capture the file information and apply validation.
        fileReader.onload = (function (readerEvt) {
            return function (e) {
                
                //Apply the validation rules for attachments upload
                ApplyFileValidationRules(readerEvt)

                //Render attachments thumbnails.
                RenderThumbnail(e, readerEvt);

                //Fill the array of attachment
                FillAttachmentArray(e, readerEvt)
            };
        })(f);

        // Read in the image file as a data URL.
        // readAsDataURL: The result property will contain the file/blob's data encoded as a data URL.
        // More info about Data URI scheme https://en.wikipedia.org/wiki/Data_URI_scheme
        fileReader.readAsDataURL(f);
    }
    document.getElementById('files').addEventListener('change', handleFileSelect, false);
}

//Render attachments thumbnails.
function RenderThumbnail(e, readerEvt)
{
    var li = document.createElement('li');
    ul.appendChild(li);
    li.innerHTML = ['<div class="img-wrap"> <span class="close">×</span><img class="thumb" src="', e.target.result, '" title="', escape(readerEvt.name), 
                    '" data-id="',readerEvt.name, '"/></div>'].join('');
 
    var div = document.createElement('div');
    div.className = "FileNameCaptionStyle";
    li.appendChild(div);
    div.innerHTML = [readerEvt.name].join('');
    document.getElementById('Filelist').insertBefore(ul, null);
}

//To remove attachment once user click on x button
jQuery(function ($) {
    $('div').on('click', '.img-wrap .close', function () {
        var id = $(this).closest('.img-wrap').find('img').data('id');
 
        //to remove the deleted item from array
        var elementPos = AttachmentArray.map(function (x) { return x.FileName; }).indexOf(id);
        if (elementPos !== -1) {
            AttachmentArray.splice(elementPos, 1);
        }
 
        //to remove image tag
        $(this).parent().find('img').not().remove();
 
        //to remove div tag
        $(this).parent().find('div').not().remove();
 
        //to remove div tag
        $(this).parent().parent().find('div').not().remove();
 
        //to remove li tag
        var lis = document.querySelectorAll('#imgList li');
        for (var i = 0; li = lis[i]; i++) {
            if (li.innerHTML == "") {
                li.parentNode.removeChild(li);
            }
        }
 
    });
}
)

//To check file type according to upload conditions
function CheckFileType(fileType) {
    if (fileType == "image/jpeg") {
        return true;
    }
    else if (fileType == "image/png") {
        return true;
    }
    else if (fileType == "image/gif") {
        return true;
    }
    else {
        return false;
    }
    return true;
}