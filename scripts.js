const projectSelector = document.getElementById('project-selector');
const singleReviewImage = document.getElementById('single-review-image');
const multipleReviewImage = document.getElementById('multiple-review-image');

function updateProjectList(projects) {
    projects.forEach((project) => {
        const option = document.createElement('option');
        option.value = project;
        option.textContent = project;
        projectSelector.appendChild(option);
    });

    updateProject(); // Load the initial project images
}

function getProjectNames() {
    fetch('./output/index.json')
        .then((response) => response.json())
        .then((files) => {
            const singleReviewFiles = files.filter((file) => file.endsWith('_single_review_histogram.png'));
            const projectNames = singleReviewFiles.map((file) => file.replace('_single_review_histogram.png', ''));
            updateProjectList(projectNames);
        });
}

function updateProject() {
    const project = projectSelector.value;
    singleReviewImage.src = `./output/${project}_single_review_histogram.png`;
    multipleReviewImage.src = `./output/${project}_multiple_review_histogram.png`;
}

getProjectNames(); // Fetch project names and populate the selector

