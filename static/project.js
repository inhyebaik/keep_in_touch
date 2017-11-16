"use strict";


// ensure event dates are today or in the future
let today = new Date();
let dd = today.getDate();
let mm = today.getMonth()+1; //January is 0!
let yyyy = today.getFullYear();
let maxYear = parseInt(today.getFullYear())+100;
 if(dd<10){ dd='0'+dd } 
    if(mm<10){ mm='0'+mm } 
today = yyyy+'-'+mm+'-'+dd;
let maxDate = maxYear+'-'+mm+'-'+dd;
$('.datefield').attr('min', today);
$('.datefield').attr('max', maxDate);


// prefilled textarea for event_for_contact.html, event_form.html
$('.template_type').on('change', function() {
    let templateType = $(".template_type").val();
        let msg = "";
        if (templateType === "ty") {
            msg = "Thank you so much for this";
        } 
        else if (templateType === "hb") {
            msg = "Happy birthday! You're awesome!";
        } 
        else if (templateType === "fup") {
            msg = "I'm just following up on our last meeting :)";
        }
    $('.template_textarea').text(msg);
})