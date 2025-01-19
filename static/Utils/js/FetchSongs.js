function callApi(query) {
    console.log("Calling API...");
    // const inputField = document.getElementById('searchInput');
    // const searchQuery = inputField.value;

    const inputData = {
        data: query
    };

    fetch('http://127.0.0.1:5000/api/scrapper', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(inputData),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(result => {
            if (result) {
                DataArray = result; // Call AddSongs here
            }
        })
        .catch(error => {
            console.error("Error calling API:", error);
        });
}

// function AddSongs(data) {
//     const Song_Container = document.querySelector('.main');

//     console.log("Adding songs...");
//     const songs = data.data;

//     songs.forEach(song => {
//         const loaderDiv = document.createElement('div');
//         loaderDiv.classList.add('loader');
//         loaderDiv.id = song.id;
//         loaderDiv.innerHTML = `
//         <div class="song">
//       <p class="name">${ song.title }</p>
//       <p class="artist">${ song.singer }</p>
//     </div>
//     <div class="albumcover">
//       <img width="100%" height="100%" src="${ song.image }" alt="" />
//     </div>
//     <div class="play"></div>
//     <div class="loading visually-hidden">
//       <div class="load"></div>
//       <div class="load"></div>
//       <div class="load"></div>
//       <div class="load"></div>
//     </div>

//         `
//         Song_Container.appendChild(loaderDiv);

//     });

// }