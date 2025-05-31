document.addEventListener('DOMContentLoaded', function() {
    const errorDisplay = document.getElementById('error-container');
    const successDisplay = document.getElementById('success-container');

    // Success Pop-Up
    if (successDisplay) {
        successDisplay.style.display = 'block';
        console.log('success pop-up displayed');

        if (document.getElementById('close-success')) {
            document.getElementById('close-success').addEventListener('click',function() {
                successDisplay.style.display = 'none';
                console.log('success pop-up closed via button');
            });
        } else {
            console.log('Close Button not Found');
        };

        if (document.querySelector('.dimmer-success')) {
            document.querySelector('.dimmer-success').addEventListener('click',function(){
                successDisplay.style.display = 'none';
                console.log('success pop-up closed via clicking outside box');
            });
        } else {
            console.log('Dimmer success not found')
        };
    } else {
        console.log('No success Container Found')
    };
    
    // Error Pop-Up
    if (errorDisplay) {
        errorDisplay.style.display = 'block';
        console.log('Error pop-up displayed');

        if (document.getElementById('close-error')) {
            document.getElementById('close-error').addEventListener('click',function() {
                errorDisplay.style.display = 'none';
                console.log('Error pop-up closed via button');
            });
        } else {
            console.log('Close Button not Found');
        };

        if (document.querySelector('.dimmer-error')) {
            document.querySelector('.dimmer-error').addEventListener('click',function(){
                errorDisplay.style.display = 'none';
                console.log('Error pop-up closed via clicking outside box');
            });
        } else {
            console.log('Dimmer error not found')
        };
    } else {
        console.log('No Error Container Found')
    };

});