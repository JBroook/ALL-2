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
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("select-history-box").innerHTML = html;
    });
}