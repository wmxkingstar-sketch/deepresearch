const timeElement = document.getElementById("time");
const dateElement = document.getElementById("date");
const timezoneElement = document.getElementById("timezone");
const offsetElement = document.getElementById("offset");
const progressElement = document.getElementById("progress");
const hourHand = document.getElementById("hour-hand");
const minuteHand = document.getElementById("minute-hand");
const secondHand = document.getElementById("second-hand");

const timeFormatter = new Intl.DateTimeFormat([], {
  hour: "2-digit",
  minute: "2-digit",
  second: "2-digit",
  hour12: false,
});

const dateFormatter = new Intl.DateTimeFormat([], {
  weekday: "long",
  month: "long",
  day: "numeric",
  year: "numeric",
});

function formatOffset(date) {
  const totalMinutes = -date.getTimezoneOffset();
  const sign = totalMinutes >= 0 ? "+" : "-";
  const absoluteMinutes = Math.abs(totalMinutes);
  const hours = String(Math.floor(absoluteMinutes / 60)).padStart(2, "0");
  const minutes = String(absoluteMinutes % 60).padStart(2, "0");
  return `UTC${sign}${hours}:${minutes}`;
}

function formatDayProgress(date) {
  const elapsedMilliseconds =
    date.getHours() * 3600000 +
    date.getMinutes() * 60000 +
    date.getSeconds() * 1000 +
    date.getMilliseconds();
  const progress = (elapsedMilliseconds / 86400000) * 100;
  return `${progress.toFixed(1)}%`;
}

function updateHands(date) {
  const seconds = date.getSeconds() + date.getMilliseconds() / 1000;
  const minutes = date.getMinutes() + seconds / 60;
  const hours = (date.getHours() % 12) + minutes / 60;

  hourHand.style.transform = `translateX(-50%) rotate(${hours * 30}deg)`;
  minuteHand.style.transform = `translateX(-50%) rotate(${minutes * 6}deg)`;
  secondHand.style.transform = `translateX(-50%) rotate(${seconds * 6}deg)`;
}

function updateClock() {
  const now = new Date();
  const timezoneName = Intl.DateTimeFormat().resolvedOptions().timeZone || "Local";

  timeElement.textContent = timeFormatter.format(now);
  dateElement.textContent = dateFormatter.format(now);
  timezoneElement.textContent = timezoneName;
  offsetElement.textContent = formatOffset(now);
  progressElement.textContent = formatDayProgress(now);
  document.title = `${timeFormatter.format(now)} | Realtime Studio Clock`;

  updateHands(now);
}

updateClock();
setInterval(updateClock, 100);
