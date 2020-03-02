"use strict";

window.onSpotifyWebPlaybackSDKReady = () => {
  const token = 'BQBGbbtmbND5s1t2_u92sMoA11Ehy7OwXQOmc7euqS3xv-kvaE-3tavrvYmq8kU48iGiFnJ-bjnTlgoPkasMuLUPPqW0GHEuS9L7s4XvspRsva2Lqx4DNp3b2haC0InIHEX78PVpUTlNUXjvt8TYHZaDSZ6dpnXj';
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

  //pause button
  function clickToPauseOrPlay(evt) {
    player.togglePlay().then(() => {
    console.log('Toggled playback!');
    });
  }
  $('#pause-play-button').on('click', clickToPauseOrPlay);

  //next track button
  function clickNextTrack(evt) {
      player.nextTrack().then(() => {
          console.log('Skipped to next track!');
      });
  }
  $('#next-button').on('click', clickNextTrack);

  //previous track button
  function clickPreviousTrack(evt) {
      player.previousTrack().then(() => {
          console.log('Set to previous track!');
      });
  }
  $('#prev-button').on('click', clickPreviousTrack);

  // Start/Resume a User's Playback




  // Connect to the player!
  player.connect();
};
