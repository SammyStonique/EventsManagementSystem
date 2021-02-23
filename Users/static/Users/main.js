/* Null check on updateHTML */
function updateHTML(elmId, value) {
    var elem = document.getElementById(elmId);
    if (typeof elem !== 'undefined' && elem !== null) {
        elem.innerHTML = value;
    }
}

function reveal() {
    if (document.getElementById('box').checked) {
        document.getElementById("pw").type = 'text';
    } else
        document.getElementById("pw").type = 'password';
}