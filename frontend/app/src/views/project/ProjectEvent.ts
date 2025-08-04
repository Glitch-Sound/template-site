import mitt from 'mitt'

type Events = {
  openCreateProjectDialog: void
}

const emitter = mitt<Events>()
export default emitter
