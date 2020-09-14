// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
var ctx = document.getElementById("myPieChart");
var a=document.getElementById("sum_adm").innerHTML;
var b=document.getElementById("sum_call").innerHTML;
var c=document.getElementById("sum_can").innerHTML;

var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ["Admitted", "Call Back","Cancel"],
    datasets: [{
      data: [a, b, c,],
      backgroundColor: ['#1cc88a', '#36b9cc', '#f6c23e'],
      hoverBackgroundColor: ['#17a673', '#2c9faf', '#dea514'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});
