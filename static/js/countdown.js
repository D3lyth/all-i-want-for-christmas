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