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
    fetch(`/users/user_create`, {
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("userinfo-box").innerHTML = html;
    });
}