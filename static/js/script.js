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

// Countdown Timer

function updateCountdown() {
    // Calculate the time remaining until Christmas
    let now = new Date();
    let christmas = new Date(now.getFullYear(), 11, 25); // December is 11 (0-based index)

    // Check if Christmas has already passed this year
    if (now > christmas) {
        christmas.setFullYear(now.getFullYear() + 1);
    }

    let timeUntilChristmas = christmas - now;

    // Convert the time remaining to days, hours, minutes, and seconds
    let days = Math.floor(timeUntilChristmas / (1000 * 60 * 60 * 24));
    let hours = Math.floor((timeUntilChristmas % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    let minutes = Math.floor((timeUntilChristmas % (1000 * 60 * 60)) / (1000 * 60));
    let seconds = Math.floor((timeUntilChristmas % (1000 * 60)) / 1000);

    // Update the countdown element with the calculated time
    document.getElementById("countdown").innerHTML = days + "d " + hours + "h " + minutes + "m " + seconds + "s";
}

// Update the countdown every second
setInterval(updateCountdown, 1000);

updateCountdown();


// Function to fetch and display the running total
function updateRunningTotal() {
    fetch('/get_running_total')  // Replace with the appropriate Flask route
        .then(response => response.json())
        .then(data => {
            document.getElementById('running-total').textContent = `Total: $${data.total}`;
        })
        .catch(error => console.error('Error:', error));
}

// Call the function to update the running total when the page loads
window.addEventListener('load', updateRunningTotal);