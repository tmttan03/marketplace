/*$(document).on('submit','#add_product', function(e){
    e.preventDefault();
    $.ajax({
        type:'GET',
        url:'/posts/create/',
        data:{
            name:$('#product_name').val(),
            description:$('#description').val(),
            price:$('#price').val(),
            category:$('#category').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(){
            alert("Created New User");
        }
    })
}*/


