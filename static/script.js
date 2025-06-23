function fetchLogs() {
    fetch('/logs')
        .then(res => res.json())
        .then(data => {
            const buyDiv = document.getElementById("buyLogs");
            const sellDiv = document.getElementById("sellLogs");

            buyDiv.innerHTML = "";
            sellDiv.innerHTML = "";

            data.buy.forEach(line => {
                const p = document.createElement('p');
                p.textContent = line;
                buyDiv.appendChild(p);
            });

            data.sell.forEach(line => {
                const p = document.createElement('p');
                p.textContent = line;
                sellDiv.appendChild(p);
            });
        });
}

setInterval(fetchLogs, 5000);
window.onload = fetchLogs;
