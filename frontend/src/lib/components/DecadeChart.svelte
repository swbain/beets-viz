<script>
  import { onMount } from 'svelte';

  let decades = [];
  let maxCount = 0;

  onMount(async () => {
    try {
      const res = await fetch('/api/decades');
      decades = await res.json();
      maxCount = Math.max(...decades.map(d => d.count));
    } catch (e) {
      console.error('Failed to load decades:', e);
    }
  });

  function getDecadeLabel(year) {
    if (!year) return '?';
    return `${year}s`;
  }
</script>

<div class="space-y-1.5">
  {#each decades as decade}
    <div class="flex items-center gap-3">
      <div class="w-12 text-xs text-gray-500">{getDecadeLabel(decade.decade)}</div>
      <div class="flex-1 h-5 bg-viz-border rounded overflow-hidden">
        <div 
          class="h-full bg-gray-600 rounded"
          style="width: {(decade.count / maxCount) * 100}%"
        ></div>
      </div>
      <div class="w-12 text-right text-xs text-gray-600">{decade.count.toLocaleString()}</div>
    </div>
  {/each}
</div>
