function fetchLogs() {
    fetch('/logs')
        .then(res => res.json())
        .then(data => {
            // Old Buy / Sell / ADX Buy sections: disabled, kept for reference
            // const buyDiv = document.getElementById("buyLogs");
            // const sellDiv = document.getElementById("sellLogs");
            // const adxBuyDiv = document.getElementById("adxBuyLogs");
            const aayushiBuyDiv = document.getElementById("aayushiBuyLogs");
            const aayushiSellDiv = document.getElementById("aayushiSellLogs");

            // buyDiv.innerHTML = "";
            // sellDiv.innerHTML = "";
            // adxBuyDiv.innerHTML = "";
            aayushiBuyDiv.innerHTML = "";
            aayushiSellDiv.innerHTML = "";

            // data.buy.forEach(line => {
            //     const p = document.createElement('p');
            //     p.textContent = line;
            //     buyDiv.appendChild(p);
            // });

            // data.sell.forEach(line => {
            //     const p = document.createElement('p');
            //     p.textContent = line;
            //     sellDiv.appendChild(p);
            // });

            // data.adx_buy.forEach(line => {
            //     const p = document.createElement('p');
            //     p.textContent = line;
            //     adxBuyDiv.appendChild(p);
            // });

            data.aayushi_buy.forEach(line => {
                const p = document.createElement('p');
                p.textContent = line;
                aayushiBuyDiv.appendChild(p);
            });

            data.aayushi_sell.forEach(line => {
                const p = document.createElement('p');
                p.textContent = line;
                aayushiSellDiv.appendChild(p);
            });
        });
}

setInterval(fetchLogs, 5000);
window.onload = fetchLogs;
