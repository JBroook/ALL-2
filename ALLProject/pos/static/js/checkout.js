document.addEventListener('DOMContentLoaded', function() {
    const cashButton = document.getElementById('doneCash-Payment');
    const cardButton = document.getElementById('doneCard-Payment');
    const paymentMethodInput = document.getElementById('paymentMethod');
    const cashInput = document.getElementById('cash-paid');
    const cardInputs = [
        document.getElementById('cardNo'),
        document.getElementById('cardExp'),
        document.getElementById('cardCVV')
    ];

    // Show payment-box cash when Check-Out button is clicked
    document.getElementById('checkOutBttn').addEventListener('click', function() {
        document.querySelector('.dimmer').style.visibility = 'visible';
        document.querySelector('.payment-box.cash').style.visibility = 'visible';
        // Reset button styles
        changePayment('cashBttn');
    });

    // Close payment box when close button is clicked
    document.querySelectorAll('#close-box').forEach(button => {
        button.addEventListener('click', function() {
            document.querySelector('.dimmer').style.visibility = 'hidden';
            document.querySelector('.payment-box.cash').style.visibility = 'hidden';
            document.querySelector('.payment-box.card').style.visibility = 'hidden';
        });
    });

    if (cashButton && cardButton && paymentMethodInput) {
        cashButton.addEventListener('click', function(){
            paymentMethodInput.value  = cashButton.getAttribute('data-payment');
            console.log('Payment method set to: ',paymentMethodInput.value);
            if (paymentMethod == 'cash'){
                paymentMethodInput.value = 'Cash';
            }
            document.getElementById('checkout_form').submit();
        });
        
        cardButton.addEventListener('click', function(){
            paymentMethodInput.value  = cardButton.getAttribute('data-payment');
            console.log('Payment method set to: ',paymentMethodInput.value);
            document.getElementById('checkout_form').submit();
        });
    } else {
        console.error('Check Out Form Element Not Found.')
    }
    
    // For TouchScreen Keyboard Inputs (Cash)
    document.querySelectorAll('.payment-box.cash .keyboard-cash').forEach(button => {
        button.addEventListener('click', function() {

            if (button.classList.contains('clear')){
                cashInput.value = '';
            } else if (button.classList.contains('decimal')) {
                if (!cashInput.value.includes('.')) {
                    cashInput.value += button.value;
                    dp = 0
                    console.log("decimal place: ",dp);
                }
            } else {
                cashInput.value += button.value;
            }
            updateChange();
        });
    });
    
    // For TouchScreen Keyboard Inputs (Card)
    let activeCardInput = 0;
    cardInputs[0].focus();

    document.querySelectorAll('.payment-box.card .keyboard-card').forEach(button => {
        button.addEventListener('click', function() {
            const activeInput = cardInputs[activeCardInput];
            if (button.classList.contains('clear')){
                cardInputs.forEach(input => input.value = '');
                activeCardInput = 0;
                cardInputs[0].focus();

            } else if (button.classList.contains('back')) {
                activeInput.value = activeInput.value.slice(0,-1);
                if (activeInput.value == ''){
                    activeCardInput -= 1;
                    activeInput.value = activeInput.value.slice(0,-1);
                }

            } else {
                if (activeCardInput == 1 && activeInput.value.length == 2){
                        activeInput.value += "/";
                    };
                if (activeInput.value.length < activeInput.maxLength) {
                    activeInput.value += button.value;

                    if (activeInput.value.length == activeInput.maxLength && 
                        activeCardInput < cardInputs.length-1){
                            activeCardInput += 1;
                            cardInputs[activeCardInput].focus();
                    };
                };
            };
        });
    });

    // Update change due for cash payment
    function updateChange(){
        const paid = parseFloat(cashInput.value) || 0;
        const change = paid - cartCost;
        changeAmount.textContent = 'RM ' , change.toFixed(2);
    }

    window.changePayment = function(id) {
        const cashButtons = document.getElementsByClassName('cashBttn');
        const cardButtons = document.getElementsByClassName('cardBttn');

        if (id === 'cashBttn') {
            cashInput.value = '';
            // Update all cash buttons
            Array.from(cashButtons).forEach(button => {
                button.style.background = '#815355';
                button.style.color = '#FFF';
            });
            // Update all card buttons
            Array.from(cardButtons).forEach(button => {
                button.style.background = '#D9D9D9';
                button.style.color = '#595959';
            });
            // Show cash payment box, hide card payment box
            document.querySelector('.payment-box.cash').style.visibility = 'visible';
            document.querySelector('.payment-box.card').style.visibility = 'hidden';
           
        } else if (id === 'cardBttn') {
            cardInputs.forEach(input => input.value = '');
            activeCardInput = 0;
            cardInputs[0].focus;

            // Update all cash buttons
            Array.from(cashButtons).forEach(button => {
                button.style.background = '#D9D9D9';
                button.style.color = '#595959';
            });
            // Update all card buttons
            Array.from(cardButtons).forEach(button => {
                button.style.background = '#815355';
                button.style.color = '#FFF';
            });
            // Show card payment box, hide cash payment box
            document.querySelector('.payment-box.cash').style.visibility = 'hidden';
            document.querySelector('.payment-box.card').style.visibility = 'visible';
        };
    }
});
