async function convertCurrency() {
    let amount = document.getElementById("amount").value;
    let base = document.getElementById("base").value;
    let target = document.getElementById("target").value;

    if (amount === "" || amount <= 0) {
        alert("Masukkan jumlah yang valid!");
        return;
    }

    try {
        let response = await fetch("http://127.0.0.1:5000/convert", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                base: base,
                target: target,
                amount: parseFloat(amount)
            })
        });

        let data = await response.json();
        document.getElementById("result").value = data.converted_amount;
    } catch (error) {
        console.error("Error:", error);
        alert("Terjadi kesalahan saat mengonversi.");
    }
}
