let sort_order = {
    name: true,
    products: true,
    total_stock: true,
    average_price: true
};

function sort_category(sort_method){
    sort_order[sort_method] = !sort_order[sort_method];
    sort_method = (sort_order[sort_method] ? "" : "-")+sort_method
    fetch(`/inventory/category_partial/?sort=${sort_method}`, {
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("product-table-body").innerHTML = html;
    });
}

function add_category(){
    fetch(`/inventory/category_form`, {
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("crud-column").innerHTML = html;
    });
}

function view_category(_category_id){
    fetch(`/inventory/category_specific/` + _category_id, {
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("crud-column").innerHTML = html;
    });
}

function delete_category(_category_id){
    fetch(`/inventory/category_delete/` + _category_id, {
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("crud-column").innerHTML = html;
    });
}

function edit_category(_category_id){
    fetch(`/inventory/category_edit/` + _category_id, {
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("crud-column").innerHTML = html;
    });
}