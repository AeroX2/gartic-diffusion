<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  props: { showDialog: Boolean },
  data() {
    return { username: "" };
  },
});
</script>

<template>
  <Dialog
    header="Set Username"
    v-bind:modal="true"
    v-bind:closable="false"
    v-bind:draggable="false"
    v-model:visible="showDialog"
  >
    <template #default>
      <div style="padding-top: 1.5rem">
        <span class="p-float-label">
          <InputText
            id="username"
            v-model="username"
            v-bind:class="username.length <= 0 && 'p-invalid'"
            type="text"
          />
          <label for="username">Username</label>
        </span>
      </div>
    </template>
    <template #footer>
      <Button
        @click="$emit('confirm', username)"
        v-bind:disabled="username.length <= 0"
        label="Confirm"
        autofocus
      />
    </template>
  </Dialog>
</template>
