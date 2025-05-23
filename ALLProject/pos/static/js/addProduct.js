document.addEventListener('DOMContentLoaded', function() {
    // Show product-detail-box cash when Enter Code button is clicked
    document.getElementById('enterCode').addEventListener('click', function() {
        document.querySelector('.details-box.default').style.visibility = 'hidden';            
        document.querySelector('.details-box.addItem').style.visibility = 'visible';
        document.querySelector('.details-box.quantity').style.visibility = 'hidden';
    });

    // Handle Close Button
    document.getElementByClassName('close-product-box').addEventListener('click', resetDefault) 
});

function resetDefault(){
        document.querySelector('.details-box.default').style.visibility = 'visible'; 
        document.querySelector('.details-box.addItem').style.visibility = 'hidden';  
        document.querySelector('.details-box.quantity').style.visibility = 'hidden';
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