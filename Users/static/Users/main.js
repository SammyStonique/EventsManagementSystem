function reveal() {
    if (document.getElementById('box').checked) {
        document.getElementById("id_password").type = 'text';
        document.getElementById("id_new_password1").type = 'text';
        document.getElementById("id_new_password2").type = 'text';
    } else {
        document.getElementById("id_password").type = 'password';
        document.getElementById("id_new_password1").type = 'password';
        document.getElementById("id_new_password2").type = 'password';
    }
}