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