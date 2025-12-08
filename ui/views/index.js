let api = null;

function selectFolder() {
    if (!api) api = window.pywebview.api;

    api.select_folder().then(path => {
        if (path) {
            const folderName = path.split("/").pop();
            document.getElementById("folder-name").innerText = "Selected folder: " + folderName;
        }
    });
}

function runProcessing() {
    if (!api) api = window.pywebview.api;

    document.getElementById("progress").innerText = "Processing...";
    api.run_processing();
}

function updateProgress(index, total, filename) {
    document.getElementById("progress").innerText = `Processing ${index}/${total}: ${filename}`
}

function onFinished() {
    document.getElementById("progress").innerText = "Finished!";
}