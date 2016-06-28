//DJANGO CSRF CODE

/**
 * setup JQuery's AJAX methods to setup CSRF token in the request before sending it off.
 * http://stackoverflow.com/questions/5100539/django-csrf-check-failing-with-an-ajax-post-request
 */

function getCookie(name)
{
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?

            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
     beforeSend: function(xhr, settings) {
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
});


//LIKE FUNCTION
function likePost(id,type) {
  //preventDefault();
  console.log('called like button');
  var counter =  parseInt($("#"+type+"-"+id+"-likes-counter").text());
  //counter += 1;
  $("#"+type+"-"+id+"-likes-counter").text(counter);
  //$("#btn-like-"+type+"-"+id).attr('disabled','disabled');
  $.ajax(location.origin+"/"+type+"/"+id+"/like", {
     success: function(data) {
       //console.log(data)
        $("#"+type+"-"+id+"-likes-counter").text(data.likes);
        console.log('got some data');
     },
     error: function() {
        console.log("Error Occurred!");
     }
  });
}
function dislike(id,type) {
  //preventDefault();
  var counter =  parseInt($("#"+type+"-"+id+"-dislikes-counter").text());
  //counter += 1;
  $("#"+type+"-"+id+"-dislikes-counter").text(counter);
  $("#btn-dislike-"+type+"-"+id).attr('disabled','disabled');
  $.ajax(location.origin+"/"+type+"/"+id+"/dislike", {
     success: function(data) {
        $("#"+type+"-"+id+"-dislikes-counter").text(data.dislikes);
     },
     error: function() {
        console.log("Error Occurred!");
     }
  });
}


/*
var frm = $('#commentform');
console.log('got the form');
frm.submit(function () {
    $.ajax({
        type: frm.attr('method'),
        url: frm.attr('action'),
        data: frm.serialize(),
        success: function (data) {
          console.log('success: appending the data to the list');
            //$("#SOME-DIV").html(data);
            $("#comments ul").append('<li class="comment"><strong>'+ You +'</strong> <em>said</em>: '+ $("#id_text").val() +', <strong><span id="comment-'+ data.commentId +'-likes-counter">'+ 0 +'</span></strong> people liked this. <button id="btn-like-comment-'+ 0 +'" class="btn btn-default like" onclick="likePost("'+ 0 +'", "comment")"> <i class="glyphicon glyphicon-heart red-text"></i> like</button>')
        },
        error: function(data) {
            console.log('Sorry there is an error');
            $("#comments ul").append('<li class="comment"> Sorry there is an error, your comment didn\'t reach us');
        }
    });
    console.log('Returning...')
    return false;
});
*/
