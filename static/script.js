function fetchLogs() {
    fetch('/logs')
        .then(res => res.json())
        .then(data => {
            const buyDiv = document.getElementById("buyLogs");
            const sellDiv = document.getElementById("sellLogs");
            const adxBuyDiv = document.getElementById("adxBuyLogs");

            buyDiv.innerHTML = "";
            sellDiv.innerHTML = "";
            adxBuyDiv.innerHTML = "";

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

            data.adx_buy.forEach(line => {
                const p = document.createElement('p');
                p.textContent = line;
                adxBuyDiv.appendChild(p);
            });
        });
}

setInterval(fetchLogs, 5000);
window.onload = fetchLogs;
