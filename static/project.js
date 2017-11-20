"use strict";

// Facebook OAuth 

// Initialize FB 
window.fbAsyncInit = function() {
    FB.init({
      appId      : '1683033888393903',
      cookie     : true,
      xfbml      : true,
      version    : 'v2.11',
      outh       : true,
    });
      
    FB.AppEvents.logPageView(); 
};


// Load the SDK asynchronously
// (function(d, s, id){
//  var js, fjs = d.getElementsByTagName(s)[0];
//  if (d.getElementById(id)) {return;}
//  js = d.createElement(s); js.id = id;
//  js.src = "https://connect.facebook.net/en_US/sdk.js";
//  fjs.parentNode.insertBefore(js, fjs);
// }(document, 'script', 'facebook-jssdk'));

(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s); js.id = id;
  js.src = 'https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v2.11&appId=385706508528517';
  fjs.parentNode.insertBefore(js, fjs);
} 
(document, 'script', 'facebook-jssdk'));

function facebookLogin() {
    FB.login(function(response) {
        if (response.authResponse) {
            console.log('Authenticated!');
            console.log(response.authResponse.userID);
            console.log(response.authResponse.accessToken);
            var loginInputs = { 'fb_uid':response.authResponse.userID, 
                                'fb_at':response.authResponse.accessToken };
           // try to add them to session 
            $.post('/fb_login', loginInputs, function(data) { 
                console.log(data);
                if (data['user_id']) {
                    // redirect to their profile 
                    window.location.href = `/users/${data['user_id']}`;
                }
            })

        } else if (response.status === 'not_authorized'){
            // the user is logged in to Facebook, 
            // but has not authenticated your app
            console.log('User cancelled login or did not fully authorize.');
            window.location.href = `/register_login`;
        } else {
            // the user isn't logged in to Facebook.
            $.get('/register_login')
        }
    },
    {
        scope: 'email,user_friends,first_name,last_name'
    });
}


function testAPI() {
    console.log('Welcome!  Fetching your information.... ');
    FB.api('/me', function(response) {
      console.log('Successful login for: ' + response.name);
      document.getElementById('status').innerHTML = 'Thanks for logging in, ' + response.name + '!';
        // var loginInputs = { 'fb_uid':response.authResponse.userID, 
        //                         'fb_at':response.authResponse.accessToken };
        //    // try to add them to session 
        //     $.post('/fb_login', loginInputs, function(data) { 
        //         console.log('making request to log in');
        //         if (data['user_id']) {
        //             // redirect to their profile 
        //             window.location.href = `/users/${data['user_id']}`;
        //         }
        //     })
    });

}


function statusChangeCallback(response) {
    console.log('statusChangeCallback');
    console.log(response);
    // The response object is returned with a status field that lets the
    // app know the current login status of the person.
    // Full docs on the response object can be found in the documentation
    // for FB.getLoginStatus().
    if (response.status === 'connected') {
      // Logged into your app and Facebook.
      testAPI();
    } else {
      // The person is not logged into your app or we are unable to tell.
      document.getElementById('status').innerHTML = 'Please log ' +
        'into this app.'; 
    }
}


// This function is called when someone finishes with the Login
// Button.  See the onlogin handler attached to it in the sample
// code below.
function checkLoginState() {
    FB.getLoginStatus(function(response) {
        statusChangeCallback(response);
    });
}



function RegisterWithFB() {
    FB.getLoginStatus(function(response) {
        if (response.status === 'connected') {
        // the user is logged in and has authenticated your
        // app, and response.authResponse supplies
        // the user's ID, a valid access token, a signed
        // request, and the time the access token 
        // and signed request each expire
        var uid = response.authResponse.userID;
        var accessToken = response.authResponse.accessToken;
        console.log(response)
        testAPI()
      } else if (response.status === 'not_authorized') {
        // the user is logged in to Facebook, 
        // but has not authenticated your app
        $.get('/register_login')
      } else {
        // the user isn't logged in to Facebook.
        $.get('/register_login')
      }
     });
}




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