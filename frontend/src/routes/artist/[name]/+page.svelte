<script>
  import { page } from '$app/stores';
  import { onMount } from 'svelte';

  let albums = [];
  let loading = true;
  let total = 0;
  let limit = 48;
  let offset = 0;
  let sort = 'year';
  let order = 'asc';
  
  $: artistName = decodeURIComponent($page.params.name);
  $: totalPages = Math.ceil(total / limit);
  $: currentPage = Math.floor(offset / limit) + 1;

  async function fetchAlbums() {
    loading = true;
    const res = await fetch(`/api/artist/${encodeURIComponent(artistName)}?limit=${limit}&offset=${offset}&sort=${sort}&order=${order}`);
    const data = await res.json();
    albums = data.albums;
    total = data.total;
    loading = false;
  }

  onMount(fetchAlbums);

  function goToPage(pageNum) {
    offset = (pageNum - 1) * limit;
    fetchAlbums();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function toggleSort(newSort) {
    if (sort === newSort) {
      order = order === 'asc' ? 'desc' : 'asc';
    } else {
      sort = newSort;
      order = newSort === 'added' ? 'desc' : 'asc';
    }
    offset = 0;
    fetchAlbums();
  }

  function getArtUrl(artpath) {
    if (!artpath) return null;
    return `/api/art?path=${encodeURIComponent(artpath)}`;
  }

  function getPageNumbers() {
    const pages = [];
    const maxVisible = 7;
    
    if (totalPages <= maxVisible) {
      for (let i = 1; i <= totalPages; i++) pages.push(i);
    } else {
      pages.push(1);
      if (currentPage > 3) pages.push('...');
      
      let start = Math.max(2, currentPage - 1);
      let end = Math.min(totalPages - 1, currentPage + 1);
      
      if (currentPage <= 3) end = 4;
      if (currentPage >= totalPages - 2) start = totalPages - 3;
      
      for (let i = start; i <= end; i++) pages.push(i);
      
      if (currentPage < totalPages - 2) pages.push('...');
      pages.push(totalPages);
    }
    return pages;
  }
</script>

<svelte:head>
  <title>{artistName} | pavlovsfrog-music</title>
</svelte:head>

<div class="space-y-6">
  <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4">
    <div>
      <a href="/" class="text-gray-400 hover:text-white text-sm">← Dashboard</a>
      <h1 class="text-4xl font-bold mt-2">{artistName}</h1>
      <p class="text-gray-400 mt-1">
        {#if loading && total === 0}
          Loading...
        {:else}
          {total} albums in your collection
        {/if}
      </p>
    </div>
    
    <div class="flex gap-2 text-sm">
      <button 
        on:click={() => toggleSort('year')}
        class="px-3 py-1.5 rounded-lg transition-colors {sort === 'year' ? 'bg-viz-accent text-white' : 'bg-viz-card hover:bg-viz-border'}"
      >
        Year {sort === 'year' ? (order === 'asc' ? '↑' : '↓') : ''}
      </button>
      <button 
        on:click={() => toggleSort('album')}
        class="px-3 py-1.5 rounded-lg transition-colors {sort === 'album' ? 'bg-viz-accent text-white' : 'bg-viz-card hover:bg-viz-border'}"
      >
        Title {sort === 'album' ? (order === 'asc' ? '↑' : '↓') : ''}
      </button>
      <button 
        on:click={() => toggleSort('added')}
        class="px-3 py-1.5 rounded-lg transition-colors {sort === 'added' ? 'bg-viz-accent text-white' : 'bg-viz-card hover:bg-viz-border'}"
      >
        Added {sort === 'added' ? (order === 'asc' ? '↑' : '↓') : ''}
      </button>
    </div>
  </div>

  {#if loading && albums.length === 0}
    <div class="flex items-center justify-center h-64">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-viz-accent"></div>
    </div>
  {:else if albums.length === 0}
    <div class="text-center py-12 text-gray-400">
      No albums found for this artist
    </div>
  {:else}
    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-6">
      {#each albums as album}
        <a href="/album/{album.id}" class="group">
          <div class="aspect-square bg-viz-border rounded-lg overflow-hidden mb-2">
            {#if album.artpath}
              <img 
                src={getArtUrl(album.artpath)} 
                alt={album.album}
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                loading="lazy"
              />
            {:else}
              <div class="w-full h-full flex items-center justify-center text-4xl text-gray-600">
                🎵
              </div>
            {/if}
          </div>
          <div class="truncate font-medium group-hover:text-viz-accent transition-colors">
            {album.album}
          </div>
          <div class="text-sm text-gray-500">{album.year || '—'}</div>
        </a>
      {/each}
    </div>

    <!-- Pagination -->
    {#if totalPages > 1}
      <div class="flex items-center justify-center gap-2 pt-4">
        <button 
          on:click={() => goToPage(currentPage - 1)}
          disabled={currentPage === 1}
          class="px-3 py-2 rounded-lg bg-viz-card hover:bg-viz-border disabled:opacity-50 disabled:cursor-not-allowed"
        >
          ←
        </button>
        
        {#each getPageNumbers() as pageNum}
          {#if pageNum === '...'}
            <span class="px-2 text-gray-500">...</span>
          {:else}
            <button 
              on:click={() => goToPage(pageNum)}
              class="px-3 py-2 rounded-lg transition-colors {pageNum === currentPage ? 'bg-viz-accent text-white' : 'bg-viz-card hover:bg-viz-border'}"
            >
              {pageNum}
            </button>
          {/if}
        {/each}
        
        <button 
          on:click={() => goToPage(currentPage + 1)}
          disabled={currentPage === totalPages}
          class="px-3 py-2 rounded-lg bg-viz-card hover:bg-viz-border disabled:opacity-50 disabled:cursor-not-allowed"
        >
          →
        </button>
      </div>
    {/if}
  {/if}
</div>
