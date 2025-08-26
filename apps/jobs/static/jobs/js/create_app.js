document.addEventListener("DOMContentLoaded", function() {
    var collapseElement = document.getElementById('collapseExample');
    var arrowIcon = document.getElementById('arrowIcon');

    collapseElement.addEventListener('show.bs.collapse', function () {
        arrowIcon.classList.remove('bi-caret-right');
        arrowIcon.classList.add('bi-caret-down');
    });

    collapseElement.addEventListener('hide.bs.collapse', function () {
        arrowIcon.classList.remove('bi-caret-down');
        arrowIcon.classList.add('bi-caret-right');
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const uploadLink = document.getElementById('uploadNewResume');
    const fileInput = document.getElementById('newResumeInput');
    const resumeInput = document.getElementById('resumeInput');
    const dropdownBtn = document.getElementById('resumeDropdown');

    // Upload new resume
    uploadLink.addEventListener('click', function(e) {
        e.preventDefault();
        fileInput.click(); // reliably opens file picker
    });

    // When a file is selected, update hidden input and dropdown label
    fileInput.addEventListener('change', function() {
        if (fileInput.files.length > 0) {
            dropdownBtn.textContent = fileInput.files[0].name;
            resumeInput.value = 'upload_new'; // mark as new upload in backend
        }
    });

    // Existing resumes
    document.querySelectorAll('.resume-item').forEach(function(item) {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const id = item.getAttribute('data-id');
            const text = item.textContent;
            dropdownBtn.textContent = text;    // update button label
            resumeInput.value = id;             // store selected resume ID
            fileInput.value = '';               // clear file input if previously used
        });
    });
});
