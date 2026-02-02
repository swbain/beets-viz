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

  function getColor(index) {
    const colors = [
      'from-violet-500 to-purple-600',
      'from-blue-500 to-cyan-500',
      'from-emerald-500 to-teal-500',
      'from-orange-500 to-amber-500',
      'from-pink-500 to-rose-500',
      'from-indigo-500 to-blue-500',
    ];
    return colors[index % colors.length];
  }

  function getSize(count) {
    const ratio = count / maxCount;
    if (ratio > 0.5) return 'text-2xl p-6';
    if (ratio > 0.2) return 'text-lg p-4';
    if (ratio > 0.1) return 'text-base p-3';
    return 'text-sm p-2';
  }
</script>

<svelte:head>
  <title>Genres | beets-viz</title>
</svelte:head>

<div class="space-y-6">
  <div>
    <h1 class="text-3xl font-bold mb-2">Genre Explorer</h1>
    <p class="text-gray-400">What kinds of music do you collect?</p>
  </div>

  {#if loading}
    <div class="flex items-center justify-center h-96">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-viz-accent"></div>
    </div>
  {:else}
    <!-- Top genres as big cards -->
    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {#each genres.slice(0, 12) as genre, i}
        <button
          class="card bg-gradient-to-br {getColor(i)} border-0 text-white text-left hover:scale-105 transition-transform"
          on:click={() => selectedGenre = genre}
        >
          <div class="text-xl font-bold truncate">{genre.name}</div>
          <div class="text-white/70">{genre.count.toLocaleString()} albums</div>
        </button>
      {/each}
    </div>

    <!-- All genres as smaller tags -->
    <div class="card">
      <h2 class="text-xl font-semibold mb-4">All Genres</h2>
      <div class="flex flex-wrap gap-2">
        {#each genres as genre, i}
          <button
            class="px-3 py-1 rounded-full bg-viz-border hover:bg-viz-accent/20 transition-colors text-sm"
            class:bg-viz-accent={selectedGenre?.name === genre.name}
            class:text-white={selectedGenre?.name === genre.name}
            on:click={() => selectedGenre = genre}
          >
            {genre.name}
            <span class="text-gray-500 ml-1">{genre.count}</span>
          </button>
        {/each}
      </div>
    </div>

    <!-- Selected genre detail (future: show albums in this genre) -->
    {#if selectedGenre}
      <div class="card border-viz-accent">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-2xl font-bold">{selectedGenre.name}</h2>
          <button 
            class="text-gray-400 hover:text-white"
            on:click={() => selectedGenre = null}
          >
            ✕
          </button>
        </div>
        <p class="text-4xl font-bold text-viz-accent">{selectedGenre.count.toLocaleString()}</p>
        <p class="text-gray-400">albums in this genre</p>
        <a 
          href="/browse?genre={encodeURIComponent(selectedGenre.name)}" 
          class="inline-block mt-4 px-4 py-2 bg-viz-accent rounded-lg hover:bg-viz-accent-dim transition-colors"
        >
          Browse Albums →
        </a>
      </div>
    {/if}
  {/if}
</div>
