const API_BASE = "http://127.0.0.1:5000";

async function api(endpoint, options = {}) {

    const response = await fetch(
        `${API_BASE}${endpoint}`,
        {
            ...options,

            headers: {
                "Content-Type": "application/json",
                ...(options.headers || {})
            }
        }
    );

    const data =
        await response.json().catch(() => ({}));


    if (!response.ok) {

        throw new Error(
            data.error ||
            "Something went wrong"
        );

    }

    return data;
}