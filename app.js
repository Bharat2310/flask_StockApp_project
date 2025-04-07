document.addEventListener("DOMContentLoaded", function () {
    const livePricesBody = document.getElementById("live-prices-body");
    const trendingStocksBody = document.getElementById("trending-stocks-body");

    livePricesBody.innerHTML = `<tr><td colspan="4">Loading live prices...</td></tr>`;
    trendingStocksBody.innerHTML = `<tr><td colspan="4">Loading trending stocks...</td></tr>`;

    fetch("/api/stocks")
        .then(res => {
            if (!res.ok) {
                throw new Error("Network response was not ok");
            }
            return res.json();
        })
        .then(data => {
            livePricesBody.innerHTML = "";
            trendingStocksBody.innerHTML = "";

            if (data.livePrices && data.livePrices.length > 0) {
                data.livePrices.forEach(stock => {
                    const row = `<tr>
                        <td>${stock.symbol}</td>
                        <td>${stock.lastPrice}</td>
                        <td>${stock.change}</td>
                        <td>${stock.pChange}%</td>
                    </tr>`;
                    livePricesBody.innerHTML += row;
                });
            } else {
                livePricesBody.innerHTML = `<tr><td colspan="4">No live prices available.</td></tr>`;
            }

            if (data.trendingStocks && data.trendingStocks.length > 0) {
                data.trendingStocks.forEach(stock => {
                    const row = `<tr>
                        <td>${stock.symbol}</td>
                        <td>${stock.lastPrice}</td>
                        <td>${stock.SMA_5}</td>
                        <td>${stock.SMA_10}</td>
                    </tr>`;
                    trendingStocksBody.innerHTML += row;
                });
            } else {
                trendingStocksBody.innerHTML = `<tr><td colspan="4">No trending stocks at the moment.</td></tr>`;
            }
        })
        .catch(err => {
            console.error("API Error:", err);
            livePricesBody.innerHTML = `<tr><td colspan="4">Failed to load live prices.</td></tr>`;
            trendingStocksBody.innerHTML = `<tr><td colspan="4">Failed to load trending stocks.</td></tr>`;
        });
});




