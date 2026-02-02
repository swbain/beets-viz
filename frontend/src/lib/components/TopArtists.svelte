<script>
  import { onMount } from 'svelte';

  let artists = [];
  let loading = true;

  onMount(async () => {
    try {
      const res = await fetch('/api/artists?limit=10');
      artists = await res.json();
    } catch (e) {
      console.error('Failed to load artists:', e);
    }
    loading = false;
  });
</script>

{#if loading}
  <div class="space-y-3">
    {#each Array(10) as _}
      <div class="animate-pulse flex items-center gap-3">
        <div class="w-8 h-8 bg-viz-border rounded-full"></div>
        <div class="flex-1 h-4 bg-viz-border rounded"></div>
      </div>
    {/each}
  </div>
{:else}
  <div class="space-y-3">
    {#each artists as artist, i}
      <a href="/artist/{encodeURIComponent(artist.name)}" 
         class="flex items-center gap-3 p-2 rounded-lg hover:bg-viz-border/50 transition-colors group">
        <div class="w-8 h-8 rounded-full bg-gradient-to-br from-viz-accent to-pink-500 flex items-center justify-center text-sm font-bold">
          {i + 1}
        </div>
        <div class="flex-1 truncate group-hover:text-viz-accent transition-colors">
          {artist.name}
        </div>
        <div class="text-gray-500 text-sm">{artist.count} albums</div>
      </a>
    {/each}
  </div>
{/if}
