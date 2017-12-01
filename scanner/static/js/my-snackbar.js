
function setSnackbarVisibility(snackbarID, visibility) {
    var sb = document.getElementById(snackbarID)

    if (visibility) {
        if (!isShown()) {
            sb.className = "show";
        }
    } 
    else {
        sb.className = sb.className.replace("show","hide");
        setTimeout(function() { sb.className = sb.className.replace("hide", ""); }, 500);
    }
}

function isSnackbarShown(snackbarID) {
    var sb = document.getElementById(snackbarID);

    return (sb.className.indexOf("show") != -1);
}
