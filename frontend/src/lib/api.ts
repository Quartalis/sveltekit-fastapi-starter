const API_BASE = '/api';

interface ApiOptions {
	method?: string;
	body?: unknown;
	token?: string;
}

export async function api(endpoint: string, options: ApiOptions = {}) {
	const headers: Record<string, string> = {
		'Content-Type': 'application/json'
	};

	if (options.token) {
		headers['Authorization'] = `Bearer ${options.token}`;
	}

	const res = await fetch(`${API_BASE}${endpoint}`, {
		method: options.method || 'GET',
		headers,
		body: options.body ? JSON.stringify(options.body) : undefined
	});

	if (!res.ok) {
		const error = await res.json().catch(() => ({ detail: 'Request failed' }));
		throw new Error(error.detail || 'Request failed');
	}

	return res.json();
}

export async function login(email: string, password: string) {
	const formData = new URLSearchParams();
	formData.append('username', email);
	formData.append('password', password);

	const res = await fetch(`${API_BASE}/auth/login`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
		body: formData
	});

	if (!res.ok) {
		const error = await res.json().catch(() => ({ detail: 'Login failed' }));
		throw new Error(error.detail || 'Login failed');
	}

	return res.json();
}

export async function register(email: string, password: string, name: string) {
	return api('/auth/register', {
		method: 'POST',
		body: { email, password, name }
	});
}

export async function getMe(token: string) {
	return api('/me', { token });
}
