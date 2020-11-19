"use strict";

function playPlaylists(evt) {
    evt.preventDefault();

    const formInput = {'playlist_id': evt.target.id}
    // evt.target is the form

    const playlistId = evt.target.id;

    // console.log(evt.target.serialize)

    // const playerButtons = $(evt.target).siblings('.player-buttons');
    // playerButtons.hide();

    $('.now-playing').hide();
    $('.player-buttons').hide();


    $(evt.target).siblings(`#player-buttons-${playlistId}`).show();

    // const nowPlaying = $(evt.target).siblings('.now-playing');
    // console.log(nowPlaying)

    $.get('/play-music', formInput, (response) => {
      console.log(response);
      // nowPlaying.hide();
      $(`#now-playing-${evt.target.id}`).show();
      $(`#now-playing-${evt.target.id}`).text(response);
    });
}
