<script lang="ts">
	import { login as apiLogin } from '$lib/api';
	import { token, user } from '$lib/auth';
	import { getMe } from '$lib/api';
	import { goto } from '$app/navigation';

	let email = $state('');
	let password = $state('');
	let error = $state('');
	let loading = $state(false);

	async function handleSubmit(e: Event) {
		e.preventDefault();
		error = '';
		loading = true;

		try {
			const result = await apiLogin(email, password);
			token.set(result.access_token);
			const me = await getMe(result.access_token);
			user.set(me);
			goto('/dashboard');
		} catch (err) {
			error = err instanceof Error ? err.message : 'Login failed';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Login — Starter App</title>
</svelte:head>

<div class="max-w-md mx-auto mt-20">
	<div class="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-8">
		<h1 class="text-2xl font-bold mb-6 text-center">Login</h1>

		{#if error}
			<div class="bg-red-500/10 border border-red-500/30 text-[var(--error)] rounded-lg p-3 mb-4 text-sm">
				{error}
			</div>
		{/if}

		<form onsubmit={handleSubmit} class="space-y-4">
			<div>
				<label for="email" class="block text-sm text-[var(--text-secondary)] mb-1">Email</label>
				<input
					id="email"
					type="email"
					bind:value={email}
					required
					class="w-full bg-[var(--bg-primary)] border border-[var(--border)] rounded-lg px-4 py-2.5 text-[var(--text-primary)] focus:border-[var(--accent)] focus:outline-none transition"
					placeholder="you@example.com"
				/>
			</div>

			<div>
				<label for="password" class="block text-sm text-[var(--text-secondary)] mb-1">Password</label>
				<input
					id="password"
					type="password"
					bind:value={password}
					required
					class="w-full bg-[var(--bg-primary)] border border-[var(--border)] rounded-lg px-4 py-2.5 text-[var(--text-primary)] focus:border-[var(--accent)] focus:outline-none transition"
					placeholder="Your password"
				/>
			</div>

			<button
				type="submit"
				disabled={loading}
				class="w-full bg-[var(--accent)] hover:bg-[var(--accent-hover)] disabled:opacity-50 text-white font-medium py-2.5 rounded-lg transition"
			>
				{loading ? 'Logging in...' : 'Login'}
			</button>
		</form>

		<p class="text-center text-[var(--text-secondary)] text-sm mt-4">
			Don't have an account? <a href="/register" class="text-[var(--accent)] hover:underline">Register</a>
		</p>
	</div>
</div>
