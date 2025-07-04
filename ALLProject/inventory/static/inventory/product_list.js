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
    const text = document.getElementById("text-search").value;

    fetch(`/inventory/product_list_partial/?category=${category}&availability=${availability}&text=${text}`, {
    })  
    .then(response => response.text())
    .then(html => {
        document.getElementById("product-list-container").innerHTML = html;
    });
}

function changeToQR() {
    console.log("Change to QR code")
    qr = document.getElementById('change-qr')
    qr_img = document.getElementById('qr-image')
    bar = document.getElementById('change-bar')
    bar_img = document.getElementById('barcode-image')

    // Buttons
    qr.style.background = '#523249';
    qr.style.color = 'white';
    bar.style.background = 'transparent';
    bar.style.color = 'black';

    // Image
    qr_img.style.visibility = 'visible';
    bar_img.style.visibility = 'hidden';
}
function changeToBar() {
    console.log("Change Barcode")
    qr = document.getElementById('change-qr')
    qr_img = document.getElementById('qr-image')
    bar = document.getElementById('change-bar')
    bar_img = document.getElementById('barcode-image')

    // Buttons
    bar.style.background = '#523249';
    bar.style.color = 'white';
    qr.style.background = 'transparent';
    qr.style.color = 'black';

    // Image
    bar_img.style.visibility = 'visible';
    qr_img.style.visibility = 'hidden';
}