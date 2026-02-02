<script>
  export let label = '';
  export let value = '';
  export let size = 'normal';
</script>

<div class="card">
  <div class="text-gray-500 text-xs uppercase tracking-wide mb-1">{label}</div>
  <div class="{size === 'small' ? 'text-xl' : 'text-2xl'} font-medium">{value}</div>
</div>
