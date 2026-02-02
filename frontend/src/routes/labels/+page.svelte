<script>
  import { onMount } from 'svelte';

  let labels = [];
  let loading = true;

  onMount(async () => {
    const res = await fetch('/api/labels?limit=200');
    labels = await res.json();
    loading = false;
  });
</script>

<svelte:head>
  <title>Labels | pavlovsfrog-music</title>
</svelte:head>

<div class="space-y-6">
  <div>
    <h1 class="text-2xl font-medium mb-1">Labels</h1>
    <p class="text-gray-500 text-sm">{labels.length} labels in your collection</p>
  </div>

  {#if loading}
    <div class="text-center py-12 text-gray-500">Loading...</div>
  {:else}
    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-2">
      {#each labels as label, i}
        <a 
          href="/browse?label={encodeURIComponent(label.name)}"
          class="flex items-center justify-between p-3 rounded border border-viz-border hover:border-gray-600 transition-colors"
        >
          <span class="truncate">{label.name}</span>
          <span class="text-gray-600 text-sm ml-2">{label.count}</span>
        </a>
      {/each}
    </div>
  {/if}
</div>
