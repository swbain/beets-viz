<script>
  import { onMount } from 'svelte';

  let albums = [];
  let loading = true;

  onMount(async () => {
    try {
      const res = await fetch('/api/recent?limit=12');
      albums = await res.json();
    } catch (e) {
      console.error('Failed to load recent albums:', e);
    }
    loading = false;
  });

  function getArtUrl(artpath) {
    if (!artpath) return null;
    return `/api/art?path=${encodeURIComponent(artpath)}`;
  }
</script>

{#if loading}
  <div class="text-gray-500 text-sm">Loading...</div>
{:else}
  <div class="grid grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
    {#each albums as album}
      <a href="/album/{album.id}" class="group">
        <div class="aspect-square bg-viz-border rounded overflow-hidden mb-1.5">
          {#if album.artpath}
            <img 
              src={getArtUrl(album.artpath)} 
              alt="{album.album}"
              class="w-full h-full object-cover"
              loading="lazy"
            />
          {:else}
            <div class="w-full h-full flex items-center justify-center text-gray-700 text-xl">♪</div>
          {/if}
        </div>
        <div class="truncate text-sm group-hover:text-white transition-colors">{album.album}</div>
        <div class="truncate text-xs text-gray-600">{album.artist}</div>
      </a>
    {/each}
  </div>
{/if}
