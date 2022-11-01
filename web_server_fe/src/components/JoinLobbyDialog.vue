<script lang="ts">
import { defineComponent } from "vue";
import { Html5Qrcode, Html5QrcodeSupportedFormats } from "html5-qrcode";
import { useToast } from "primevue/usetoast";

export default defineComponent({
  props: { showDialog: Boolean, error: String },
  data() {
    return { code: "", toast: useToast() };
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
    <template #default>
      <div class="flex flex-column gap-2">
        <Tag severity="danger" v-if="error">
          {{ error }}
        </Tag>
        <div style="padding-top: 1.5rem">
          <span class="p-float-label">
            <InputText
              id="code"
              class="w-full"
              autocomplete="off"
              v-model="code"
              v-bind:class="code.length != 5 && 'p-invalid'"
              @keyup.enter="code.length == 5 && $emit('confirm', code)"
              type="number"
              min="10000"
              max="99999"
              autofocus
            />
            <label for="code">Code</label>
          </span>
        </div>
      </div>
    </template>
    <template #footer>
      <Button
        @click="$emit('confirm', code)"
        v-bind:disabled="code.length != 5"
        label="Confirm"
      />
    </template>
  </Dialog>
</template>
