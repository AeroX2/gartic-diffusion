<template>
  <Card>
    <template #title> Gartic Diffusion </template>
    <template #content>
      <div class="flex flex-column gap-2">
        <RouterLink to="/lobby/create">
          <Button
            class="flex justify-content-center w-full"
            label="Create Lobby"
          />
        </RouterLink>
        <RouterLink to="/lobby/join">
          <Button
            class="flex justify-content-center w-full"
            label="Join Lobby"
          />
        </RouterLink>
      </div>
    </template>
  </Card>
</template>
