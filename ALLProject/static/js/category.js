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
            headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-Custom-Partial-Request': 'true'
        }
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("product-table-body").innerHTML = html;
    });
}

function add_category(){
    fetch(`/inventory/category_form`, {
            headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-Custom-Partial-Request': 'true'
        }
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("crud-column").innerHTML = html;
    });
}

function view_category(_category_id){
    console.log("from-category-"+toString(_category_id))
    const products = document.getElementsByClassName("from-category-"+_category_id);
    const category = document.getElementById("category-"+_category_id);
    for (let i = 0; i < products.length; i++) {
        if(products[i].style.display!='table-row'){
            products[i].style.display = 'table-row';
            category.style['background-color'] = '#C3B299' ;
        }else{
            products[i].style.display = 'none';
            category.style['background-color'] = 'transparent' ;
        }
    }

    fetch(`/inventory/category_specific/` + _category_id, {
            headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-Custom-Partial-Request': 'true'
        }
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("crud-column").innerHTML = html;
    });
}

function delete_category(_category_id){
    fetch(`/inventory/category_delete/` + _category_id, {
            headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-Custom-Partial-Request': 'true'
        }
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("crud-column").innerHTML = html;
    });
}

function edit_category(_category_id){
    fetch(`/inventory/category_edit/` + _category_id, {
            headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-Custom-Partial-Request': 'true'
        }
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("crud-column").innerHTML = html;
    });
}