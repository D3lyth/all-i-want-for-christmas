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
    // Initialize the modal
    let modal = document.getElementById('confirmUndo');

    // Open the modal when the "Undo" button is clicked
    let undoButtons = document.getElementsByClassName('undo-gift-button');
    Array.from(undoButtons).forEach(function (button) {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            let giftId = button.getAttribute('data-gift-id');
            let modalConfirm = document.querySelector('#confirmUndo .modal-confirm');
            modalConfirm.setAttribute('form', 'form-' + giftId);
            M.Modal.getInstance(modal).open();
        });
    });

    // Close the modal when the "Cancel" button is clicked
    let modalCancel = document.querySelector('#confirmUndo .modal-close');
    modalCancel.addEventListener('click', function () {
        M.Modal.getInstance(modal).close();
    });
});
