<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  props: { showDialog: Boolean },
  data() {
    return { code: "" };
  },
});
</script>

<template>
  <Dialog
    class="w-6"
    header="Join lobby"
    v-bind:modal="true"
    v-bind:closable="false"
    v-bind:draggable="false"
    v-model:visible="showDialog"
  >
    <div style="padding-top: 1.5rem">
      <span class="p-float-label">
        <InputText
          id="code"
          class="w-full"
          v-model="code"
          v-bind:class="code.length != 5 && 'p-invalid'"
          type="number"
          min="10000"
          max="99999"
        />
        <label for="code">Code</label>
      </span>
    </div>
    <template #footer>
      <Button
        @click="$emit('confirm', code)"
        v-bind:disabled="code.length != 5"
        label="Confirm"
        autofocus
      />
    </template>
  </Dialog>
</template>
