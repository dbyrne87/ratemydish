$(function () {
    for(var i=1; i<=120; i++){
    var select = document.getElementById("prep_time");
        var option = document.createElement("OPTION");
	    select.options.add(option);
	    option.text = i;
	    option.value = i;
}
  for(var i=5; i<=300; i+= 5){
   var select = document.getElementById("cook_time");
    var option = document.createElement("OPTION");
	    select.options.add(option);
	    option.text = i;
	    option.value = i;
}
  for(var i=1; i<=10; i+= 1){
   var select = document.getElementById("servings");
    var option = document.createElement("OPTION");
	    select.options.add(option);
	    option.text = i;
	    option.value = i;
}

});