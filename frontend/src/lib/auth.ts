import { writable } from 'svelte/store';

export const token = writable<string | null>(
	typeof localStorage !== 'undefined' ? localStorage.getItem('token') : null
);

export const user = writable<{ email: string; name: string } | null>(null);

token.subscribe((value) => {
	if (typeof localStorage !== 'undefined') {
		if (value) {
			localStorage.setItem('token', value);
		} else {
			localStorage.removeItem('token');
		}
	}
});

export function logout() {
	token.set(null);
	user.set(null);
}
