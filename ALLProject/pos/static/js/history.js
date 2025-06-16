function filter_by_date(type){
  fetch(`/pos/history_partial/selection/?specific=${type}`, {
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("history-list").innerHTML = html;
    });

    if (type=="today"){
      type = 'Today'
    }else if (type=="week"){
      type = 'Last 7 Days'
    }else if (type=="month"){
      type = 'Last Month'
    }

    document.getElementById('date-filter-title').innerText = type
}

function is_date(d) {
  return d instanceof Date && !isNaN(d);
}

function filter_custom_date(start_date, end_date){
  const processed_start_date = new Date(start_date)
  const processed_end_date = new Date(end_date)
  if (is_date(processed_start_date) && is_date(processed_end_date)){
    console.log("Valid dates")

    fetch(`/pos/history_partial/custom/?start=${start_date}&end=${end_date}`, {
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("history-list").innerHTML = html;
    });

    document.getElementById('date-filter-title').innerText = start_date + ' - ' + end_date

  }else console.log("Invalid dates")
}

function filter_payment(type){
  fetch(`/pos/history_partial/payment/?specific=${type}`, {
    })  
    .then(response => response.text())
    .then(html => {
        document.getElementById("history-list").innerHTML = html;
    });
}

window.addEventListener("DOMContentLoaded", (event) => {
  document.getElementById("date-filter-selection")?.addEventListener("click", function () {
        document.querySelector(".filter-date-box").classList.toggle("visible");
    });

  document.getElementById("payment-filter-selection")?.addEventListener("click", function () {
        document.querySelector(".filter-payment-box").classList.toggle("visible");
    });

  const start_date = document.getElementById("start-date")
  const end_date = document.getElementById("end-date")

  start_date?.addEventListener("input", function (){
    filter_custom_date(start_date.value, end_date.value)
  });

  end_date?.addEventListener("input", function (){
    filter_custom_date(start_date.value, end_date.value)
  });
});
