<script lang="ts">
  import { fade, slide } from 'svelte/transition';
  import { quintOut } from 'svelte/easing';

  let showUserInfoForm = true;
  let showCalculator = false;

  let firstName = '';
  let lastName = '';
  let email = '';
  let phone = '';

  let transactionAmount = 0;
  let currency = 'USD';
  let merchantCountry = 'USA';
  let customerCountry = 'USA';
  let paymentMethod = 'Card';
  let dayOfWeek = 'Weekday';
  let optionalMarkup = 0;
  let pspsToCompare = [];

  const currencies = ['USD', 'EUR', 'GBP', 'JPY'];
  const countries = ['USA', 'Canada', 'UK', 'Australia', 'Germany', 'India'];
  const paymentMethods = ['Card', 'ACH', 'Bank Transfer', 'PayPal Balance'];
  const pspOptions = ['Stripe', 'PayPal', 'Square', 'Wise'];

  function validateEmail(email: string) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
  }

  function validatePhone(phone: string): boolean {
    const cleanedPhone = phone.replace(/\D/g, ''); // Remove non-digits
    return cleanedPhone.length === 10;
  }

  function formatPhoneNumber(phoneNumberString: string): string {
    const cleaned = phoneNumberString.replace(/\D/g, '');
    const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/);
    if (match) {
      return `(${match[1]})-${match[2]}-${match[3]}`;
    }
    return phoneNumberString; // Return original if not 10 digits
  }

  let displayPhone = ''; // This will be bound to the input field

  $: { // Reactive statement to update displayPhone when phone changes
    if (phone) {
      displayPhone = formatPhoneNumber(phone);
    } else {
      displayPhone = '';
    }
  }

  async function submitUserInfo() {
    if (!firstName || !lastName || !email || !phone) {
      alert('Please fill in all required fields.');
      return;
    }
    if (!validateEmail(email)) {
      alert('Please enter a valid email address.');
      return;
    }
    if (!validatePhone(phone)) {
      alert('Please enter a valid 10-digit phone number.');
      return;
    }

    // Placeholder for backend submission
    console.log('Submitting user info:', { firstName, lastName, email, phone });
    // In a real app, you'd make an API call here

    showUserInfoForm = false;
    showCalculator = true;
  }

  let simulationResults: any[] = [];

  async function calculateFees() {
    try {
      const response = await fetch('http://localhost:8000/simulate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          amount: transactionAmount,
          currency: currency,
          merchant_country: merchantCountry,
          customer_country: customerCountry,
          payment_method: paymentMethod,
          day_of_week: dayOfWeek === 'Weekday' ? 'weekday' : 'weekend',
          optional_markup: optionalMarkup,
          psps_to_compare: pspsToCompare,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        alert(`Error: ${errorData.detail || response.statusText}`);
        return;
      }

      const data = await response.json();
      simulationResults = data.results; // Store the results
      console.log("Simulation Results:", simulationResults); // Add this line

    } catch (error) {
      console.error('Error calculating fees:', error);
      alert('Failed to calculate fees. Please try again.');
    }
  }
</script>

<div class="container mx-auto py-12 px-4">
  <h1 class="text-4xl md:text-5xl font-bold text-center mb-8">FeePilot Simulation</h1>

  {#if showUserInfoForm}
    <div class="card bg-base-100 shadow-xl p-8 max-w-2xl mx-auto" transition:fade={{ duration: 500 }}>
      <h2 class="card-title text-2xl mb-6">Step 1: Your Information</h2>
      <p class="mb-4 text-gray-600">Please provide your details to proceed with the simulation.</p>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <label class="form-control w-full">
          <div class="label"><span class="label-text">First Name</span></div>
          <input type="text" placeholder="John" class="input input-bordered w-full" bind:value={firstName} required />
        </label>
        <label class="form-control w-full">
          <div class="label"><span class="label-text">Last Name</span></div>
          <input type="text" placeholder="Doe" class="input input-bordered w-full" bind:value={lastName} required />
        </label>
        <label class="form-control w-full">
          <div class="label"><span class="label-text">Email</span></div>
          <input type="email" placeholder="john.doe@example.com" class="input input-bordered w-full" bind:value={email} required />
        </label>
        <label class="form-control w-full">
          <div class="label"><span class="label-text">Phone Number</span></div>
          <input type="tel" placeholder="(123)-456-7890" class="input input-bordered w-full" bind:value={displayPhone} on:input={(e) => { phone = e.currentTarget.value.replace(/\D/g, ''); }} required />
        </label>
      </div>
      <button class="btn btn-primary w-full" on:click={submitUserInfo}>Proceed to Calculator</button>
    </div>
  {/if}

  {#if showCalculator}
    <div class="card bg-base-100 shadow-xl p-8 max-w-4xl mx-auto mt-8" transition:slide={{ duration: 500, easing: quintOut }}>
      <h2 class="card-title text-2xl mb-6">Step 2: Transaction Fee Calculator</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <label class="form-control w-full">
          <div class="label"><span class="label-text">Transaction Amount</span></div>
          <input type="number" placeholder="100.00" class="input input-bordered w-full" bind:value={transactionAmount} min="0" step="0.01" required />
        </label>
        <label class="form-control w-full">
          <div class="label"><span class="label-text">Currency</span></div>
          <select class="select select-bordered w-full" bind:value={currency}>
            {#each currencies as c}
              <option>{c}</option>
            {/each}
          </select>
        </label>
        <label class="form-control w-full">
          <div class="label"><span class="label-text">Merchant Country</span></div>
          <select class="select select-bordered w-full" bind:value={merchantCountry}>
            {#each countries as country}
              <option>{country}</option>
            {/each}
          </select>
        </label>
        <label class="form-control w-full">
          <div class="label"><span class="label-text">Customer Country</span></div>
          <select class="select select-bordered w-full" bind:value={customerCountry}>
            {#each countries as country}
              <option>{country}</option>
            {/each}
          </select>
        </label>
        <label class="form-control w-full">
          <div class="label"><span class="label-text">Payment Method</span></div>
          <select class="select select-bordered w-full" bind:value={paymentMethod}>
            {#each paymentMethods as method}
              <option>{method}</option>
            {/each}
          </select>
        </label>
        <label class="form-control w-full">
          <div class="label"><span class="label-text">Day of Week</span></div>
          <div class="flex space-x-2">
            <button
              class="btn flex-1 {dayOfWeek === 'Weekday' ? 'btn-primary' : 'btn-outline'}"
              on:click={() => (dayOfWeek = 'Weekday')}
            >Weekday</button>
            <button
              class="btn flex-1 {dayOfWeek === 'Weekend' ? 'btn-primary' : 'btn-outline'}"
              on:click={() => (dayOfWeek = 'Weekend')}
            >Weekend</button>
          </div>
        </label>
        <label class="form-control w-full">
          <div class="label"><span class="label-text">Optional Markup (%)</span></div>
          <input type="number" placeholder="0" class="input input-bordered w-full" bind:value={optionalMarkup} min="0" step="0.01" />
        </label>
        <label class="form-control w-full">
          <div class="label"><span class="label-text">PSPs to Compare</span></div>
          <div class="flex flex-wrap gap-2">
            {#each pspOptions as psp}
              <label class="label cursor-pointer">
                <input type="checkbox" class="checkbox checkbox-primary" value={psp} bind:group={pspsToCompare} />
                <span class="label-text ml-2">{psp}</span>
              </label>
            {/each}
          </div>
        </label>
      </div>
      <button class="btn btn-primary w-full" on:click={calculateFees}>Calculate Fees</button>

      <!-- Comparison Dashboard -->
      {#if simulationResults.length > 0}
        <div class="mt-8 border-t pt-8" transition:fade={{ duration: 500 }}>
          <h3 class="text-xl font-bold mb-4">Comparison Dashboard</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {#each simulationResults as result}
              <div class="card bg-base-200 shadow-md">
                <div class="card-body">
                  <h4 class="card-title">{result.psp_name}</h4>
                  <p>Effective Rate: {result.effective_rate.toFixed(2)}%</p>
                  <p>Fixed Fee: ${result.fixed_fee.toFixed(2)}</p>
                  <p>Variable Fee: ${result.variable_fee.toFixed(2)}</p>
                  <p>FX Cost: ${result.fx_cost.toFixed(2)}</p>
                  <p>Weekend Surcharge: ${result.weekend_surcharge.toFixed(2)}</p>
                  <p>Cross-Border Surcharge: ${result.cross_border_surcharge.toFixed(2)}</p>
                  <p class="font-bold">Net Revenue: ${result.net_revenue.toFixed(2)}</p>
                </div>
              </div>
            {/each}
          </div>
        </div>
      {/if}
    </div>
  {/if}
</div>