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
