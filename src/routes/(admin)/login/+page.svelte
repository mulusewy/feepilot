<script lang="ts">
  let email = '';
  let password = '';

  async function handleLogin() {
    console.log('Admin Login Attempt:', { email, password });
    // Placeholder for API call to /admin/login
    alert('Login logic to be implemented with backend.');
  }
</script>

<div class="container mx-auto py-12 px-4">
  <div class="card bg-base-100 shadow-xl p-8 max-w-md mx-auto">
    <h1 class="card-title text-3xl mb-6 text-center">Admin Login</h1>
    <form on:submit|preventDefault={handleLogin}>
      <label class="form-control w-full mb-4">
        <div class="label"><span class="label-text">Email</span></div>
        <input type="email" placeholder="admin@example.com" class="input input-bordered w-full" bind:value={email} required />
      </label>
      <label class="form-control w-full mb-6">
        <div class="label"><span class="label-text">Password</span></div>
        <input type="password" placeholder="********" class="input input-bordered w-full" bind:value={password} required />
      </label>
      <button type="submit" class="btn btn-primary w-full">Login</button>
    </form>
  </div>
</div>