
/* jshint esversion: 11 */

/*
    vanilla JavaScript for MaterializeCSS initialization
*/

document.addEventListener('DOMContentLoaded', function () {
    let sidenavs = document.querySelectorAll(".sidenav");
    let sidenavsInstance = M.Sidenav.init(sidenavs, { edge: "right" });
    let collapsibles = document.querySelectorAll(".collapsible");
    let collapsiblesInstance = M.Collapsible.init(collapsibles);
    let tooltips = document.querySelectorAll(".tooltipped");
    let tooltipsInstance = M.Tooltip.init(tooltips);
    let selects = document.querySelectorAll("select");
    let selectsInstance = M.FormSelect.init(selects);
});


document.addEventListener("DOMContentLoaded", function () {
    // Add event listeners for "GOT IT!" buttons
    const markAsBoughtButtons = document.querySelectorAll(".btn-small.light-green");
    markAsBoughtButtons.forEach(button => {
        button.addEventListener("click", function () {
            markAsBought(this); // Call the markAsBought function when clicked
        });
    });
});


// Modal event Listeners

document.addEventListener('DOMContentLoaded', function () {
    let modals = document.querySelectorAll('.modal');
    M.Modal.init(modals);
});

