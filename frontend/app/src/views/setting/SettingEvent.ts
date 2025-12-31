import mitt from 'mitt'

type Events = {
  openCreateTargetDialog: void
  openCreateUserDialog: void
  openCreateCompanyDialog: void
  openCreateProjectGroupDialog: void
}

const emitter = mitt<Events>()
export default emitter
