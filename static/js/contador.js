const birthday = DateTime.local(2021, 6, 24);
let updateClockIntervalId;

function updateClock() {
    const distance = birthday.diffNow();
    const countdownElement = document.getElementById("countdown");

    countdownElement.innerText = distance.toFormat("d 'dias' h 'horas' m 'minutos' s 'segundos'");

    //do something later when date is reached
    if (distance < 0) {
        document.getElementById("headline").innerText = "It's my birthday!";
        countdownElement.style.display = "none";
        document.getElementById("content").style.display = "block";

        clearInterval(updateClockIntervalId);
    }
}

updateClockIntervalId = setInterval(updateClock, 1000);
updateClock();
