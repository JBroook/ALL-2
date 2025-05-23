
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