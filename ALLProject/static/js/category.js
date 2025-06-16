// function refresh_table(_category_id){

//     fetch(`/inventory/category_partial/?category_id=${_category_id}`, {
//     })
//     .then(response => response.text())
//     .then(html => {
//         document.getElementById("product-table-body").innerHTML = html;
//     });
// }

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