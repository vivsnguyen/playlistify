"use strict";

window.onSpotifyWebPlaybackSDKReady = () => {
  const token = 'BQCBmY8hfzyS-MMVlm2dkedpAjk6VQI0-rekDF6F3BD0d3EBGaU7IINZ5TNEjdm0sECOtI9owIwEOhoGImxux1v9U-opGRk3g5r0wjLwDT40_ieu4F0y6RTpgpJvDdpp01Uf2KuHzgmy3ZX6YEj2Yq5kMxF6-2LZ';
  const player = new Spotify.Player({
    name: 'Playlist Web Player thingy',
    getOAuthToken: cb => { cb(token); }
  });

  // Error handling
  player.addListener('initialization_error', ({ message }) => { console.error(message); });
  player.addListener('authentication_error', ({ message }) => { console.error(message); });
  player.addListener('account_error', ({ message }) => { console.error(message); });
  player.addListener('playback_error', ({ message }) => { console.error(message); });

  // Playback status updates
  player.addListener('player_state_changed', state => { console.log(state); });

  // Ready
  player.addListener('ready', ({ device_id }) => {
    console.log('Ready with Device ID', device_id);
  });

  // Not Ready
  player.addListener('not_ready', ({ device_id }) => {
    console.log('Device ID has gone offline', device_id);
  });

  // pause button
  function clickToPauseOrPlay(evt) {
    player.togglePlay()
    console.log('Toggled playback!');
    // });
  }
  // $('#pause-play-button').on('click', clickToPauseOrPlay);

  $('button.pause-play-button').on('click', clickToPauseOrPlay);

  //next track button
  function clickNextTrack(evt) {
      
      player.nextTrack().then(() => {
          console.log('Skipped to next track!');
      });
  }

  // $('.next-button').on('click', clickNextTrack);

   $('button.next-button').on('click', clickNextTrack);

  //previous track button
  function clickPreviousTrack(evt) {
      player.previousTrack().then(() => {
          console.log('Set to previous track!');
      });
  }
  // $('.prev-button').on('click', clickPreviousTrack);

  $('button.prev-button').on('click', clickPreviousTrack);

  // Start/Resume a User's Playback




  // Connect to the player!
  player.connect();
};
