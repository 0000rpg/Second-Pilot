<script setup>
import { useCounterStore } from '../stores/counter';

let useCounter = useCounterStore();
</script>

<template>
	<h2 @click="useCounter.increment()">Тестовый счётчик (кликай): {{ useCounter.count }}</h2>
</template>

<style scoped></style>
