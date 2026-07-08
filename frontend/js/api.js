const API_BASE_URL = "http://127.0.0.1:8000";


/**
 * Uploads a HAR file to the backend.
 * Returns the parsed JSON response.
 */
async function uploadHAR(file) {

    const formData = new FormData();

    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/upload/`, {

        method: "POST",

        body: formData

    });

    if (!response.ok) {

        const error = await response.json();

        throw new Error(error.detail || "Upload failed.");

    }

    return await response.json();

}