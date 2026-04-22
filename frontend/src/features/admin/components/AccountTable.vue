<template>
  <div class="text-text min-w-full overflow-x-auto p-4">
    <div
      class="border-border text-text mb-2 grid grid-cols-5 items-center gap-4 border-b-2 text-base font-medium uppercase"
    >
      <div class="col-span-1 text-left">ID</div>
      <div class="col-span-2 text-left">Имя пользователя</div>
      <div class="col-span-2 text-center">Действия</div>
    </div>

    <div v-for="user in accounts" :key="user.id">
      <div class="border-border mb-1 grid grid-cols-5 items-center gap-4 border-b text-base">
        <div class="col-span-1 text-left text-sm opacity-60">{{ user.id }}</div>
        <div class="col-span-2 text-left">{{ user.username }}</div>
        <div class="col-span-2 text-center">
          <button @click="onEdit(user)" class="btn-default mb-1 w-full py-1 text-base">
            Edit
          </button>
          <button
            @click="onDelete(user.id, user.username)"
            class="btn-error mb-1 w-full py-1 text-base"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  accounts: {
    type: Array,
    required: true,
  },
});
const emit = defineEmits(['edit', 'delete']);
const onEdit = (user) => emit('edit', user);
const onDelete = (id, username) => emit('delete', id, username);
</script>
