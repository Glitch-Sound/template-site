import mitt from 'mitt'

type Events = {
  openCreateUserDialog: void
  openCreateCompanyDialog: void
}

const emitter = mitt<Events>()
export default emitter
