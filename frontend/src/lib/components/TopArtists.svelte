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
  <div class="text-gray-500 text-sm">Loading...</div>
{:else}
  <div class="space-y-1">
    {#each artists as artist, i}
      <a href="/artist/{encodeURIComponent(artist.name)}" 
         class="flex items-center gap-3 py-1.5 hover:bg-viz-border/50 rounded px-2 -mx-2 transition-colors">
        <div class="w-5 text-xs text-gray-600">{i + 1}</div>
        <div class="flex-1 truncate text-sm">{artist.name}</div>
        <div class="text-gray-600 text-xs">{artist.count}</div>
      </a>
    {/each}
  </div>
{/if}
