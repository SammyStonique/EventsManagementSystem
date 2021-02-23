function reveal() {
    if (document.getElementById('box').checked) {
        document.getElementById("id_password").type = 'text';
    } else
        document.getElementById("id_password").type = 'password';
}