function likePost(id,type) {
  //preventDefault();
  var counter =  parseInt($("#"+type+"-"+id+"-likes-counter").text());
  counter += 1;
  $("#"+type+"-"+id+"-likes-counter").text(counter);
  $("#btn-like-"+type+"-"+id).attr('disabled','disabled');
  $.ajax(location.origin+"/"+type+"/"+id+"/like", {
     success: function(data) {
        $("#"+type+"-"+id+"-likes-counter").text(data.likes);
     },
     error: function() {
        console.log("Error Occurred!");
     }
  });
}
$(document).ready({
  $.ajax({
        type:'GET',
        url: 'http://vimeo.com/api/v2/video/' + video_id + '.json',
        jsonp: 'callback',
        dataType: 'jsonp',
        success: function(data){
            var thumbnail_src = data[0].thumbnail_large;
            $('#thumb_wrapper').append('<img src="' + thumbnail_src + '"/>');
        }
    });
});
