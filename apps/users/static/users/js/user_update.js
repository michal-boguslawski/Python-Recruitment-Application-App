document.addEventListener("DOMContentLoaded", function() {
    const selectBtn = document.getElementById("selectPhotoBtn");
    const removeBtn = document.getElementById("removePhotoBtn");
    const fileInput = document.getElementById("id_profile_picture");
    const preview = document.getElementById("profilePreview");

    selectBtn.addEventListener("click", () => fileInput.click());

    fileInput.addEventListener("change", () => {
        if (fileInput.files && fileInput.files[0]) {
            const reader = new FileReader();
            reader.onload = e => preview.src = e.target.result;
            reader.readAsDataURL(fileInput.files[0]);
        }
    });

    removeBtn.addEventListener("click", () => {
        fileInput.value = "";  // clears the selected file
        preview.src = preview.dataset.defaultSrc;
    });
});


// Enhance description fields to use textarea on focus
document.addEventListener("DOMContentLoaded", function() {


    function makeTextareaOnFocus(input) {
        input.addEventListener("focus", function handleFocus() {
            const textarea = document.createElement("textarea");
            textarea.className = input.className;
            textarea.name = input.name;
            textarea.value = input.value;

            // Make it visually larger
            textarea.rows = 6;          
            textarea.style.width = "100%";
            textarea.style.minHeight = "100px";

            // Replace input with textarea
            input.parentNode.replaceChild(textarea, input);
            textarea.focus();

            // When textarea loses focus, revert back to input
            textarea.addEventListener("blur", function handleBlur() {
                const newInput = document.createElement("input");
                newInput.type = "text";
                newInput.className = textarea.className;
                newInput.name = textarea.name;
                newInput.value = textarea.value;

                textarea.parentNode.replaceChild(newInput, textarea);

                // Reattach the focus handler to the new input
                makeTextareaOnFocus(newInput);
            });
        });
    }

    // Attach to all existing description fields
    document.querySelectorAll(".description-field").forEach(function(input) {
        makeTextareaOnFocus(input);
    });

    // Formset management
    const addRowBtn = document.getElementById("addRow");
    const removeLastRowBtn = document.getElementById("removeLastRow");
    const formsetTable = document.getElementById("formsetTable"); // tbody
    const totalFormsInput = document.getElementById("id_form-TOTAL_FORMS");
    const template = document.getElementById("emptyFormTemplate");

    if (!formsetTable || !totalFormsInput || !template) return; // required elements missing

    let formCount = parseInt(totalFormsInput.value, 10);

    function replacePrefix(element, index) {
        if (element.nodeType === Node.ELEMENT_NODE) {
            if (element.name) element.name = element.name.replace(/__prefix__/g, index);
            if (element.id) element.id = element.id.replace(/__prefix__/g, index);
        }
        element.childNodes.forEach(child => replacePrefix(child, index));
    }

    // Add new row
    addRowBtn.addEventListener("click", function() {
        const clone = template.content.cloneNode(true);
        replacePrefix(clone, formCount);

        // Append the new row to tbody
        const newRow = clone.firstElementChild;
        newRow.dataset.dynamic = "true"; 
        formsetTable.appendChild(newRow);

        // Attach textarea-on-focus behavior to the new row's description input
        const descInput = newRow.querySelector(".description-field");
        if (descInput) makeTextareaOnFocus(descInput);


        formCount++;
        totalFormsInput.value = formCount;
    });
    // Remove last row
    removeLastRowBtn.addEventListener("click", function() {
        const rows = formsetTable.querySelectorAll("tr[data-dynamic='true']");
        if (rows.length > 0) {
            const lastDynamicRow = rows[rows.length - 1];
            lastDynamicRow.remove();
            formCount--;
            totalFormsInput.value = formCount;
        }
    });
});
