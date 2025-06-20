function fetchLogs() {
    fetch('/logs')
        .then(res => res.json())
        .then(data => {
            const logBox = document.getElementById("logBox");
            logBox.innerHTML = '';
            data.forEach(line => {
                const p = document.createElement('p');
                p.textContent = line.trim();
                logBox.appendChild(p);
            });
        });
}

setInterval(fetchLogs, 5000); // every 5 sec
window.onload = fetchLogs;
