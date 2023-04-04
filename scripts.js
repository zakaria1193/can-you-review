const projectSelector = document.getElementById('project-selector');
const singleReviewImage = document.getElementById('single-review-image');
const multipleReviewImage = document.getElementById('multiple-review-image');

const projects = [
    // Add your project names here
    'magellan',
];

projects.forEach((project) => {
    const option = document.createElement('option');
    option.value = project;
    option.textContent = project;
    projectSelector.appendChild(option);
});

function updateProject() {
    const project = projectSelector.value;
    singleReviewImage.src = `./output/${project}_single_review_histogram.png`;
    multipleReviewImage.src = `./output/${project}_multiple_review_histogram.png`;
}

updateProject(); // Load the initial project images

