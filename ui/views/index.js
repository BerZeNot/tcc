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
    let foldersListing = document.getElementById("folder-name")
    foldersListing.innerHTML = '';
    for (folderData of folders) {
        let folderNameInBase64 = btoa(folderData.name)
        let template = `
            <div>
                <span>${folderData.name}</span>
                <button name="btRemoveFolder" folderNameInBase64="${folderNameInBase64}" type="button">x</button>
            </div>
        `;
        foldersListing.innerHTML += template;
        document.querySelectorAll('[name="btRemoveFolder"]').forEach(bt => {
            bt.addEventListener("click", removeFolder);
        });
    }
}
const removeFolder = (event) => {
    const folderNameInBase64 = event.target.attributes['folderNameInBase64'].value;
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

    document.getElementById("progress").innerText = "Processing...";
    api.run_processing();
}

function updateProgress(index, total, filename) {
    document.getElementById("progress").innerText = `Processing ${index}/${total}: ${filename}`
}

function onFinished() {
    document.getElementById("progress").innerText = "Finished!";
}