// Facebook OAuth 

// Initialize FB 
window.fbAsyncInit = function() {
    FB.init({
      appId      : '1683033888393903',
      cookie     : true,
      xfbml      : true,
      version    : 'v2.11',
      oauth      : true,
    });
      
    FB.AppEvents.logPageView(); 
};

// Load the SDK asynchronously
(function(d, s, id){
 var js, fjs = d.getElementsByTagName(s)[0];
 if (d.getElementById(id)) {return;}
 js = d.createElement(s); js.id = id;
 js.src = "https://connect.facebook.net/en_US/sdk.js";
 fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));


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
            });

        } else if (response.status === 'not_authorized'){
            // the user is logged in to Facebook, 
            // but has not authenticated your app
            console.log('User cancelled login or did not fully authorize.');
            alert('Please authenticate Keep in Touch')
            // window.location.href = `/register_login`;
        } else {
            // the user isn't logged in to Facebook.
            alert('Please log into FB AND authenticate Keep in Touch')
            // window.location.href = `/register_login`;
        }
    },
    {scope: 'public_profile,email,user_friends'});
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
      facebookLogin(response)
    } else {
      // The person is not logged into your app or we are unable to tell.
      document.getElementById('status').innerHTML = 'Please log ' +
        'into this app.'; 
    }
}



function checkLoginState() {
    FB.getLoginStatus(function(response) {
        statusChangeCallback(response);
        console.log('Welcome!  Fetching your information.... ');
        var url = '/me?fields=id,name,email';
        FB.api(url, function(response) {
             console.log(response.name + " " + response.id + " " +response.email);
                 let formInputs = { 'fname': response.name.split(" ")[0], 
                        'lname':response.name.split(" ")[1], 
                        'email':response.email, 
                        'fb_uid':response.id };
            console.log(formInputs);

        }, {scope: 'email'});
    });
}



function RegisterWithFB() {
    FB.getLoginStatus(function(response) {
        // statusChangeCallback(response);
        console.log('Welcome!  Fetching your information.... ');

        console.log(response.authResponse.accessToken);
        var url = '/me?fields=id,name,email,friends{birthday}';
        FB.api(url, function(response) {
            console.log(response);
            // console.log(response.name + " " + response.id + " " +response.email);

            // let formInputs = {  'fname': response.name.split(" ")[0], 
            //                     'lname':response.name.split(" ")[1], 
            //                     'email':response.email, 
            //                     'fb_uid':response.id    };
            // console.log(formInputs);
            // $.post('/fb_register', formInputs, function(data) {
        
            //     console.log(data);
            //     // console.log('welcome new user! redirecting to profile');
            //     alert(data['result']);
            //     window.location.href = `/users/${data['user_id']}`; 
            //     // if (data['result']) {
            //     //     console.log('existing user!!!');
            //     //     alert(data['result']);
            //     //     window.location.href = '/register_login'; 
            //     // } else {  window.location.href = `/users/${data['user_id']}`; } 
                        
            // });

        }, 

        {scope: "email,user_friends"});
    });
}


//Getting basic user info
function getInfo() {
    FB.api('/me', 'GET', {fields: 'first_name,last_name,name,id'}, function(response){
        alert(response);
    });
}

