/*
    jQuery for MaterializeCSS initialization
*/

$(document).ready(function () {
    $(".sidenav").sidenav({ edge: "right" });
    $(".collapsible").collapsible();
    $(".tooltipped").tooltip();
    $("select").formSelect();
});

validateMaterializeSelect();
function validateMaterializeSelect() {
    let classValid = { "border-bottom": "1px solid #4caf50", "box-shadow": "0 1px 0 0 #4caf50" };
    let classInvalid = { "border-bottom": "1px solid #f44336", "box-shadow": "0 1px 0 0 #f44336" };
    if ($("select.validate").prop("required")) {
        $("select.validate").css({ "display": "block", "height": "0", "padding": "0", "width": "0", "position": "absolute" });
    }
    $(".select-wrapper input.select-dropdown").on("focusin", function () {
        $(this).parent(".select-wrapper").on("change", function () {
            if ($(this).children("ul").children("li.selected:not(.disabled)").on("click", function () { })) {
                $(this).children("input").css(classValid);
            }
        });
    }).on("click", function () {
        if ($(this).parent(".select-wrapper").children("ul").children("li.selected:not(.disabled)").css("background-color") === "rgba(0, 0, 0, 0.03)") {
            $(this).parent(".select-wrapper").children("input").css(classValid);
        } else {
            $(".select-wrapper input.select-dropdown").on("focusout", function () {
                if ($(this).parent(".select-wrapper").children("select").prop("required")) {
                    if ($(this).css("border-bottom") != "1px solid rgb(76, 175, 80)") {
                        $(this).parent(".select-wrapper").children("input").css(classInvalid);
                    }
                }
            });
        }
    });
};





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

// JavaScript function to hide the clicked gift item
function markAsBought(button) {
    const giftId = button.getAttribute('data-giftid'); // Get the gift ID from the button
    const giftItem = document.querySelector(`li[data-giftid="${giftId}"]`); // Find the corresponding gift item

    if (giftItem) {
        giftItem.style.display = 'none'; // Hide the gift item
    }
}

document.addEventListener("DOMContentLoaded", function () {
    // Add event listeners for "GOT IT!" buttons
    const markAsBoughtButtons = document.querySelectorAll(".btn-small.light-green");
    markAsBoughtButtons.forEach(button => {
        button.addEventListener("click", function () {
            markAsBought(this); // Call the markAsBought function when clicked
        });
    });
});

// JavaScript code to hide the message when a gift is added
$(document).ready(function () {
    // Event listener to the "Add Gift" button in the modal
    $("#add-gift-button").on("click", function () {
        // Hide the message when a gift is added
        $("#no-gifts-message").hide();
    });
});



// Flash messages trigger

$(document).ready(function () {
    // Check for flash messages
    {% with messages = get_flashed_messages() %}
    {% if messages %}
    var flashMessage = "{{ messages[0] }}"; // Get the first flash message
    if (flashMessage) {
        // Display the modal and set the message content
        var modal = M.Modal.init(document.getElementById('flash-message-modal'));
        document.getElementById('flash-message-content').textContent = flashMessage;
        modal.open();
    }
    {% endif %}
    {% endwith %}
});
