const BaseClient = {
    async get(endpoint: string) {
        const response = await fetch(endpoint);
        return response.json();
    },

    async post(endpoint: string, body: Object = {}) {
        return fetch(
            endpoint,
            {
                method: 'POST',
                body: JSON.stringify(body),
                headers: {
                    'Content-Type': 'application/json'
                },
            }
        );
    }
}

export default BaseClient;
