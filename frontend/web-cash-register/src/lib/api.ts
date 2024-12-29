// import { NEXT_PUBLIC_API_URL } from "@/config/api";

export async function fetchData<T>(
    endpoint: string,
    apiURL?: { method: string; body: string },
    options?: RequestInit
): Promise<T> {
    const token = localStorage.getItem('token');
    // const url = apiURL || NEXT_PUBLIC_API_URL;
    // console.log(`${url}/${endpoint}`)
    const response = await fetch(`http://localhost:8000/${endpoint}`, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            Authorization: token ? `Bearer ${token}`: '',
            ...(options?.headers ?? {}),
        },
    });

    if (!response.ok) {
        throw new Error(response.statusText);
    }

    return response.json();
}

// import { NEXT_PUBLIC_API_URL } from "@/config/api";

export async function editData(
    endpoint: string,
    method: "POST" | "PUT" | "DELETE" = "POST",
    options?: RequestInit
) {
    const token = localStorage.getItem('token');
    const response = await fetch(`http://localhost:8000/${endpoint}`, {
        method: method,
        ...options,
        headers: {
            'Content-Type': 'application/json',
            Authorization: token ? `Bearer ${token}`: '',
            ...(options?.headers ?? {}),
        },
    });

    if (!response.ok) {
        if (response.status === 400) {
            const errorData = await response.json();
            throw { validationError: errorData };
        }
        throw new Error(response.statusText);
    }
    if (response.statusText === '204') return response.json()
    return null;


}