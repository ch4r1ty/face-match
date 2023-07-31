function submitForm(event) {
    event.preventDefault();
    var image_path = document.getElementById('image_path').value;
    fetch('/find_person_info', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            image_path: image_path,
        }),
    })
    .then(response => response.json())
    .then(data => {
        var resultDiv = document.getElementById('result');
        resultDiv.textContent = JSON.stringify(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
