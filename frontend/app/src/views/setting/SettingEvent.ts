import mitt from 'mitt'

type Events = {
  openCreateUserDialog: void
}

const emitter = mitt<Events>()
export default emitter
