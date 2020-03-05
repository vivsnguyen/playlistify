"use strict";

function playPlaylists(evt) {
    evt.preventDefault();

    const formInput = {'playlist_title': evt.target.id}
    // evt.target is the form

    // console.log(evt.target.serialize)
    console.log($(evt.target).siblings('#player-buttons'+evt.target.id))
    $(evt.target).siblings('.player-buttons').show();

    $.get('/play-music', formInput, (response) => {
      console.log(response);
      $('#now-playing-'+evt.target.id).text(response);
      // display what playlist is playing html?
    });
}
