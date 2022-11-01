<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  props: { showDialog: Boolean, error: String },
  data() {
    return { username: "" };
  },
});
</script>

<template>
  <Dialog
    class="w-6"
    header="Set Username"
    v-bind:modal="true"
    v-bind:closable="false"
    v-bind:draggable="false"
    v-model:visible="showDialog"
  >
    <template #default>
      <div class="flex flex-column gap-2">
        <Tag severity="danger" v-if="error">
          {{ error }}
        </Tag>
        <div style="padding-top: 1.5rem">
          <span class="p-float-label">
            <InputText
              class="w-full"
              id="username"
              autocomplete="off"
              v-model="username"
              v-bind:class="username.length <= 0 && 'p-invalid'"
              @keyup.enter="username.length > 0 && $emit('confirm', username)"
              type="text"
              autofocus
            />
            <label for="username">Username</label>
          </span>
        </div>
      </div>
    </template>
    <template #footer>
      <Button
        @click="$emit('confirm', username)"
        v-bind:disabled="username.length <= 0"
        label="Confirm"
      />
    </template>
  </Dialog>
</template>
