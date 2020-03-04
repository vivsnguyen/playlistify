"use strict";

function playPlaylists(evt) {
    evt.preventDefault();

    const formInput = {'playlist_title': $('input[name="playlist_title"]').val()}

    // const playlistTitle = $('input[name="playlist_title"]').val();
    console.log(formInput);

    $(evt.target).siblings('.player-buttons').show();

    $.get('/play-music', formInput, (response) => {
      console.log(response);
    });
}
