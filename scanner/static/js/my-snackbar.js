
function setSnackbarVisibility(snackbarID, visibility) {
    var sb = document.getElementById(snackbarID);

    if (visibility && !isSnackbarShown(snackbarID)) {
        sb.className = sb.className.replace("snackbar", "snackbar show");    
    } 
    else if (!visibility && isSnackbarShown(snackbarID)) {
        sb.className = sb.className.replace("show","show hide");
        setTimeout(function() { sb.className = sb.className.replace("snackbar show hide", "snackbar"); }, 500);
    }
}

function isSnackbarShown(snackbarID) {
    var sb = document.getElementById(snackbarID);

    return (sb.className.indexOf("show") != -1);
}
