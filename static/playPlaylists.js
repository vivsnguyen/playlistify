"use strict";

function playPlaylists(evt) {
    evt.preventDefault();

    const formInput = {'playlist_id': evt.target.id}
    // evt.target is the form

    const playlistId = evt.target.id;
    console.log(playlistId)

    // console.log(evt.target.serialize)
    const playerButtons = $(evt.target).siblings('.player-buttons');

    playerButtons.hide();
    $(evt.target).siblings(`#player-buttons-${playlistId}`).show();
    // $(evt.target).siblings('.player-buttons').show();

    const nowPlaying = $(evt.target).siblings('.now-playing');

    $.get('/play-music', formInput, (response) => {
      console.log(response);
      nowPlaying.hide();
      $(`#now-playing-${evt.target.id}`).show();
      $(`#now-playing-${evt.target.id}`).text(response);
    });
}
