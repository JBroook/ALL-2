function refresh_table(_category_id){

    fetch(`/inventory/product_table_partial/?category_id=${_category_id}`, {
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("product-table-body").innerHTML = html;
    });
}
