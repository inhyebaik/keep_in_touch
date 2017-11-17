"use strict";


// get new quote for each refresh (base.html)
$(document).ready(function() {
    $('#quote-text').load('/quote');
});

// when user clicks on a contact name:
// display all of contact's events, add_event for this contact, delete contact
function showEvents(results) {
    // console.dir(Object.keys(results));
    console.log("in showEvents");
    let contact_id = results['contact_id'];
    let element = $("#contact-options-"+contact_id);
    if (element.html() === '') {
    for (let e_id in results['events']) {
        console.log(element);
         $(element).append("<li>" + results['events'][e_id]["template_name"] + "</li>");
        }
    } else {
        element.html(''); }
}


function showOptions(evt) {
    let contact_id = $(this).attr('id');
    let url = "/contact.json";
    let formInputs = { "contact_id" : contact_id};
    $.post(url, formInputs, showEvents);
}   

$('.contact-name').on("click", showOptions);


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