Song_Container = document.querySelector('.main');

if (songs.length != 0) {
    AddSongs(songs);
} else {
    console.log("No songs found.");
}

function AddSongs(songs) {
    songs.forEach(song => {
        const loaderDiv = document.createElement('div');
        loaderDiv.classList.add('loader');
        loaderDiv.id = song.id;
        loaderDiv.innerHTML = `
        <div class="song">
      <p class="name">${ song.title }</p>
      <p class="artist">${ song.singer }</p>
    </div>
    <div class="albumcover">
      <img width="100%" height="100%" src="${ song.image }" alt="" />
    </div>
    <div class="play"></div>
    <div class="loading visually-hidden">
      <div class="load"></div>
      <div class="load"></div>
      <div class="load"></div>
      <div class="load"></div>
    </div>
        
        `
        Song_Container.appendChild(loaderDiv);

    });

}