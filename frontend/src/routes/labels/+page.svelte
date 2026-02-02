<script>
  import { onMount } from 'svelte';

  let labels = [];
  let loading = true;
  let maxCount = 0;

  onMount(async () => {
    const res = await fetch('/api/labels?limit=100');
    labels = await res.json();
    maxCount = labels.length ? labels[0].count : 0;
    loading = false;
  });
</script>

<svelte:head>
  <title>Labels | beets-viz</title>
</svelte:head>

<div class="space-y-6">
  <div>
    <h1 class="text-3xl font-bold mb-2">Record Labels</h1>
    <p class="text-gray-400">Which labels dominate your collection?</p>
  </div>

  {#if loading}
    <div class="flex items-center justify-center h-96">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-viz-accent"></div>
    </div>
  {:else}
    <!-- Top 10 as big cards -->
    <div class="grid md:grid-cols-2 gap-4">
      {#each labels.slice(0, 10) as label, i}
        <a 
          href="/browse?label={encodeURIComponent(label.name)}"
          class="card flex items-center gap-4 hover:border-viz-accent transition-colors"
        >
          <div class="text-3xl font-bold text-viz-accent w-16 text-right">#{i + 1}</div>
          <div class="flex-1 min-w-0">
            <div class="font-semibold truncate">{label.name}</div>
            <div class="text-gray-400 text-sm">{label.count} albums</div>
          </div>
          <div class="w-32 h-3 bg-viz-border rounded-full overflow-hidden">
            <div 
              class="h-full bg-gradient-to-r from-viz-accent to-pink-500 rounded-full"
              style="width: {(label.count / maxCount) * 100}%"
            ></div>
          </div>
        </a>
      {/each}
    </div>

    <!-- Rest as smaller list -->
    <div class="card">
      <h2 class="text-xl font-semibold mb-4">All Labels ({labels.length})</h2>
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-2">
        {#each labels.slice(10) as label}
          <a 
            href="/browse?label={encodeURIComponent(label.name)}"
            class="flex items-center justify-between p-2 rounded-lg hover:bg-viz-border/50 transition-colors"
          >
            <span class="truncate">{label.name}</span>
            <span class="text-gray-500 text-sm ml-2">{label.count}</span>
          </a>
        {/each}
      </div>
    </div>
  {/if}
</div>
