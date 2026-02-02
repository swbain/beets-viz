<script>
  import { onMount } from 'svelte';

  let genres = [];
  let loading = true;
  let selectedGenre = null;
  let maxCount = 0;

  onMount(async () => {
    const res = await fetch('/api/genres');
    genres = await res.json();
    maxCount = genres.length ? genres[0].count : 0;
    loading = false;
  });
</script>

<svelte:head>
  <title>Genres | pavlovsfrog-music</title>
</svelte:head>

<div class="space-y-6">
  <div>
    <h1 class="text-2xl font-medium mb-1">Genres</h1>
    <p class="text-gray-500 text-sm">{genres.length} genres in your collection</p>
  </div>

  {#if loading}
    <div class="flex items-center justify-center h-64">
      <div class="text-gray-500">Loading...</div>
    </div>
  {:else}
    <!-- Top genres -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
      {#each genres.slice(0, 12) as genre}
        <a
          href="/browse?genre={encodeURIComponent(genre.name)}"
          class="card hover:border-gray-600 transition-colors"
        >
          <div class="font-medium truncate">{genre.name}</div>
          <div class="text-gray-500 text-sm">{genre.count} albums</div>
        </a>
      {/each}
    </div>

    <!-- All genres -->
    <div class="card">
      <h2 class="text-lg font-medium mb-4">All Genres</h2>
      <div class="flex flex-wrap gap-2">
        {#each genres as genre}
          <a
            href="/browse?genre={encodeURIComponent(genre.name)}"
            class="px-2 py-1 text-sm text-gray-400 hover:text-white border border-viz-border rounded hover:border-gray-500 transition-colors"
          >
            {genre.name}
            <span class="text-gray-600 ml-1">{genre.count}</span>
          </a>
        {/each}
      </div>
    </div>
  {/if}
</div>
