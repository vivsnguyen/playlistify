"use strict";

function playPlaylists(evt) {
    evt.preventDefault();


    $.put('/play-music', (response) => {
        // need to get playlist title and user id
        // BUT do I need it or can i run the server function??
        // going to try on submit
    });
}

$('#choose-playlist-button').on('click', playPlaylists);
