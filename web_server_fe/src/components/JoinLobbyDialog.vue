<script lang="ts">
import { defineComponent } from "vue";
import { Html5Qrcode } from "html5-qrcode";
import { useToast } from "primevue/usetoast";

export default defineComponent({
  props: { showDialog: Boolean, error: String },
  data() {
    return { code: "", toast: useToast() };
  },
  methods: {
    openCamera() {
      const html5QrCode = new Html5Qrcode("reader");
      html5QrCode
        .start(
          { facingMode: { exact: "environment" } },
          {
            fps: 10,
          },
          (decodedText) => {
            if (parseInt(decodedText).toString().length != 5) return;
            this.$emit("confirm", decodedText);
            html5QrCode.stop();
          },
          (_) => {
            // parse error, ignore it.
          }
        )
        .catch((err) => {
          this.toast.add({
            severity: "error",
            summary: "Error happened",
            detail: err,
            life: 3000,
          });
        });
    },
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
        <div id="reader" width="600px" height="600px"></div>
        <Button @click="openCamera()" class="pi pi-camera">Use camera</Button>
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
