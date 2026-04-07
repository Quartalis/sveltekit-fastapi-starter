<script lang="ts">
	import { register as apiRegister, login as apiLogin, getMe } from '$lib/api';
	import { token, user } from '$lib/auth';
	import { goto } from '$app/navigation';

	let name = $state('');
	let email = $state('');
	let password = $state('');
	let error = $state('');
	let loading = $state(false);

	async function handleSubmit(e: Event) {
		e.preventDefault();
		error = '';
		loading = true;

		try {
			await apiRegister(email, password, name);
			const result = await apiLogin(email, password);
			token.set(result.access_token);
			const me = await getMe(result.access_token);
			user.set(me);
			goto('/dashboard');
		} catch (err) {
			error = err instanceof Error ? err.message : 'Registration failed';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Register — Starter App</title>
</svelte:head>

<div class="max-w-md mx-auto mt-20">
	<div class="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-8">
		<h1 class="text-2xl font-bold mb-6 text-center">Create Account</h1>

		{#if error}
			<div class="bg-red-500/10 border border-red-500/30 text-[var(--error)] rounded-lg p-3 mb-4 text-sm">
				{error}
			</div>
		{/if}

		<form onsubmit={handleSubmit} class="space-y-4">
			<div>
				<label for="name" class="block text-sm text-[var(--text-secondary)] mb-1">Name</label>
				<input
					id="name"
					type="text"
					bind:value={name}
					required
					class="w-full bg-[var(--bg-primary)] border border-[var(--border)] rounded-lg px-4 py-2.5 text-[var(--text-primary)] focus:border-[var(--accent)] focus:outline-none transition"
					placeholder="Your name"
				/>
			</div>

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
					minlength="8"
					class="w-full bg-[var(--bg-primary)] border border-[var(--border)] rounded-lg px-4 py-2.5 text-[var(--text-primary)] focus:border-[var(--accent)] focus:outline-none transition"
					placeholder="Minimum 8 characters"
				/>
			</div>

			<button
				type="submit"
				disabled={loading}
				class="w-full bg-[var(--accent)] hover:bg-[var(--accent-hover)] disabled:opacity-50 text-white font-medium py-2.5 rounded-lg transition"
			>
				{loading ? 'Creating account...' : 'Create Account'}
			</button>
		</form>

		<p class="text-center text-[var(--text-secondary)] text-sm mt-4">
			Already have an account? <a href="/login" class="text-[var(--accent)] hover:underline">Login</a>
		</p>
	</div>
</div>
