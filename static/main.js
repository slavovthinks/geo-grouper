document.getElementById('submitManual').addEventListener('click', function() {
    const manualData = document.getElementById('manualEntry').value;
    const dataArray = manualData.split('\n').map(line => {
        const commaIndex = line.indexOf(',');
        const name = line.substring(0, commaIndex).trim();
        const address = line.substring(commaIndex + 1).trim();
        return { name, address };
    });
    postData('/groups/', dataArray);
});

document.getElementById('submitFile').addEventListener('click', function() {
    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    postFile('/groups/csv/', formData);
});

document.getElementById('downloadResults').addEventListener('click', function() {
    download('grouped_results.txt', document.getElementById('results').innerText);
});

function postData(url, data) {
    showSpinner(true);
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        showSpinner(false);
        displayResults(data);
    })
    .catch((error) => {
        showSpinner(false);
        console.error('Error:', error);
    });
}

function postFile(url, data) {
    showSpinner(true);
    fetch(url, {
        method: 'POST',
        body: data,
    })
    .then(response => response.json())
    .then(data => {
        showSpinner(false);
        displayResults(data);
    })
    .catch((error) => {
        showSpinner(false);
        console.error('Error:', error);
    });
}

function displayResults(data) {
    let resultText = data.map(group => group.users.map(user => user.name).join(', ')).join('\n');
    document.getElementById('results').textContent = resultText;
    document.getElementById('downloadResults').style.display = 'block';
}

function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}
function showSpinner(show) {
    document.getElementById('overlay').style.display = show ? 'flex' : 'none';
}
