"use strict";

function playPlaylists(evt) {
    evt.preventDefault();

    const formInput = {'playlist_title': evt.target.id}
    // evt.target is the form

    // console.log(evt.target.serialize)

    $(evt.target).siblings('.player-buttons').show();

    $.get('/play-music', formInput, (response) => {
      console.log(response);
      // display what playlist is playing html?
    });
}
