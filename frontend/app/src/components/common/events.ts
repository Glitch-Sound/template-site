export type EmitType<E extends string, T> = {
  (event: E, payload: T): void
}
