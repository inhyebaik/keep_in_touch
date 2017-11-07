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