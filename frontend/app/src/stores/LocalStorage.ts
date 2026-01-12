import type { User } from '@/types/User'
import type { SearchCondition } from '@/types/Project'

const STORAGE_EXPIRATION_TIME = 12 * 60 * 60 * 1000

const STORAGE_KEY_LOGIN_USER = 'login_user'
const STORAGE_KEY_PROJECT_CONDITION = 'project_condition'

export function saveLoginUser(user: User | null) {
  if (user) {
    const data = {
      user,
      timestamp: new Date().getTime(),
    }
    localStorage.setItem(STORAGE_KEY_LOGIN_USER, JSON.stringify(data))
  } else {
    localStorage.removeItem(STORAGE_KEY_LOGIN_USER)
  }
}

export function loadLoginUser(): User | null {
  const dataString = localStorage.getItem(STORAGE_KEY_LOGIN_USER)
  if (dataString) {
    const data = JSON.parse(dataString)
    const currentTime = new Date().getTime()

    if (currentTime - data.timestamp > STORAGE_EXPIRATION_TIME) {
      localStorage.removeItem(STORAGE_KEY_LOGIN_USER)
      return null
    }
    return data.user as User
  }
  return null
}

export function saveProjectCondition(condition: SearchCondition | null) {
  if (condition) {
    const data = {
      condition,
      timestamp: new Date().getTime(),
    }
    localStorage.setItem(STORAGE_KEY_PROJECT_CONDITION, JSON.stringify(data))
  } else {
    localStorage.removeItem(STORAGE_KEY_PROJECT_CONDITION)
  }
}

export function loadProjectCondition(): SearchCondition | null {
  const dataString = localStorage.getItem(STORAGE_KEY_PROJECT_CONDITION)
  if (dataString) {
    const data = JSON.parse(dataString)
    const currentTime = new Date().getTime()

    if (currentTime - data.timestamp > STORAGE_EXPIRATION_TIME) {
      localStorage.removeItem(STORAGE_KEY_PROJECT_CONDITION)
      return null
    }
    return data.condition as SearchCondition
  }
  return null
}
