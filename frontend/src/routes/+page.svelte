<script lang="ts">
	import { token } from '$lib/auth';
</script>

<svelte:head>
	<title>SvelteKit + FastAPI Starter</title>
</svelte:head>

<div class="max-w-2xl mx-auto text-center mt-20">
	<h1 class="text-4xl font-bold mb-4">SvelteKit + FastAPI Starter</h1>
	<p class="text-[var(--text-secondary)] text-lg mb-8">
		A production-ready starter template with JWT authentication, dark theme, and Docker deployment.
	</p>

	{#if $token}
		<a
			href="/dashboard"
			class="inline-block bg-[var(--accent)] hover:bg-[var(--accent-hover)] text-white px-6 py-3 rounded-lg text-lg font-medium transition"
		>
			Go to Dashboard
		</a>
	{:else}
		<div class="flex gap-4 justify-center">
			<a
				href="/login"
				class="bg-[var(--bg-secondary)] border border-[var(--border)] hover:border-[var(--accent)] text-[var(--text-primary)] px-6 py-3 rounded-lg text-lg font-medium transition"
			>
				Login
			</a>
			<a
				href="/register"
				class="bg-[var(--accent)] hover:bg-[var(--accent-hover)] text-white px-6 py-3 rounded-lg text-lg font-medium transition"
			>
				Get Started
			</a>
		</div>
	{/if}

	<div class="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
		<div class="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-6">
			<h3 class="text-lg font-semibold mb-2">JWT Authentication</h3>
			<p class="text-[var(--text-secondary)] text-sm">Secure login and registration with bcrypt hashing and JWT tokens.</p>
		</div>
		<div class="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-6">
			<h3 class="text-lg font-semibold mb-2">Dark Theme</h3>
			<p class="text-[var(--text-secondary)] text-sm">Beautiful dark UI with Tailwind CSS v4, ready for customisation.</p>
		</div>
		<div class="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-6">
			<h3 class="text-lg font-semibold mb-2">Docker Ready</h3>
			<p class="text-[var(--text-secondary)] text-sm">One-command deployment with Docker Compose for both frontend and backend.</p>
		</div>
	</div>
</div>
