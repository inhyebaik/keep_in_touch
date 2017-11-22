"use strict";


// Facebook stuff ////////////////////////////////////////////////////////////

window.fbAsyncInit = function() {
    FB.init({
      appId      : '1683033888393903',
      cookie     : true,
      xfbml      : true,
      version    : 'v2.11',
      oauth      : true,
    });
      
    FB.AppEvents.logPageView(); 

    FB.getLoginStatus(function(response) {
        if (response.status === 'connected') {
            // document.getElementById('status1 ').innerHTML = 'we are connected';
            // document.getElementById('login').style.visibility = 'hidden';
        } else if (response.status === 'not_authorized') {
            // document.getElementById('status1').innerHTML = 'we are not logged in';
        } else {
            // document.getElementById('status1').innerHTML = 'You are not logged into FB';
        }
    });
};

// Load the SDK asynchronously
(function(d, s, id){
 var js, fjs = d.getElementsByTagName(s)[0];
 if (d.getElementById(id)) {return;}
 js = d.createElement(s); js.id = id;
 js.src = "https://connect.facebook.net/en_US/sdk.js";
 fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));





// login with FB with extra persmissions
function login() {
    FB.login(function(response) {
        if (response.status === 'connected') {
            document.getElementById('status1').innerHTML = 'we are connected';
            document.getElementById('login').style.visibility = 'hidden';
        } else if (response.status === 'not_authorized') {
            document.getElementById('status1').innerHTML = 'we are not logged in';
        } else {
            document.getElementById('status1').innerHTML = 'You are not logged into FB';
        }

    }, {scope: 'email,user_friends,user_relationships,read_custom_friendlists'});
}

// get information on friends
function getInfo() {
    FB.api('/me', 'GET', {fields: 'id,first_name,last_name,taggable_friends{name,id},friends.limit(10){birthday}'}, function(response) {
        var friends = response['taggable_friends']['data'];
        var friendsNamesID = getNamesID(friends);
        console.log(friendsNamesID);
        var fname = response['first_name'];
        var lname = response['last_name'];
        var fb_uid = response['id'];
        document.getElementById('status1').innerHTML = response;
    });
}

function getNamesID(friends) {
    var friends_names = {};
    for (friend of friends) { friends_names[friend['id']] = friend['name']; }
    return friends_names;
}


// log in and get info
function loginGetInfo() {
    FB.login(function(response) {
        if (response.status === 'connected') {
            document.getElementById('status1').innerHTML = 'we are connected';
            document.getElementById('fb-login-button').style.visibility = 'hidden';
            getInfo();
        } else if (response.status === 'not_authorized') {
            document.getElementById('status1').innerHTML = 'we are not logged in';
        } else {
            document.getElementById('status1').innerHTML = 'You are not logged into FB';
        } 
        

    }, {scope: 'email,user_friends,user_relationships,read_custom_friendlists'});
}


// end Facebook stuff  ////////////////////////////////////////////////////////////






// Get new quote for each refresh (base.html)
$(document).ready(function() {
    $('#quote-text').load('/quote');
});


// When user clicks on a contact name:
// display all of contact's events, add_event for this contact, delete contact
function showEvents(results) {
    let contact_id = results['contact_id'];
    let element = $("#contact-options-"+contact_id);
    if (element.html() === '') {
    for (let e_id in results['events']) {
         $(element).append("<li>" + results['events'][e_id]["date"] + ": " + results['events'][e_id]["template_name"] + "</li>");
        }
    } else {
        element.html(''); }
}

// On user profile, click on a contact and show events
function showOptions(evt) {
    let contact_id = $(this).attr('id');
    let url = "/contact.json";
    let formInputs = { "contact_id" : contact_id};
    $.post(url, formInputs, showEvents);
}   
$('.contact-name').on("click", showOptions);


// When creating an event, ensure dates are today or in the future
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


// Prefilled textarea for event_for_contact.html, event_form.html
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