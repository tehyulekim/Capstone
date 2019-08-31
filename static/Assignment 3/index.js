/*

*/



function disappearId(nameString) {
    document.getElementById(nameString).style.display = "none";
}

function appearId(nameString) {
    document.getElementById(nameString).style.display = "block";
}

function disappearClass(nameString) {
    for (let i = 0; i < document.getElementsByClassName(nameString).length; i++) {
        document.getElementsByClassName(nameString)[i].style.display = "none";
    }
    document.getElementById(nameString).classList.remove("active");
}

function appearClass(nameString) {
    for (let i = 0; i < document.getElementsByClassName(nameString).length; i++) {
        document.getElementsByClassName(nameString)[i].style.display = "block";
    }
    document.getElementById(nameString).classList.add("active");
}


/*window.outer width 816 | 817 */
// <button type="button" onclick="openNav()">OPEN SIDEBAR</button>
// <button type="button" onclick="closeNav()">CLOSE SIDEBAR</button>
/* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
function openNav() {
    if (window.outerWidth > 816) { // console.log(window.outerWidth);
        document.getElementById("sidebar").style.width = "320px";
        document.getElementById("content").style.marginLeft = "320px";
    }
}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
function closeNav() {
    if (window.outerWidth > 816) {
        document.getElementById("sidebar").style.width = "0";
        document.getElementById("content").style.marginLeft = "0";
    }
}

