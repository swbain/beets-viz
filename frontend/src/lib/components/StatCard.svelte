<script>
  export let label = '';
  export let value = '';
  export let icon = '📊';
  export let size = 'normal';
</script>

<div class="card flex items-center gap-4 {size === 'small' ? 'py-4' : ''}">
  <span class="text-3xl">{icon}</span>
  <div>
    <div class="{size === 'small' ? 'text-2xl' : 'stat-number'}">{value}</div>
    <div class="text-gray-400 text-sm">{label}</div>
  </div>
</div>
