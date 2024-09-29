document.getElementById('upload-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const videoFile = document.getElementById('video').files[0];
    const presentationFile = document.getElementById('presentation').files[0];

    if (!videoFile || !presentationFile) {
        document.getElementById('error-message').innerText = "Please select both files.";
        return;
    }

    // Create FormData object
    const formData = new FormData();
    formData.append('video', videoFile);
    formData.append('presentation', presentationFile);

    // Redirect to loading page
    window.location.href = 'loading.html';

    // Optionally send to backend here and then redirect to result.html after processing
    // await fetch('http://your-python-backend-url/upload', {
    //     method: 'POST',
    //     body: formData
    // });
});
