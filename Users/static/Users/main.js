function reveal() {
    if (document.getElementById('box').checked) {
        document.getElementById("pw").type = 'text';
    } else
        document.getElementById("pw").type = 'password';
}