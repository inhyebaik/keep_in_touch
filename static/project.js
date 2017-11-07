"use strict";

// function handleGenre(evt) {

//     evt.preventDefault();
//     let formInput = {
//         "inputGenre": $("#genre-option").val()
//     }

//     $.get('/movie-filter.json', formInput, filterGenre);
// }

// function filterGenre(results) {

//     $("#movie-list").empty();
//     for (let movie in results) {
//         $("#movie-list").append(
//                   `<li>
//                       <a href="/movies/${results[movie]}">
//                         ${movie} (${results[movie]})
//                       </a>
//                   </li>`
//             );
//         }
// }

// $('#genre-option').on('change', handleGenre);


 // copied from http://jsfiddle.net/trixta/h7YdJ/ for calendar input on new event
// webshims.setOptions('forms-ext', {
//     replaceUI: 'auto',
//     types: 'date'
// });
// webshims.polyfill('forms forms-ext');

// $(function(){
//     $('[type="date"].min-today').prop('min', function(){
//         return new Date().toJSON().split('T')[0];
//     });
// });


// ensure event dates are today or in the future
let today = new Date();
let dd = today.getDate();
let mm = today.getMonth()+1; //January is 0!
let yyyy = today.getFullYear();
 if(dd<10){ dd='0'+dd } 
    if(mm<10){ mm='0'+mm } 
today = yyyy+'-'+mm+'-'+dd;
document.getElementById("neweventdate").setAttribute("min", today);
document.getElementById("editeventdate").setAttribute("min", today)


