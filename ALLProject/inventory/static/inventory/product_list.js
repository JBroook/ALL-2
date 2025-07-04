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

let select_mode = false;
function select_products() {
    if (!select_mode){
        const category = document.getElementById("category-filter").value;
        const availability = document.getElementById("availability-filter").value;
        const text = document.getElementById("text-search").value;

        fetch(`/inventory/product_select_partial/?category=${category}&availability=${availability}&text=${text}`, {
        })  
        .then(response => response.text())
        .then(html => {
            document.getElementById("product-list-container").innerHTML = html;
        });

        fetch(`/inventory/product_select_list`, {
        })  
        .then(response => response.text())
        .then(html => {
            document.getElementById("right-section").innerHTML = html;
        });

        select_mode = true;
    }else{
        window.location.href = `/inventory/product_list`
        select_mode = false;
    }
}

let select_count = 0;
let select_list = [];

function select_product(_product_id){
    const product_select = document.getElementById("product-select-"+_product_id);
    const product_select_border = document.getElementById("product-icon-"+_product_id);
    const product_select_count = document.getElementById("select-count");
    const list = document.getElementById("select-list")

    if (product_select.style['display']!='block'){
        product_select.style['display'] = 'block'
        product_select_border.style['display'] = 'none'
        select_count ++;

        select_list.push(_product_id)

        fetch(`/inventory/product_info_json/${_product_id}`, {})
        .then(
            response => response.json()
        ).then(
            r => {
                console.log(r['name'])
                const addition = document.createElement('li')
                addition.id = "addition-"+_product_id
                addition.innerText = r['name']+" selected";
                list.appendChild(addition)
            }
        );
    }else{
        product_select.style['display'] = 'none'
        product_select_border.style['display'] = 'block'
        select_count--;

        document.getElementById('addition-'+_product_id).remove();

        select_list.splice(select_list.indexOf(_product_id),1)
    }

    console.log(select_list)

    product_select_count.innerText = select_count +" Products Selected"
}

function force_select_product(_product_id, mode){
    const product_select = document.getElementById("product-select-"+_product_id);
    const product_select_border = document.getElementById("product-icon-"+_product_id);
    const product_select_count = document.getElementById("select-count");
    const list = document.getElementById("select-list")

    if (mode){
        if (product_select.style['display']!='block'){
            product_select.style['display'] = 'block'
            product_select_border.style['display'] = 'none'
            select_count ++;

            select_list.push(_product_id)

            fetch(`/inventory/product_info_json/${_product_id}`, {})
            .then(
                response => response.json()
            ).then(
                r => {
                    const addition = document.createElement('li')
                    addition.id = "addition-"+_product_id
                    addition.innerText = r['name']+" selected";
                    list.appendChild(addition)
                }
            );
        }
    }else{
        if (product_select.style['display']=='block'){
            product_select.style['display'] = 'none'
            product_select_border.style['display'] = 'block'
            select_count--;

            document.getElementById('addition-'+_product_id).remove();

            select_list.splice(select_list.indexOf(_product_id),1)
        }
    }
}

let selected_all = false;
function select_all(){
    const products = document.getElementsByClassName("product");
    select_list = [];
    for (let i=0;i<products.length;i++){
        const product_id = products[i].id;
        force_select_product(product_id, !selected_all)
    }

    select_count = selected_all ? 0: products.length;

    const select_label = document.getElementById('select-all-button')
    if(!selected_all){
        select_label.innerText = "Deselect All";
    }else{
        select_label.innerText = "Select All";
    }
    selected_all = !selected_all;
}

function print_selected(){
    if(select_count>0){
        window.location.href = `/inventory/product_print_selected/?ids=${ select_list.join(',') }`;
    }
}

function delete_selected(){
    if(select_count>0){
        fetch(`/inventory/product_delete_selected/?ids=${ select_list.join(',') }`, {
        })
        .then(response => response.text())
        .then(html => {
            document.getElementById("right-section").innerHTML = html;
        });
    }
}