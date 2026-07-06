document.addEventListener("DOMContentLoaded", function(){

const emailChart=document.getElementById("emailChart");

if(emailChart){

new Chart(emailChart,{

type:"bar",

data:{

labels:[

"Safe",

"Medium",

"High"

],

datasets:[{

label:"Email Threats",

data:[

65,

20,

15

]

}]

},

options:{

responsive:true,

plugins:{

legend:{

display:false

}

}

}

});

}

const trendChart=document.getElementById("trendChart");

if(trendChart){

new Chart(trendChart,{

type:"line",

data:{

labels:[

"Mon",

"Tue",

"Wed",

"Thu",

"Fri",

"Sat",

"Sun"

],

datasets:[{

label:"Analysis",

data:[

5,

8,

10,

12,

18,

15,

20

],

fill:false,

tension:.4

}]

},

options:{

responsive:true

}

});

}

const pieChart=document.getElementById("pieChart");

if(pieChart){

new Chart(pieChart,{

type:"pie",

data:{

labels:[

"Email",

"URL"

],

datasets:[{

data:[

65,

35

]

}]

},

options:{

responsive:true

}

});

}

});
