{"filter":false,"title":"form.js","tooltip":"/static/media/form.js","undoManager":{"mark":0,"position":0,"stack":[[{"start":{"row":0,"column":0},"end":{"row":23,"column":3},"action":"insert","lines":["$(function () {"," for(var i=1; i<=120; i++){","   var select = document.getElementById(\"prep_time\");","    var option = document.createElement(\"OPTION\");","\t    select.options.add(option);","\t    option.text = i;","\t    option.value = i;","}","  for(var i=5; i<=300; i+= 5){","   var select = document.getElementById(\"cook_time\");","    var option = document.createElement(\"OPTION\");","\t    select.options.add(option);","\t    option.text = i;","\t    option.value = i;","}","  for(var i=1; i<=10; i+= 1){","   var select = document.getElementById(\"servings\");","    var option = document.createElement(\"OPTION\");","\t    select.options.add(option);","\t    option.text = i;","\t    option.value = i;","}","","});"],"id":1}]]},"ace":{"folds":[],"scrolltop":12,"scrollleft":0,"selection":{"start":{"row":23,"column":3},"end":{"row":23,"column":3},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":0},"timestamp":1565884184454,"hash":"9eee240dc6300705f9338f6f645de40107dd5761"}