import axios from "axios";

// this how you can create an axios instance with a base URL and default headers
const apiClient = axios.create({
    baseURL: "http://127.0.0.1:8000/api/v1",
    headers: {
        "Content-Type": "application/json",
    },
    timeout: 10000,
});

export default apiClient;