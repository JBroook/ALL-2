function refresh_numbers(_quantity){
    const unitsInput = document.getElementById('id_units');
    const unitCostInput = document.getElementById('id_cpu');
    const totalCostDisplay = document.getElementById('h3-total');
    const newStock = document.getElementById('h3-quantity')

    const units = parseFloat(unitsInput.value) || 0;
    const unitCost = parseFloat(unitCostInput.value) || 0;
    const total = units * unitCost;
    totalCostDisplay.textContent = "RM"+(total.toFixed(2)).toString();
    newStock.textContent = (_quantity+units).toString();
}

function refresh_history(_asc, _product_id){
    const newOrder = _asc ? "desc" : "asc"

    fetch(`/inventory/restock_order/?order=${newOrder}&product_id=${_product_id}`, {
            headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-Custom-Partial-Request': 'true'
        }
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("select-history-box").innerHTML = html;
    });
}

function changeToQR() {
    console.log("Change to QR code")
    qr = document.getElementById('qr-bttn')
    qr_img = document.getElementById('qrCode')
    bar = document.getElementById('barcode-bttn')
    bar_img = document.getElementById('barCode')

    // Buttons
    qr.style.background = 'rgba(205, 231, 161, 0.5)';
    qr.style.color = 'black';
    bar.style.background = 'transparent';
    bar.style.color = 'grey';

    // Image
    qr_img.style.visibility = 'visible';
    bar_img.style.visibility = 'hidden';
}
function changeToBar() {
    console.log("Change Barcode")
    qr = document.getElementById('qr-bttn')
    qr_img = document.getElementById('qrCode')
    bar = document.getElementById('barcode-bttn')
    bar_img = document.getElementById('barCode')

    // Buttons
    bar.style.background = 'rgba(205, 231, 161, 0.5)';
    bar.style.color = 'black';
    qr.style.background = 'transparent';
    qr.style.color = 'grey';

    // Image
    bar_img.style.visibility = 'visible';
    qr_img.style.visibility = 'hidden';
}