<script lang="ts">
	import { token, user } from '$lib/auth';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	onMount(() => {
		if (!$token) {
			goto('/login');
		}
	});
</script>

<svelte:head>
	<title>Dashboard — Starter App</title>
</svelte:head>

{#if $user}
	<div class="max-w-4xl mx-auto mt-10">
		<h1 class="text-3xl font-bold mb-2">Welcome, {$user.name}</h1>
		<p class="text-[var(--text-secondary)] mb-8">This is your dashboard. Start building your app from here.</p>

		<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
			<div class="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-6">
				<h3 class="text-lg font-semibold mb-2">Your Profile</h3>
				<div class="space-y-2 text-sm">
					<p><span class="text-[var(--text-secondary)]">Email:</span> {$user.email}</p>
					<p><span class="text-[var(--text-secondary)]">Name:</span> {$user.name}</p>
				</div>
			</div>

			<div class="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-6">
				<h3 class="text-lg font-semibold mb-2">Quick Start</h3>
				<ul class="space-y-2 text-sm text-[var(--text-secondary)]">
					<li>1. Add your routes in <code class="text-[var(--accent)]">src/routes/</code></li>
					<li>2. Add API endpoints in <code class="text-[var(--accent)]">backend/main.py</code></li>
					<li>3. Deploy with <code class="text-[var(--accent)]">docker compose up</code></li>
				</ul>
			</div>

		</div>
	</div>
{/if}
