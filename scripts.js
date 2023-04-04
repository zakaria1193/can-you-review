
const projectSelector = document.getElementById('project-selector');
const singleReviewImage = document.getElementById('single-review-image');
const multipleReviewImage = document.getElementById('multiple-review-image');

function updateProjectList(projects) {
    projects.sort(); // Sort project names alphabetically

    // Remove "all" from project names if it exists
    const allIndex = projects.indexOf('all');
    if (allIndex !== -1) {
        projects.splice(allIndex, 1);
    }

    // Add the "All" option as the default selection
    const allOption = document.createElement('option');
    allOption.value = 'all';
    allOption.textContent = 'All projects';
    projectSelector.appendChild(allOption);

    // Add the sorted project names as options
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
    if (project === 'All') {
        singleReviewImage.src = './output/All_single_review_histogram.png';
        multipleReviewImage.src = './output/All_multiple_review_histogram.png';
    } else {
        singleReviewImage.src = `./output/${project}_single_review_histogram.png`;
        multipleReviewImage.src = `./output/${project}_multiple_review_histogram.png`;
    }
}

getProjectNames(); // Fetch project names and populate the selector
