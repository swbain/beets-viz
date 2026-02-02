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
    // Convert file path to API endpoint (we'll add this)
    return `/api/art?path=${encodeURIComponent(artpath)}`;
  }

  function timeSince(timestamp) {
    if (!timestamp) return '';
    const seconds = Math.floor(Date.now() / 1000 - timestamp);
    const intervals = [
      { label: 'year', seconds: 31536000 },
      { label: 'month', seconds: 2592000 },
      { label: 'day', seconds: 86400 },
      { label: 'hour', seconds: 3600 },
      { label: 'minute', seconds: 60 }
    ];
    for (const interval of intervals) {
      const count = Math.floor(seconds / interval.seconds);
      if (count >= 1) {
        return `${count} ${interval.label}${count > 1 ? 's' : ''} ago`;
      }
    }
    return 'Just now';
  }
</script>

{#if loading}
  <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
    {#each Array(12) as _}
      <div class="animate-pulse">
        <div class="aspect-square bg-viz-border rounded-lg mb-2"></div>
        <div class="h-4 bg-viz-border rounded w-3/4 mb-1"></div>
        <div class="h-3 bg-viz-border rounded w-1/2"></div>
      </div>
    {/each}
  </div>
{:else}
  <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
    {#each albums as album}
      <a href="/album/{album.id}" class="group">
        <div class="aspect-square bg-viz-border rounded-lg mb-2 overflow-hidden">
          {#if album.artpath}
            <img 
              src={getArtUrl(album.artpath)} 
              alt="{album.album}"
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              loading="lazy"
            />
          {:else}
            <div class="w-full h-full flex items-center justify-center text-4xl text-gray-600">
              🎵
            </div>
          {/if}
        </div>
        <div class="truncate text-sm font-medium group-hover:text-viz-accent transition-colors">
          {album.album}
        </div>
        <div class="truncate text-xs text-gray-500">{album.artist}</div>
        <div class="text-xs text-gray-600">{timeSince(album.added)}</div>
      </a>
    {/each}
  </div>
{/if}
