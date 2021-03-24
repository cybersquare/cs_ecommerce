//Remove resubmit form while refresh
if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}

function validate_login() {
    console.log("test")
    status = 1;
    username = document.getElementById("admusername");
    password = document.getElementById("admpassword");
    if (username.value == "") {
        username.style.borderColor = "#FF0000";
        status = 0;
    } else {
        username.style.borderColor = "#ced4da"
    }
    if (password.value == "") {
        password.style.borderColor = "#FF0000";
        status = 0;
    } else {
        password.style.borderColor = "#ced4da";

    }
    console.log(status)
    if (status == 0) {
        return false;
    }
}