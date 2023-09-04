// Init with empty data
var soleReviewData = {};
var multipleReviewData = {};

window.onload = function () {
  fetch("/get_data")
    .then((response) => response.json())
    .then((data) => {
      console.log("Data received:", data);
      soleReviewData = data.sole_review_data;
      multipleReviewData = data.multiple_review_data;

      updateCharts();

      // Hide the loading screen
      document.getElementById("loading-container").style.display = "none";

      // Show the content
      document.getElementById("content").style.display = "block";

      // Update the content with the fetched data
      // Example: updateProjectList(data.sole_review_data);
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
};

// the charts
var selectedProject = "all";

function updateCharts() {
  console.log("Updating charts");
  selectedProject = document.getElementById("projectSelector").value;

  createChart(
    soleReviewData,
    "soleReviewChart",
    "Review Count",
    selectedProject
  );
  createChart(
    multipleReviewData,
    "multipleReviewChart",
    "Multiple Review Count",
    selectedProject
  );
}

function createChart(data, id, label, selectedProject) {
  let chartStatus = Chart.getChart(id); // <canvas> id
  if (chartStatus != undefined) {
    chartStatus.destroy();
  }

  // If data is empty, print a message
  if (Object.keys(data).length === 0) {
    var ctx = document.getElementById("content");
    ctx.innerHTML = "No reviewer data available";
    return;
  }

  var usernames = data.map((item) => item.username);
  var counts = data.map((item) => item[selectedProject]);

  console.log("Creating chart with id: " + id);

  // If the chart already exists, destroy it
  if (document.getElementById(id).__chartjs) {
    document.getElementById(id).__chartjs.destroy();
  }

  var ctx = document.getElementById(id);
  var chart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: usernames,
      datasets: [
        {
          label: label,
          data: counts,
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          borderColor: "rgba(75, 192, 192, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
}

function setClickEvent(id) {
  const canvas = document.getElementById(id);
  const ctx = canvas.getContext("2d");

  // Make sure to attach `onclick` to the canvas, **not** the chart instance
  canvas.onclick = (evt) => {
    // Get chart instance from the canvas

    const chart = Chart.getChart(id);

    const res = chart.getElementsAtEventForMode(
      evt,
      "nearest",
      { intersect: true },
      true
    );
    // If didn't click on a bar, `res` will be an empty array
    if (res.length === 0) {
      return;
    }
    // Alerts "You clicked on A" if you click the "A" chart
    console.log("You clicked on " + chart.data.labels[res[0].index]);
    open_gitlab_review_page(chart.data.labels[res[0].index]);
  };

  function open_gitlab_review_page(username) {
    // Get url from /get_user_reviews_url
    fetch("/get_user_reviews_url?username=" + username)
      .then((response) => response.json())

      // Open the url in a new tab
      .then((data) => {
        window.open(data.url, "_blank");
      });
  }
}

// Set click event for the charts
setClickEvent("soleReviewChart");
setClickEvent("multipleReviewChart");
