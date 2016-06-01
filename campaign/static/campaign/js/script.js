function likePost(id,type) {
  //preventDefault();
  var counter =  parseInt($("#"+type+"-"+id+"-likes-counter").text());
  counter += 1;
  console.log(counter);
  $("#"+type+"-"+id+"-likes-counter").text(counter);
}
