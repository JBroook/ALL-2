document.addEventListener('DOMContentLoaded', function() {
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
});

function changePayment(id) {
    const cashButtons = document.getElementsByClassName('cashBttn');
    const cardButtons = document.getElementsByClassName('cardBttn');

    if (id === 'cashBttn') {
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
    }
}