"use strict";

// Facebook OAuth ////////////////////////////////////////////////////////////
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
            // document.getElementById('status1').innerHTML = 'we are connected';
            $('#status1').html('we are connected');
            console.log('we are connected');
            // document.getElementById('whatever').style.visibility = 'hidden';
        } else if (response.status === 'not_authorized') {
            // document.getElementById('status1').innerHTML = 'we are not logged in';
            console.log('we are not logged in');
        } else {
            // document.getElementById('status1').innerHTML = 'You are not logged into FB';
            console.log('you are not logged into FB');
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


// login with FB with scope permissions
function login() {
    FB.login(function(response) {
        if (response.status === 'connected') {
            $('#status1').html('we are connected');
            console.log('we are connected');
            // document.getElementById('status1').innerHTML = 'we are connected';
        } else if (response.status === 'not_authorized') {
            // document.getElementById('status1').innerHTML = 'we are not logged in';
            console.log('we are not logged in');
        } else {
            // document.getElementById('status1').innerHTML = 'You are not logged into FB';
            console.log('you are not logged into FB');
        }

    }, {scope: 'email,user_friends,user_relationships,read_custom_friendlists'});
}

// helper function 
function getNamesID(friends) {
    var friends_names = {};
    for (let friend of friends) 
        { friends_names[friend['id']] = friend['name']; }
    return friends_names;
}

// get info from FB after successful login
function getInfo() {
    FB.api('/me', 'GET', {fields: 'id,email,first_name,last_name,family{name,id},taggable_friends{name,id},friends{birthday}'}, function(response) {
        var famdata = response['family']['data']
        var frdata = response['taggable_friends']['data'];
        console.log(frdata);
        var familyIDName = getNamesID(famdata);
        var friendsIDName = getNamesID(frdata);
        var fname = response['first_name'];
        var lname = response['last_name'];
        var email = response['email'];
        var fb_uid = response['id'];

        console.log(fname, lname, email, fb_uid, Object.values(familyIDName), Object.values(friendsIDName));
      
        document.getElementById('status1').innerHTML = response;
    });
}


// after FB login and getInfo, use information to app login/register
function registerLogInFB(fname, lname, email, fb_uid) {
    var loginInputs = {
                        'fname': fname,
                        'lname': lname,
                        'email': email,
                        'fb_uid': fb_uid  };
    console.log(loginInputs);
    // try to add them to session
    $.post('/fb_register', loginInputs, function(data){
        console.log('route response came back!!!');
        console.log(data);
        if (data['user_id']){
            // redirect to their profile
            window.location.href = `/users/${data['user_id']}`;
        } 
    });

}

var contactsList;
// makes FB API request; uses that information to register/login to our app)
function getInfoRegisterLogin() {
    FB.api('/me', 'GET', {fields: 'id,email,first_name,last_name,picture.width(100).height(100),family{name,id,picture.width(100).height(100)},taggable_friends{name,id,picture.width(100).height(100)},friends{birthday}'}, function(response) {
        // debugger;
        console.log(response);
        $('#status1').html('we are connected');
        var famdata = response['family']['data']
        var frdata = response['taggable_friends']['data'];
        var cdata = famdata.concat(frdata);
        console.log(cdata);
        contactsList = getContacts(cdata);
        console.log(contactsList);

        var familyIDName = getNamesID(famdata);
        var friendsIDName = getNamesID(frdata);
        var fname = response['first_name'];
        var lname = response['last_name'];
        var email = response['email'];
        var fb_uid = response['id'];
        var pic_url = response['picture']['data']['url']
        console.log(pic_url);
        console.log(fname, lname, email, fb_uid, Object.values(familyIDName), Object.values(friendsIDName));
        
        var loginInputs = {
                        'fname': fname,
                        'lname': lname,
                        'email': email,
                        'fb_uid': fb_uid,
                        'pic_url': pic_url,
                        'contacts_list': JSON.stringify(contactsList) };
        console.log(loginInputs);
        $.post('/fb_register', loginInputs, function(data){

            console.log('route response came back!!!');
            console.log(data);
            
            if (data['user_id']) window.location.href = `/users/${data['user_id']}`;


    });
});
}



function getContacts(friends) {
    let namesList = [];
    for (let f in friends){
        let name=friends[f]['name'];
        let pic_url=friends[f]['picture']['data']['url']
        namesList.push([name, pic_url]); }
    return namesList;
}


function loginGetInfo() {
    // logs in via FB; getInfo from FB (calls getInfo())

    // log in FB with scope permissions
    FB.login(function(response) {
        if (response.status === 'connected') {
            $('#status1').html('we are connected');
            console.log('we are connected');
            // document.getElementById('status1').innerHTML = 'we are connected';
            // document.getElementById('whatever').style.visibility = 'hidden';
            getInfo();
            
        } else if (response.status === 'not_authorized') {
            $('#status1').html('we are not logged in');
            console.log('we are not logged in');
            // document.getElementById('status1').innerHTML = 'we are not logged in';
        } else {
             $('#status1').html('You are not logged into FB');
             console.log('You are not logged into FB');
            // document.getElementById('status1').innerHTML = 'You are not logged into FB';
        } 

    }, {scope: 'email,user_friends,user_relationships,read_custom_friendlists'});
}



function loginGetInfo2() {
   // logs in via FB; getInfo from FB
   // attempts to register/log user into our app (calls getInfoRegisterLogin())

    // log in with scope permissions
    FB.login(function(response) {
        if (response.status === 'connected') {
            $('#status1').html('we are connected');
            // document.getElementById('whatever').style.visibility = 'hidden';
    
            // if successful FB login, get info thru FB API and login/register on our app
            getInfoRegisterLogin()
            
        } else if (response.status === 'not_authorized') {
            $('#status1').html('we are not logged in');
        } else {
            $('#status1').html('You are not logged into FB');
        } 

    }, {scope: 'email,user_friends,user_relationships,read_custom_friendlists'});
}

// end Facebook ////////////////////////////////////////////////////////////////


// Get new quote for each refresh (base.html) //////////////////////////////////
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

// On user profile, click on a contact and show events /////////////////////////
function showOptions(evt) {
    let contact_id = $(this).attr('id');
    let url = "/contact.json";
    let formInputs = { "contact_id" : contact_id};
    $.post(url, formInputs, showEvents);
}   
$('.contact-name').on("click", showOptions);


// When creating an event, ensure dates are today or in the future /////////////
var today1 = new Date();
var dd = today1.getDate();
var mm = today1.getMonth()+1; //January is 0!
var yyyy = today1.getFullYear();
var maxYear = parseInt(today1.getFullYear())+100;
 if(dd<10){ dd='0'+dd } 
    if(mm<10){ mm='0'+mm } 
today1 = yyyy+'-'+mm+'-'+dd;
var maxDate = maxYear+'-'+mm+'-'+dd;
$('.datefield').attr('min', today1);
$('.datefield').attr('max', maxDate);


// show random message templates in textbox when adding new event ////////////// 
function fillWithMessage(results) {
    let msg = results['message']; 
    $('textarea.template_textarea').html(msg);
}

function getMessage(evt) {
    let templateType = $(".template_type").val();
    console.log(templateType);
    let url = "/msg.json";
    let formInputs = {"template_type" : templateType};
    $.post(url, formInputs, fillWithMessage);
}

$('.template_type').on('change', getMessage);

// adding event for specific contact
// show random message templates in textbox when adding new event ////////////// 
function fillWithMessage2(results) {
    var msg = results['message']; 
    $('.template_textarea2').html(msg);
}

function getMessage2(evt) {
    var t = $(this).val();
    console.log("this is this:");
    console.log($(this).val());
    console.log(t);
    var url = "/msg.json";
    var formInputs = {"template_type" : t};
    $.post(url, formInputs, fillWithMessage2);
}

$('.template_type2').on('change', getMessage2);



// reset form after closing/submitting /////////////////////////////////////////
function returnDefault(evt) {
    $('form').trigger('reset');
    $('.template_textarea2').empty(); 
    $('.template_textarea').empty(); 
}
// add event listener on close and submit of forms
$('button.close').on('click', returnDefault);
// $('.newevent').on('submit', returnDefault);

// flash messages to disappear /////////////////////////////////////////////////
 // $('.red').hide().fadeIn();
setTimeout(function(){$('.red').fadeOut();}, 4000);
$(window).click(function(){$('.red').fadeOut();});


// choose-existing: when adding new event, pre-fills contact fields ////////////
function getContactInfo(evt) {
    let contactID = $('.choose-existing').val();
    console.log(contactID);
    let url = "/contact.json";
    let formInputs = {"contact_id": contactID};
    $.post(url, formInputs, fillInForm);
}

function fillInForm(results) {
    $('input[name=contact_name]').val(results['name']);
    $('input[name=contact_email]').val(results['email']);
    $('input[name=contact_address]').val(results['address']);
    $('input[name=contact_phone]').val(results['phone']);
}

$('.choose-existing').on('change', getContactInfo)


