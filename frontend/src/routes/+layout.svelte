<script lang="ts">
	import '../app.css';
	import { token, user, logout } from '$lib/auth';
	import { getMe } from '$lib/api';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	let { children } = $props();

	onMount(async () => {
		const t = $token;
		if (t) {
			try {
				const me = await getMe(t);
				user.set(me);
			} catch {
				logout();
			}
		}
	});

	function handleLogout() {
		logout();
		goto('/login');
	}
</script>

<div class="min-h-screen flex flex-col">
	<nav class="border-b border-[var(--border)] px-6 py-4 flex items-center justify-between">
		<a href="/" class="text-xl font-bold text-[var(--accent)]">Starter App</a>
		<div class="flex items-center gap-4">
			{#if $user}
				<span class="text-[var(--text-secondary)] text-sm">{$user.name}</span>
				<button
					onclick={handleLogout}
					class="text-sm text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition"
				>
					Logout
				</button>
			{:else}
				<a href="/login" class="text-sm text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition">Login</a>
				<a href="/register" class="text-sm bg-[var(--accent)] hover:bg-[var(--accent-hover)] text-white px-4 py-2 rounded-lg transition">Register</a>
			{/if}
		</div>
	</nav>

	<main class="flex-1 p-6">
		{@render children()}
	</main>

	<footer class="border-t border-[var(--border)] px-6 py-4 text-center text-[var(--text-secondary)] text-sm">
		Built with <a href="https://github.com/Quartalis/sveltekit-fastapi-starter" class="text-[var(--accent)] hover:underline" target="_blank" rel="noopener">SvelteKit + FastAPI Starter</a>
	</footer>
</div>
