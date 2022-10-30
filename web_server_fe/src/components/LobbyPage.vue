<script lang="ts">
import { defineComponent } from 'vue'
import { io, Socket } from "socket.io-client";
import { v4 as uuid } from 'uuid';


type User = {
    name: string,
    uuid: string,
}

type ComponentData = {
    loading: boolean,
    uuid: string,
    users: User[],
    socket: Socket,
}

export default defineComponent({
    data(): ComponentData {
        return {
            loading: false,
            uuid: '',
            users: [] as User[],
            socket: io(),
        }
    },
    mounted() {
        this.uuid = uuid();
        this.socket.emit('lobby_create', { username: 'blub', lobby_uuid: this.uuid })
    },
    methods: {
        kickUser() {
        }
    }
})
</script>

<template>
    <h4>Users</h4>
    <li v-for="user in users">
        <button @click="kickUser">{{ user.name }}</button>
    </li>
    <Dialog></Dialog>
</template>