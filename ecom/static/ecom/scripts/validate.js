// Validate whether username and password is entered or not
function validate_login() {
    status = 1;
    username = document.getElementById("username");
    password = document.getElementById("userpassword");
    if (username.value == "") {
        username.style.borderColor = "#FF0000";
        status = 0;
    } else {
        username.style.borderColor = "#ced4da"
        status = 1;
    }
    if (password.value == "") {
        password.style.borderColor = "#FF0000";
        status = 0;
    } else {
        password.style.borderColor = "#ced4da";
        status = 1;
    }
    if (status == 0) {
        return false;
    }

} //End validate



//Remove resubmit form while refresh
if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}


function signup_validate() {

    signinstatus = 1;
    usrtype = document.getElementById("usrtyp");
    if (usrtype.value == "reseller") {
        var a = 1;
    } else {
        //firstname validation
        fname = document.getElementById("fname")
        if (fname.value == "") {
            fname.style.borderColor = "#FF0000";
            signinstatus = 0;
        } else {
            fname.style.borderColor = "#ced4da";
        }

        // validate date of birth
        dateofbirth = document.getElementById("dob")
        if (dateofbirth.value == "") {
            dateofbirth.style.borderColor = "#FF0000";
            signinstatus = 0;
        } else {
            dateofbirth.style.borderColor = "#ced4da";
        }
    }

    // validate address
    address = document.getElementById("adrs");
    if (address.value == "") {
        address.style.borderColor = "#FF0000";
        signinstatus = 0;
    } else {
        address.style.borderColor = "#ced4da";
    }
    // validate country
    country = document.getElementById("cntry")
    if (country.value == "") {
        country.style.borderColor = "#FF0000";
        signinstatus = 0;
    } else {
        country.style.borderColor = "#ced4da";
    }
    // validate mobile number
    var phoneformat = /^\d{10}$/;
    phone = document.getElementById("userMobile");
    if (phone.value.match(phoneformat)) {
        phone.style.borderColor = "#ced4da";

    } else {
        phone.style.borderColor = "#FF0000";
        signinstatus = 0;
    }

    //  Validate mail valid or not
    var mailformat = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    mail = document.getElementById("userEmail")
    if (mail.value.match(mailformat)) {
        mail.style.borderColor = "#ced4da";
    } else {
        mail.style.borderColor = "#FF0000";
        signinstatus = 0;
    }
    // validate password is entered or not
    password = document.getElementById("userPassword");
    cnfpassword = document.getElementById("cnfPassword");
    document.getElementById("pswerror").innerHTML = ""
    if (password.value == "") {
        password.style.borderColor = "#FF0000";
        signinstatus = 0;
    } else {
        password.style.borderColor = "#ced4da";

    }
    // validate password and confirm password matching
    if (password.value != cnfpassword.value) {
        signinstatus = 0;
        document.getElementById("pswerror").innerHTML = "paaassword and confirm password mismatch";
        cnfpassword.style.borderColor = "#FF0000";
    } else {
        cnfpassword.style.borderColor = "#ced4da";
    }

    if (signinstatus == 0) {
        return false;
    }
}