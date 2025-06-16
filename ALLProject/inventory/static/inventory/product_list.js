function show_product(_product_id){
    fetch(`/inventory/product_info/${_product_id}`, {
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("right-section").innerHTML = html;
    });
}

function add_product(){
    fetch(`/inventory/product_create`, {
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("right-section").innerHTML = html;
    });
}

function edit_product(_product_id){
    fetch(`/inventory/product_update/${_product_id}`, {
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("right-section").innerHTML = html;
    });
}

function delete_product(_product_id){
    fetch(`/inventory/product_delete/${_product_id}`, {
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("right-section").innerHTML = html;
    });
}

function filter_products(){
    const category = document.getElementById("category-filter").value;
    const availability = document.getElementById("availability-filter").value;

    fetch(`/inventory/product_list_partial/?category=${category}&availability=${availability}`, {
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("product-list-container").innerHTML = html;
    });
}