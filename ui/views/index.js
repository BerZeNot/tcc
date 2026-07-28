let api = null;
const folders = []

function selectFolder() {
    if (!api) api = window.pywebview.api;

    api.select_folder().then(selectedFolderPath => {
        if (selectedFolderPath) {
            const folderName = selectedFolderPath.split("/").pop();
            folders.push({
                "name": folderName,
                "path": selectedFolderPath
            });
            updateSelectedFoldersDisplay()
        }
    });
}

const updateSelectedFoldersDisplay = () => {
    let foldersListing = document.getElementById("selected-folders")
    foldersListing.innerHTML = '';

    if (folders.length == 0) {
        foldersListing.innerHTML = '<p>No folders selected. Add a folder</p>';
        return;
    }

    for (folderData of folders) {
        let folderNameInBase64 = btoa(folderData.name)
        let template = `
            <div class="folder-row">
                <img src="./assets/yellow-folder.svg" alt="folder icon">
                <span title="${folderData.name}">
                    ${truncateString(folderData.name, 30)}
                </span>
                <button name="btRemoveFolder" folderNameInBase64="${folderNameInBase64}" type="button">
                    <img src="./assets/red-x.svg" alt="red-x icon">
                </button>
            </div>
        `;
        foldersListing.innerHTML += template;
        document.querySelectorAll('[name="btRemoveFolder"]').forEach(bt => {
            bt.addEventListener("click", removeFolder);
        });
    }
}

const truncateString = (string, maxLength) => {
    if (string.length > maxLength)
        return string.substr(0, maxLength) + "...";

    return string;
}

const removeFolder = (event) => {
    const folderNameInBase64 = event.currentTarget.attributes['folderNameInBase64'].value;
    if (!folderNameInBase64)
        return;

    const folderName = atob(folderNameInBase64)
    const indexToRemove = folders.findIndex(folderData => folderData.name === folderName);
    if (indexToRemove < 0)
        return;

    api.remove_selected_folder(folders[indexToRemove].path);
    folders.splice(indexToRemove, 1);
    updateSelectedFoldersDisplay();
}

function runProcessing() {
    if (!api) api = window.pywebview.api;

    if (folders.length <= 0) {
        alert("Please select a folder first")
        return;
    }

    document.getElementById("progress-text").innerText = "Processing...";
    showProgressBar();
    processingOptions = buildProcessingOptions()
    api.run_processing(processingOptions);
}

const showProgressBar = () => {
    document.getElementById("progress-bar-section").hidden = false;
}

const hideProgressBar = () => {
    document.getElementById("progress-bar-section").hidden = true;
    document.getElementById("progressFill").style.width = `${0}%`;
    document.getElementById("progressLabel").textContent = `${0}%`;
}

function updateProgress(current, total, filename) {
    document.getElementById("progress-text").innerText = `Processing ${current}/${total}: ${filename}`

    const percent = Math.round(current / total * 100);

    document.getElementById("progressFill").style.width = `${percent}%`;
    document.getElementById("progressLabel").textContent = `${percent}%`;
}

function onFinished(outputFolder) {
    const processFinishedMessage =
        `<span class="bt-icon-alignment">
            <img src="./assets/green-circle-check-big.svg" alt="folder icon">
            Finished! Result saved at <span class="result-highlight">${outputFolder}</span>
        </span>`;

    document.getElementById("progress-text").innerHTML = processFinishedMessage;
    hideProgressBar();
}

function buildProcessingOptions() {
    var processingOptions = {}

    const cutEdgespercentage = document.getElementById("cut-edges-percentage").value ?? 0;
    const invertSegmentImages = document.getElementById("invert-segmented-images").checked ?? false;
    const sperm_type = document.getElementById("sperm-type").value ?? "BULL";

    processingOptions["cut_edges"] = cutEdgespercentage;
    processingOptions["invert_segmented_images"] = invertSegmentImages;
    processingOptions["segment_images"] = false;
    processingOptions["sperm_type"] = sperm_type;

    return processingOptions;
}