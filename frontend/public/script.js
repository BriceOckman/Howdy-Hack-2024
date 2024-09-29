document.getElementById('upload-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const videoFile = document.getElementById('video').files[0];
    const presentationFile = document.getElementById('presentation').files[0];

    if (!videoFile || !presentationFile) {
        document.getElementById('error-message').innerText = "Please select both files.";
        return;
    }

    const formData = new FormData();
    formData.append('video', videoFile);
    formData.append('presentation', presentationFile);

    // Redirect to loading page (optional)
    window.location.href = 'loading.html';

    // Send files to backend
    await fetch('/upload', {
        method: 'POST',
        body: formData,
    });
});
