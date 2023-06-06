// JavaScript code
function chooseRandomWord() {
    fetch('http://127.0.0.1:5000/random_word')
        .then(response => response.text())
        .then(word => {
            document.getElementById("referenceWord").value = word;
        });
}

document.getElementById("suggestRandomWord").addEventListener("click", chooseRandomWord);
