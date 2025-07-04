function call_manager(){
    const button = document.getElementById("call-manager-button")
    button.disabled = true;
    button.textContent = "Manager Called";

    fetch('/pos/call_manager/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);

        setTimeout(() => {
            button.disabled = false;
            button.textContent = "Call Manager";
        }, 60000);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to call manager.');
        button.disabled = false;
        button.textContent = "Call Manager";
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}