<script lang="ts">
  // This page would be protected by JWT in a real application
  // and fetch data from /admin/simulations and handle tracking scripts.

  let userSubmissions = []; // Placeholder for fetched data
  let googlePixelScript = '';
  let facebookPixelScript = '';
  let trackingEnabled = false;

  async function fetchUserSubmissions() {
    console.log('Fetching user submissions...');
    // Placeholder for API call to /admin/simulations
    userSubmissions = [
      { id: 1, firstName: 'John', lastName: 'Doe', email: 'john@example.com', phone: '+1234567890', timestamp: new Date().toLocaleString() },
      { id: 2, firstName: 'Jane', lastName: 'Smith', email: 'jane@example.com', phone: '+1987654321', timestamp: new Date().toLocaleString() },
    ];
  }

  async function saveTrackingScripts() {
    console.log('Saving tracking scripts:', { googlePixelScript, facebookPixelScript, trackingEnabled });
    // Placeholder for API call to /admin/tracking
    alert('Tracking scripts saved! (Logic to be implemented with backend)');
  }

  // Fetch submissions on component mount (in a real app, after authentication)
  // onMount(fetchUserSubmissions);
</script>

<div class="container mx-auto py-12 px-4">
  <h1 class="text-4xl md:text-5xl font-bold text-center mb-8">Admin Dashboard</h1>

  <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
    <div class="card bg-base-100 shadow-xl p-8">
      <h2 class="card-title text-2xl mb-6">User Submissions</h2>
      <button class="btn btn-primary mb-4" on:click={fetchUserSubmissions}>Load User Submissions</button>
      {#if userSubmissions.length > 0}
        <div class="overflow-x-auto">
          <table class="table w-full">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {#each userSubmissions as submission}
                <tr>
                  <td>{submission.id}</td>
                  <td>{submission.firstName} {submission.lastName}</td>
                  <td>{submission.email}</td>
                  <td>{submission.phone}</td>
                  <td>{submission.timestamp}</td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      {:else}
        <p>No user submissions loaded yet.</p>
      {/if}
    </div>

    <div class="card bg-base-100 shadow-xl p-8">
      <h2 class="card-title text-2xl mb-6">Tracking Script Management</h2>
      <label class="form-control w-full mb-4">
        <div class="label"><span class="label-text">Google Pixel Script</span></div>
        <textarea class="textarea textarea-bordered h-32" placeholder="<!-- Google Pixel Code -->" bind:value={googlePixelScript}></textarea>
      </label>
      <label class="form-control w-full mb-4">
        <div class="label"><span class="label-text">Facebook Pixel Script</span></div>
        <textarea class="textarea textarea-bordered h-32" placeholder="<!-- Facebook Pixel Code -->" bind:value={facebookPixelScript}></textarea>
      </label>
      <div class="form-control mb-6">
        <label class="label cursor-pointer">
          <span class="label-text">Enable Tracking</span>
          <input type="checkbox" class="toggle toggle-primary" bind:checked={trackingEnabled} />
        </label>
      </div>
      <button class="btn btn-primary w-full" on:click={saveTrackingScripts}>Save Tracking Scripts</button>
    </div>
  </div>
</div>