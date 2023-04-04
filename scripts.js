
const projectSelector = document.getElementById('project-selector');
const soleReviewImage = document.getElementById('sole-review-image');
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
            const soleReviewFiles = files.filter((file) => file.endsWith('_sole_review_histogram.png'));
            const projectNames = soleReviewFiles.map((file) => file.replace('_sole_review_histogram.png', ''));
            updateProjectList(projectNames);
        });
}

function updateProject() {
    const project = projectSelector.value;
    if (project === 'All') {
        soleReviewImage.src = './output/All_sole_review_histogram.png';
        multipleReviewImage.src = './output/All_multiple_review_histogram.png';
    } else {
        soleReviewImage.src = `./output/${project}_sole_review_histogram.png`;
        multipleReviewImage.src = `./output/${project}_multiple_review_histogram.png`;
    }
}

getProjectNames(); // Fetch project names and populate the selector
