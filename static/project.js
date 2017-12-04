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
            $('#status1').html('we are connected');
            console.log('we are connected');
        } else if (response.status === 'not_authorized') {
            console.log('we are not logged in');
        } else {
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
        } else if (response.status === 'not_authorized') {
            console.log('we are not logged in');
        } else {
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
            getInfo();
            
        } else if (response.status === 'not_authorized') {
            $('#status1').html('we are not logged in');
            console.log('we are not logged in');
        } else {
             $('#status1').html('You are not logged into FB');
             console.log('You are not logged into FB');
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

$(document).ready(function() {
    var today1 = new Date();
    var dd = today1.getDate();
    var mm = today1.getMonth()+1; //January is 0!
    var yyyy = today1.getFullYear();
    var maxYear = parseInt(today1.getFullYear())+100;
     if(dd<10){ 
        dd='0'+dd ;
        console.log(dd);} 

        if(mm<10){ mm='0'+mm } 
    today1 = yyyy+'-'+mm+'-'+dd;
    var maxDate = maxYear+'-'+mm+'-'+dd;
    $('.datefield').attr('min', today1);
    $('.datefield').attr('max', maxDate);
    console.log("hello!!");
        // console.log($('.datefield').val());
})

// show random message templates in textbox when adding new event ////////////// 
function fillWithMessage(results) {
    console.log(results);
    var msg = results['message']; 
    $('textarea.template_textarea').html(msg);
}

function getMessage(evt) {
    var templateType = $(".template_type").val();
    console.log(templateType);
    let url = "/msg.json";
    let formInputs = {"template_type" : templateType};
    $.post(url, formInputs, fillWithMessage);
}


$(document).ready(function() {
$('.template_type').on('change', getMessage);
})

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

$(document).ready(function() {
$('.template_type2').on('change', getMessage2);
})

// reset form after closing/submitting /////////////////////////////////////////
function returnDefault(evt) {
    $('form').trigger('reset');
    $('.template_textarea2').empty(); 
    $('.template_textarea').empty(); 
}
// add event listener on close and submit of forms
$('button.close').on('click', returnDefault);

// flash messages to disappear /////////////////////////////////////////////////
setTimeout(function(){$('.red').fadeOut();}, 4000);
$(window).click(function(){$('.red').fadeOut();});


// choose-existing: when adding new event, pre-fills contact fields ////////////
function fillInForm(results) {
    $('input[name=contact_id]').val(results['id']);
    $('input[name=contact_name]').val(results['name']);
    $('input[name=contact_email]').val(results['email']);
    $('input[name=contact_address]').val(results['address']);
    $('input[name=contact_phone]').val(results['phone']);
    $('form.newevent').attr("action", "/handle_new_event_for_contact");
    $('form.newevent').attr("method", "POST");
}

function getContactInfo(evt) {
    let contactID = $('.choose-existing').val();
    console.log(contactID);
    let url = "/contact.json";
    let formInputs = {"contact_id": contactID};
    $.post(url, formInputs, fillInForm);
}

$(document).ready(function () {
$('.choose-existing').on('change', getContactInfo)

})


// Carousel ////////////////////////////////////////////////////////////////////
// Instantiate the Bootstrap carousel
$('.multi-item-carousel').carousel({
  interval: false
});

// for every slide in carousel, copy the next slide's item in the slide.
// Do the same for the next, next item.
$('.multi-item-carousel .item').each(function(){
  var next = $(this).next();
  if (!next.length) {
    next = $(this).siblings(':first');
  }
  next.children(':first-child').clone().appendTo($(this));
  
  if (next.next().length>0) {
    next.next().children(':first-child').clone().appendTo($(this));
  } else {
    $(this).siblings(':first').children(':first-child').clone().appendTo($(this));
  }
});






$(document).ready(function () {
    var itemsMainDiv = ('.MultiCarousel');
    var itemsDiv = ('.MultiCarousel-inner');
    var itemWidth = "";

    $('.leftLst, .rightLst').click(function () {
        var condition = $(this).hasClass("leftLst");
        if (condition)
            click(0, this);
        else
            click(1, this)
    });

    ResCarouselSize();




    $(window).resize(function () {
        ResCarouselSize();
    });

    //this function define the size of the items
    function ResCarouselSize() {
        var incno = 0;
        var dataItems = ("data-items");
        var itemClass = ('.item');
        var id = 0;
        var btnParentSb = '';
        var itemsSplit = '';
        var sampwidth = $(itemsMainDiv).width();
        var bodyWidth = $('body').width();
        $(itemsDiv).each(function () {
            id = id + 1;
            var itemNumbers = $(this).find(itemClass).length;
            btnParentSb = $(this).parent().attr(dataItems);
            itemsSplit = btnParentSb.split(',');
            $(this).parent().attr("id", "MultiCarousel" + id);


            if (bodyWidth >= 1200) {
                incno = itemsSplit[3];
                itemWidth = sampwidth / incno;
            }
            else if (bodyWidth >= 992) {
                incno = itemsSplit[2];
                itemWidth = sampwidth / incno;
            }
            else if (bodyWidth >= 768) {
                incno = itemsSplit[1];
                itemWidth = sampwidth / incno;
            }
            else {
                incno = itemsSplit[0];
                itemWidth = sampwidth / incno;
            }
            $(this).css({ 'transform': 'translateX(0px)', 'width': itemWidth * itemNumbers });
            $(this).find(itemClass).each(function () {
                $(this).outerWidth(itemWidth);
            });

            $(".leftLst").addClass("over");
            $(".rightLst").removeClass("over");

        });
    }


    //this function used to move the items
    function ResCarousel(e, el, s) {
        var leftBtn = ('.leftLst');
        var rightBtn = ('.rightLst');
        var translateXval = '';
        var divStyle = $(el + ' ' + itemsDiv).css('transform');
        var values = divStyle.match(/-?[\d\.]+/g);
        var xds = Math.abs(values[4]);
        if (e == 0) {
            translateXval = parseInt(xds) - parseInt(itemWidth * s);
            $(el + ' ' + rightBtn).removeClass("over");

            if (translateXval <= itemWidth / 2) {
                translateXval = 0;
                $(el + ' ' + leftBtn).addClass("over");
            }
        }
        else if (e == 1) {
            var itemsCondition = $(el).find(itemsDiv).width() - $(el).width();
            translateXval = parseInt(xds) + parseInt(itemWidth * s);
            $(el + ' ' + leftBtn).removeClass("over");

            if (translateXval >= itemsCondition - itemWidth / 2) {
                translateXval = itemsCondition;
                $(el + ' ' + rightBtn).addClass("over");
            }
        }
        $(el + ' ' + itemsDiv).css('transform', 'translateX(' + -translateXval + 'px)');
    }

    //It is used to get some elements from btn
    function click(ell, ee) {
        var Parent = "#" + $(ee).parent().attr("id");
        var slide = $(Parent).attr("data-slide");
        ResCarousel(ell, Parent, slide);
    }

});




$(function() {
        var $grid = $('.grid').masonry({
            itemSelector: '.grid-item',
            columnWidth: 290,
        }); })


