import mitt from 'mitt'

type Events = {
  openCreateUserDialog: void
  openCreateCompanyDialog: void
  openCreateProjectGroupDialog: void
}

const emitter = mitt<Events>()
export default emitter
