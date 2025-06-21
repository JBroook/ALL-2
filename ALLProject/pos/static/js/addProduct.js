document.addEventListener('DOMContentLoaded', function() {
    const closeaddItem = document.getElementById('close-addItem')
    const closequantity = document.getElementById('close-quantity')
    // Show product-detail-box cash when Enter Code button is clicked
    document.getElementById('enterCode').addEventListener('click', function() {
        document.querySelector('.details-box.default').style.visibility = 'hidden';            
        document.querySelector('.details-box.addItem').style.visibility = 'visible';
        document.querySelector('.details-box.quantity').style.visibility = 'hidden';
    });

    // Handle Close Button
    if (closeaddItem) {
        closeaddItem.addEventListener('click', function (){
            resetDefault();
            console.log("Closed additem");
        });
    }
    if (closequantity) {
        closequantity.addEventListener('click', function(){
            resetDefault();
            console.log("Closed quantity");
        });
    }

    //enter item code
    document.querySelectorAll('.keyboard.keyboard-cart').forEach(button => {
        button.addEventListener('click', function() {
            const parent_code_box = document.getElementById('add-item-box')
            const code_input = document.getElementById('itemCode')
            const parent_quantity_box = document.getElementById('quantity-item-box')
            const quantity_input = document.getElementById('quantity-input')

            console.log(parent_quantity_box.style.visibility)

            if (parent_code_box.style.visibility=='visible'){
                code_input.value = code_input.value+button.value
                console.log("Code input:", button.value)
            }else if(parent_quantity_box.style.visibility=='visible'){
                quantity_input.value = quantity_input.value+button.value
                console.log("Quantity input:", button.value)
            }else{
                console.log("no dice")
            }
        });
    });
});

function resetDefault(){
        document.querySelector('.details-box.default').style.visibility = 'visible'; 
        document.querySelector('.details-box.addItem').style.visibility = 'hidden';  
        document.querySelector('.details-box.quantity').style.visibility = 'hidden';
        document.getElementById('itemCode').value="";
        document.getElementById('quantity').value='';
}

function enterPin() {
    document.addEventListener('DOMContentLoaded',function(){
        var textbox = document.querySelectorAll('.userPinInput');
        var keyboardBttns = document.querySelectorAll('.keyboard');

        keyboardBttns.forEach(function(keyboard) {
            keyboard.addEventListener("click",function() {
                textbox.value += this.value;
            });
        });
    });
}

let successful_scan = false;
let successive_scans = 0;

function onScanSuccess(decodedText, decodedResult) {
  // handle the scanned code as you like, for example:
    successive_scans++;
    if(successive_scans>=5){
        if (!successful_scan){
            successful_scan = true;

            console.log("One success")
            console.log(`Code matched = ${decodedText}`, decodedResult);
        }
    }
}

function onScanFailure(error) {
  // handle scan failure, usually better to ignore and keep scanning.
  // for example:
//   console.warn(`Code scan error = ${error}`);
    successful_scan = false;
    successive_scans = 0;
}

let html5QrcodeScanner = new Html5QrcodeScanner(
  "reader",
  { fps: 30, qrbox: {width: 250, height: 250} },
  /* verbose= */ false);
html5QrcodeScanner.render(onScanSuccess, onScanFailure);

function show_scanner(show){
    document.getElementById('scanner-div').style.visibility = (show ? "visible" : "hidden")
}