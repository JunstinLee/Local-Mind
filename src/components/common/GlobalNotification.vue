<template>
  <transition name="notification-fade">
    <div
      v-if="uiStore.notification.show"
      class="tw-fixed tw-top-20 tw-left-1/2 tw--translate-x-1/2 tw-px-6 tw-py-3 tw-rounded-lg tw-shadow-xl tw-text-white tw-z-[10000]"
      :class="{
        'tw-bg-green-500': uiStore.notification.type === 'success',
        'tw-bg-red-500': uiStore.notification.type === 'error',
      }"
    >
      {{ uiStore.notification.message }}
    </div>
  </transition>
</template>

<script setup>
import { useUiStore } from '@/stores/modules/ui'
const uiStore = useUiStore()
</script>

<style scoped>
.notification-fade-enter-active,
.notification-fade-leave-active {
  transition:
    opacity 0.3s ease,
    transform 0.3s ease;
}

.notification-fade-enter-from,
.notification-fade-leave-to {
  opacity: 0;
  transform: translateY(-20px) translateX(-50%);
}

.notification-fade-enter-to,
.notification-fade-leave-from {
  opacity: 1;
  transform: translateY(0) translateX(-50%);
}
</style>