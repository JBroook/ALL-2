const { stringify } = require("querystring");

function refresh_users(_role){
    fetch(`/users/user_list_partial/?role=${_role}`, {
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("user-list").innerHTML = html;
    });
}

function search_users(){
    const input_value = document.getElementById("searchbar").value;
    
    fetch(`/users/user_list_search/?input=${input_value}`, {
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("user-list").innerHTML = html;
    });
}

function add_user(){
    fetch(`/users/user_create_form`, {
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("userinfo-box").innerHTML = html;
    });
}

function edit_user(_employee_id){
    fetch(`/users/user_edit_form/`+_employee_id, {
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("userinfo-box").innerHTML = html;
    });
}

function show_user(_employee_id){
    fetch(`/users/user_info/`+_employee_id, {
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("userinfo-box").innerHTML = html;
    });
}

function delete_user(_employee_id){
    fetch(`/users/user_delete/`+_employee_id, {
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("userinfo-box").innerHTML = html;
    });
}

